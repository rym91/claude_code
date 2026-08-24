"""Проверка доступа: аккаунт, доски, и какие эндпоинты реально открыты токеном."""

from __future__ import annotations

import sys

from pinterest.pin_api.client import PinterestAPIError, PinterestClient

PROBES = [
    ("/user_account", {}, "профиль"),
    ("/boards", {"page_size": 5}, "доски"),
    ("/user_account/analytics", {
        "start_date": "2026-08-01", "end_date": "2026-08-20",
        "metric_types": ["IMPRESSION", "SAVE"],
    }, "органическая аналитика аккаунта"),
    ("/trends/keywords/US/top/growing", {"limit": 3}, "тренды США"),
    ("/ad_accounts", {"page_size": 5}, "рекламные кабинеты (гео-разрезы)"),
]


def main() -> int:
    client = PinterestClient()
    account = client.get("/user_account")
    print(f"Аккаунт: {account.get('username')}  тип: {account.get('account_type')}")
    print(f"Подписчиков: {account.get('follower_count')}  подписок: {account.get('following_count')}\n")

    print("Доступность эндпоинтов этим токеном:")
    for path, params, label in PROBES:
        try:
            client.get(path, **params)
            print(f"  OK    {label:38} {path}")
        except PinterestAPIError as error:
            print(f"  {error.status:<5} {label:38} {path}  {error.payload[:120]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
