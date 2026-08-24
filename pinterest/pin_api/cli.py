"""Общая обёртка запуска: ошибки доступа печатаются человеку, а не трассировкой."""

from __future__ import annotations

import sys
from typing import Callable

from .auth import PinterestAuthError
from .client import PinterestAPIError

HINTS = {
    401: "токен не принят: истёк или отозван — выдай новый кнопкой «Создать маркер» "
         "и сохрани: python -m pinterest.scripts.login --token=<маркер>",
    403: "доступ закрыт: не хватает скоупа либо приложение ещё в trial access",
    404: "объекта нет — проверь id (для ad_account удали secrets/ad_account.json)",
    429: "уперлись в лимит запросов Pinterest, повтори позже",
}


def run(main: Callable[..., int], *args) -> None:
    try:
        sys.exit(main(*args))
    except PinterestAuthError as error:
        print(f"Ошибка доступа: {error}", file=sys.stderr)
        sys.exit(1)
    except PinterestAPIError as error:
        print(f"Pinterest ответил {error.status} на {error.args[0].split(' на ')[-1]}", file=sys.stderr)
        if hint := HINTS.get(error.status):
            print(f"  {hint}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(130)
