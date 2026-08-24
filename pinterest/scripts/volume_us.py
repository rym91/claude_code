"""Количество запросов по ключам в США.

  GET /v5/ad_accounts/{id}/keywords/metrics?country_code=US&keywords=...
      → keyword_query_volume

Единственный эндпоинт v5, который отдаёт частотность поиска с привязкой к стране.
Значение — не точное число, а корзина ("5M+", "100K-1M"): Pinterest округляет.

  python -m pinterest.scripts.volume_us "ukrainian embroidery" "cross stitch pattern"
  python -m pinterest.scripts.volume_us --from-config        # ключи из keywords_us.json
  python -m pinterest.scripts.volume_us --file=keys.txt      # по ключу в строке
  python -m pinterest.scripts.volume_us --from-config --expand
      дополнительно тянет /terms/related и /terms/suggested и меряет их тоже —
      так из темы пина вырастает список соседних запросов с частотностью
  python -m pinterest.scripts.volume_us --from-config --country=CA
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

from pinterest.pin_api.cli import run
from pinterest.pin_api.client import PinterestAPIError, PinterestClient

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "keywords_us.json"
OUT = ROOT / "out"
CACHE = ROOT / "secrets" / "ad_account.json"
CHUNK = 25  # Pinterest не документирует предел на keywords[], режем с запасом


def parse(argv: list[str]) -> tuple[dict, list[str]]:
    args: dict[str, str | bool] = {}
    rest: list[str] = []
    for item in argv:
        if item.startswith("--"):
            key, _, value = item.partition("=")
            args[key] = value or True
        else:
            rest.append(item)
    return args, rest


def ad_account_id(client: PinterestClient) -> str:
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))["id"]
    accounts = client.get("/ad_accounts", page_size=25).get("items", [])
    if not accounts:
        raise SystemExit(
            "У аккаунта нет рекламного кабинета. keywords/metrics живёт под ad_account,\n"
            "поэтому кабинет нужно завести (бесплатно, тратить бюджет не обязательно):\n"
            "ads.pinterest.com → создать рекламный аккаунт, затем запустить снова."
        )
    chosen = accounts[0]
    CACHE.write_text(json.dumps({"id": chosen["id"], "name": chosen.get("name")}, ensure_ascii=False), encoding="utf-8")
    if len(accounts) > 1:
        print("Кабинетов несколько, взят первый:", chosen.get("name"), chosen["id"])
        print("Чтобы сменить — удали", CACHE)
    return chosen["id"]


def chunks(items: list[str], size: int):
    for start in range(0, len(items), size):
        yield items[start : start + size]


def volumes(client: PinterestClient, account: str, keywords: list[str], country: str) -> dict[str, str]:
    found: dict[str, str] = {}
    for batch in chunks(keywords, CHUNK):
        payload = client.get(
            f"/ad_accounts/{account}/keywords/metrics",
            country_code=country,
            keywords=batch,
        )
        for row in payload.get("data", []):
            found[row.get("keyword", "")] = (row.get("metrics") or {}).get("keyword_query_volume", "")
    return found


def expand(client: PinterestClient, seeds: list[str]) -> dict[str, tuple[str, str]]:
    """{новый ключ: (откуда, из какого сида)} — related и suggested по сидам."""
    grown: dict[str, tuple[str, str]] = {}
    try:
        related = client.get("/terms/related", terms=seeds)
        for entry in related.get("related_terms_list", []):
            for term in entry.get("related_terms", []):
                grown.setdefault(term, ("related", entry.get("term", "")))
    except PinterestAPIError as error:
        print(f"terms/related: HTTP {error.status} {error.payload[:140]}", file=sys.stderr)

    for seed in seeds:
        try:
            for term in client.get("/terms/suggested", term=seed, limit=20):
                grown.setdefault(term, ("suggested", seed))
        except PinterestAPIError as error:
            print(f"terms/suggested «{seed}»: HTTP {error.status} {error.payload[:140]}", file=sys.stderr)
    return grown


def sort_key(volume: str) -> float:
    """«5M+», «100K-1M», «10K» → число для сортировки по убыванию."""
    text = (volume or "").replace("+", "").replace(",", "").strip().lower()
    if not text:
        return -1.0
    text = text.split("-")[-1]  # у диапазона берём верхнюю границу
    factor = 1.0
    if text.endswith("m"):
        factor, text = 1e6, text[:-1]
    elif text.endswith("k"):
        factor, text = 1e3, text[:-1]
    try:
        return float(text) * factor
    except ValueError:
        return -1.0


def main(argv: list[str]) -> int:
    args, inline = parse(argv)
    country = str(args.get("--country", "US")).upper()

    seeds = list(inline)
    if args.get("--file"):
        seeds += [
            line.strip()
            for line in Path(str(args["--file"])).read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")
        ]
    if args.get("--from-config") or not seeds:
        seeds += json.loads(CONFIG.read_text(encoding="utf-8"))["keywords"]
    seeds = list(dict.fromkeys(k.strip().lower() for k in seeds if k.strip()))
    if not seeds:
        print("нет ключей: передай их аргументами, --file= или --from-config", file=sys.stderr)
        return 1

    client = PinterestClient()
    account = ad_account_id(client)
    print(f"Кабинет {account}, страна {country}, ключей на входе: {len(seeds)}\n")

    origin: dict[str, tuple[str, str]] = {k: ("input", "") for k in seeds}
    if args.get("--expand"):
        grown = expand(client, seeds)
        for keyword, meta in grown.items():
            origin.setdefault(keyword.strip().lower(), meta)
        print(f"расширение: +{len(origin) - len(seeds)} соседних запросов\n")

    measured = volumes(client, account, list(origin), country)

    rows = [
        {
            "keyword": keyword,
            "query_volume": measured.get(keyword, ""),
            "source": meta[0],
            "from_seed": meta[1],
        }
        for keyword, meta in origin.items()
    ]
    rows.sort(key=lambda row: sort_key(row["query_volume"]), reverse=True)

    width = max(len(row["keyword"]) for row in rows)
    for row in rows[:40]:
        mark = "" if row["source"] == "input" else f"  ← {row['source']}"
        print(f"  {row['keyword']:<{width}}  {row['query_volume'] or '—':>10}{mark}")
    if len(rows) > 40:
        print(f"  … ещё {len(rows) - 40} в CSV")

    OUT.mkdir(exist_ok=True)
    target = OUT / f"volume_{country.lower()}.csv"
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["keyword", "query_volume", "source", "from_seed"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"\n{len(rows)} строк → {target}")
    return 0


if __name__ == "__main__":
    run(main, sys.argv[1:])
