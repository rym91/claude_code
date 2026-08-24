"""Органическая аналитика аккаунта и пинов за период.

Гео-разреза здесь нет — Pinterest его в органике не отдаёт. Разрезы, которые есть:
устройство (APP_TYPE), свой/чужой контент (OWNED_CONTENT), источник (SOURCE),
формат пина (PIN_FORMAT).

  python -m pinterest.scripts.account_report --days=30
  python -m pinterest.scripts.account_report --start=2026-07-01 --end=2026-08-24 --split=APP_TYPE
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import sys
from pathlib import Path

from pinterest.pin_api.client import PinterestAPIError, PinterestClient

OUT = Path(__file__).resolve().parent.parent / "out"
METRICS = [
    "IMPRESSION",
    "PIN_CLICK",
    "OUTBOUND_CLICK",
    "SAVE",
    "ENGAGEMENT",
    "ENGAGEMENT_RATE",
    "SAVE_RATE",
    "OUTBOUND_CLICK_RATE",
]


def parse(argv: list[str]) -> dict:
    args: dict[str, str | bool] = {}
    for item in argv:
        key, _, value = item.partition("=")
        args[key] = value or True
    return args


def window(args: dict) -> tuple[str, str]:
    if args.get("--start") and args.get("--end"):
        return str(args["--start"]), str(args["--end"])
    days = int(args.get("--days", 30))
    end = dt.date.today() - dt.timedelta(days=1)   # сегодняшний день Pinterest ещё считает
    return (end - dt.timedelta(days=days - 1)).isoformat(), end.isoformat()


def write_csv(name: str, rows: list[dict]) -> Path:
    OUT.mkdir(exist_ok=True)
    target = OUT / name
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return target


def main(argv: list[str]) -> int:
    args = parse(argv)
    start, end = window(args)
    split = str(args.get("--split", "NO_SPLIT"))
    client = PinterestClient()
    print(f"Период {start} … {end}, split={split}\n")

    daily = client.get(
        "/user_account/analytics",
        start_date=start,
        end_date=end,
        metric_types=METRICS,
        split_field=split,
        content_type="ORGANIC",
    )
    rows: list[dict] = []
    for group, payload in daily.items():
        summary = payload.get("summary_metrics", {})
        for day in payload.get("daily_metrics", []):
            if day.get("data_status") == "NOT_READY":
                continue
            rows.append({"split": group, "date": day.get("date"), **(day.get("metrics") or {})})
        print(f"{group:14} итог за период: " + ", ".join(f"{k}={v}" for k, v in summary.items()))
    if rows:
        print("\nподневно →", write_csv("account_daily.csv", rows))

    try:
        top = client.get(
            "/user_account/analytics/top_pins",
            start_date=start,
            end_date=end,
            sort_by="OUTBOUND_CLICK",
            metric_types=["IMPRESSION", "PIN_CLICK", "OUTBOUND_CLICK", "SAVE", "SAVE_RATE"],
            num_of_pins=50,
            content_type="ORGANIC",
        )
        pins = [
            {"pin_id": item.get("PIN_ID"), **{k: v for k, v in item.items() if k != "PIN_ID"}}
            for item in top.get("pins", [])
        ]
        if pins:
            print("топ пинов →", write_csv("top_pins.csv", pins))
    except PinterestAPIError as error:
        print(f"top_pins: HTTP {error.status} {error.payload[:200]}", file=sys.stderr)

    (OUT / "account_raw.json").write_text(json.dumps(daily, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
