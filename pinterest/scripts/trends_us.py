"""Спрос в Pinterest США: /v5/trends/keywords/US/top/{growing|monthly|yearly|seasonal}.

Это единственный источник в API v5, где данные привязаны к стране: у органической
аналитики аккаунта гео-разреза нет вообще (см. README).

  python -m pinterest.scripts.trends_us
  python -m pinterest.scripts.trends_us --types=growing,seasonal --limit=50
  python -m pinterest.scripts.trends_us --no-mine    # только общие тренды ниши
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

from pinterest.pin_api.client import PinterestAPIError, PinterestClient

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "keywords_us.json"
OUT = ROOT / "out"
TREND_TYPES = ["growing", "monthly", "yearly", "seasonal"]


def parse(argv: list[str]) -> dict:
    args: dict[str, str | bool] = {}
    for item in argv:
        key, _, value = item.partition("=")
        args[key] = value or True
    return args


def rows_from(payload: dict, trend_type: str, bucket: str) -> list[dict]:
    rows = []
    for trend in payload.get("trends", []):
        rows.append(
            {
                "trend_type": trend_type,
                "bucket": bucket,
                "keyword": trend.get("keyword"),
                "pct_growth_wow": trend.get("pct_growth_wow"),
                "pct_growth_mom": trend.get("pct_growth_mom"),
                "pct_growth_yoy": trend.get("pct_growth_yoy"),
                "time_series": json.dumps(trend.get("time_series"), ensure_ascii=False)
                if trend.get("time_series")
                else "",
                "demographics": json.dumps(trend.get("demographics"), ensure_ascii=False)
                if trend.get("demographics")
                else "",
            }
        )
    return rows


def main(argv: list[str]) -> int:
    args = parse(argv)
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    types = str(args.get("--types", "")).split(",") if args.get("--types") else TREND_TYPES
    limit = int(args.get("--limit", 50))

    client = PinterestClient()
    rows: list[dict] = []

    for trend_type in types:
        trend_type = trend_type.strip()
        if trend_type not in TREND_TYPES:
            print(f"пропуск неизвестного типа: {trend_type}", file=sys.stderr)
            continue

        # 1) что вообще растёт в интересах ниши по США
        try:
            payload = client.get(
                f"/trends/keywords/US/top/{trend_type}",
                interests=config["interests"],
                limit=limit,
                include_demographics=True,
            )
            rows += rows_from(payload, trend_type, "interests")
            print(f"{trend_type:9} интересы ниши: {len(payload.get('trends', []))}")
        except PinterestAPIError as error:
            print(f"{trend_type:9} интересы ниши: HTTP {error.status} {error.payload[:160]}", file=sys.stderr)

        # 2) наши собственные ключи — где мы на этой кривой
        if args.get("--no-mine"):
            continue
        try:
            payload = client.get(
                f"/trends/keywords/US/top/{trend_type}",
                include_keywords=config["keywords"],
                limit=limit,
                include_demographics=True,
            )
            rows += rows_from(payload, trend_type, "our_keywords")
            print(f"{trend_type:9} наши ключи:    {len(payload.get('trends', []))}")
        except PinterestAPIError as error:
            print(f"{trend_type:9} наши ключи:    HTTP {error.status} {error.payload[:160]}", file=sys.stderr)

    if not rows:
        print("ничего не получено — проверь доступ токена (см. whoami)", file=sys.stderr)
        return 1

    OUT.mkdir(exist_ok=True)
    target = OUT / "trends_us.csv"
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"\n{len(rows)} строк → {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
