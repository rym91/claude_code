"""Получение токена: ссылка → code → token.json.

  python -m pinterest.scripts.login                 # напечатать ссылку для браузера
  python -m pinterest.scripts.login --code=ABC123   # обменять code на токен
  python -m pinterest.scripts.login --refresh       # обновить вручную
  python -m pinterest.scripts.login --app-only      # client_credentials (нужен 2FA)
"""

from __future__ import annotations

import sys

from pinterest.pin_api import auth


def main(argv: list[str]) -> int:
    args = {a.split("=", 1)[0]: (a.split("=", 1)[1] if "=" in a else True) for a in argv}

    if "--refresh" in args:
        token = auth.refresh()
    elif "--app-only" in args:
        token = auth.client_credentials()
    elif "--code" in args:
        token = auth.exchange_code(str(args["--code"]))
    else:
        print("Открой ссылку в браузере под аккаунтом ridnavyshyvka, разреши доступ,")
        print("затем скопируй параметр code= из адреса, куда тебя перебросит:\n")
        print(auth.authorize_url())
        print(f"\nПотом: python -m pinterest.scripts.login --code=<code>")
        print("code живёт считаные минуты — меняй сразу.")
        return 0

    print("Токен сохранён в", auth.TOKEN_FILE)
    print("  scope:     ", token.get("scope"))
    print("  expires_in:", token.get("expires_in"), "сек")
    if token.get("refresh_token_expires_in"):
        print("  refresh до:", token.get("refresh_token_expires_in"), "сек")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except auth.PinterestAuthError as error:
        print("Ошибка:", error, file=sys.stderr)
        sys.exit(1)
