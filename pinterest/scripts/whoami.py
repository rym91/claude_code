"""Проверка доступа: аккаунт и карта того, какие эндпоинты реально открыты токеном.

Печатает по каждому OK или код ошибки — так сразу видно, что упирается в
trial access, что в скоупы, а что в отсутствие рекламного кабинета.
"""

from __future__ import annotations

import sys

from pinterest.pin_api.cli import run
from pinterest.pin_api.client import PinterestAPIError, PinterestClient

BASE = [
    ("/user_account", {}, "профиль"),
    ("/boards", {"page_size": 5}, "доски"),
    ("/user_account/analytics", {
        "start_date": "2026-08-01", "end_date": "2026-08-20",
        "metric_types": ["IMPRESSION", "SAVE"],
    }, "органическая аналитика аккаунта"),
    ("/user_account/analytics/top_pins", {
        "start_date": "2026-08-01", "end_date": "2026-08-20", "sort_by": "IMPRESSION",
    }, "топ пинов"),
    ("/trends/keywords/US/top/growing", {"limit": 3}, "тренды США"),
    ("/terms/suggested", {"term": "embroidery", "limit": 3}, "подсказанные запросы"),
    ("/ad_accounts", {"page_size": 5}, "рекламные кабинеты"),
]


def probe(client: PinterestClient, path: str, params: dict, label: str) -> None:
    try:
        client.get(path, **params)
        print(f"  OK    {label:34} {path}")
    except PinterestAPIError as error:
        print(f"  {error.status:<5} {label:34} {path}  {error.payload[:110]}")


def main() -> int:
    client = PinterestClient()
    account = client.get("/user_account")
    print(f"Аккаунт: {account.get('username')}   тип: {account.get('account_type')}")
    print(f"Подписчиков: {account.get('follower_count')}   подписок: {account.get('following_count')}\n")

    print("Доступность эндпоинтов:")
    for path, params, label in BASE:
        probe(client, path, params, label)

    # частотность и гео-разрезы живут под ad_account — проверяем отдельно
    try:
        accounts = client.get("/ad_accounts", page_size=5).get("items", [])
    except PinterestAPIError:
        accounts = []
    if not accounts:
        print("\n  Рекламного кабинета нет — недоступны keywords/metrics (частотность по США),")
        print("  targeting_analytics и audience_insights. Кабинет заводится бесплатно на ads.pinterest.com.")
        return 0

    ad_id = accounts[0]["id"]
    print(f"\nПод кабинетом {accounts[0].get('name')} ({ad_id}):")
    probe(client, f"/ad_accounts/{ad_id}/keywords/metrics",
          {"country_code": "US", "keywords": ["embroidery"]}, "частотность запросов США")
    probe(client, f"/ad_accounts/{ad_id}/audience_insights",
          {"audience_insight_type": "YOUR_TOTAL_AUDIENCE"}, "инсайты аудитории")
    probe(client, f"/ad_accounts/{ad_id}/targeting_analytics",
          {"start_date": "2026-08-01", "end_date": "2026-08-20",
           "targeting_types": ["COUNTRY"], "columns": ["PAID_IMPRESSION"], "granularity": "TOTAL"},
          "разрез по странам (платное)")
    return 0


if __name__ == "__main__":
    run(main)
