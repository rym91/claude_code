"""OAuth для Pinterest API v5.

Три пути получить токен:

  authorization_code  — токен пользователя, нужен браузер один раз.
                        Только он открывает /user_account/analytics и /trends/*.
  refresh_token       — обновление без браузера, дальше всё автоматически.
  client_credentials  — токен приложения без пользователя, но Pinterest требует
                        включённый 2FA на аккаунте-владельце приложения
                        (иначе code 1201 "Two-factor authentication required")
                        и не пускает к user_account/analytics и trends.
"""

from __future__ import annotations

import base64
import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.pinterest.com/v5"
AUTHORIZE = "https://www.pinterest.com/oauth/"

ROOT = Path(__file__).resolve().parent.parent
SECRETS = ROOT / "secrets"
TOKEN_FILE = SECRETS / "token.json"
ENV_FILE = SECRETS / "pinterest.env"

# всё, что нужно для аналитики; write-скоупов сознательно нет
READ_SCOPES = [
    "user_accounts:read",
    "pins:read",
    "boards:read",
    "ads:read",
]


class PinterestAuthError(RuntimeError):
    pass


def _load_env() -> None:
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def app_credentials() -> tuple[str, str]:
    _load_env()
    app_id = os.environ.get("PINTEREST_APP_ID", "").strip()
    secret = os.environ.get("PINTEREST_APP_SECRET", "").strip()
    if not app_id or not secret:
        raise PinterestAuthError(
            "нет PINTEREST_APP_ID / PINTEREST_APP_SECRET — "
            f"заполни {ENV_FILE} по образцу pinterest.env.example"
        )
    return app_id, secret


def redirect_uri() -> str:
    _load_env()
    value = os.environ.get("PINTEREST_REDIRECT_URI", "").strip()
    if not value:
        raise PinterestAuthError("нет PINTEREST_REDIRECT_URI в secrets/pinterest.env")
    return value


def _post_token(data: dict[str, str]) -> dict:
    app_id, secret = app_credentials()
    basic = base64.b64encode(f"{app_id}:{secret}".encode()).decode()
    body = urllib.parse.urlencode(data).encode()
    request = urllib.request.Request(
        f"{API}/oauth/token",
        data=body,
        headers={
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as error:  # noqa: PERF203 — нужен текст ошибки
        payload = error.read().decode(errors="replace")
        hint = ""
        if '"code":1201' in payload.replace(" ", ""):
            hint = (
                "\nPinterest требует двухфакторную аутентификацию на аккаунте-владельце "
                "приложения для токена client_credentials. Включи 2FA в настройках "
                "аккаунта Pinterest либо используй authorization_code."
            )
        raise PinterestAuthError(f"HTTP {error.code} от /oauth/token: {payload}{hint}") from error


def authorize_url(scopes: list[str] | None = None, state: str = "ridnavyshyvka") -> str:
    """Ссылка, которую владелец аккаунта открывает в браузере один раз."""
    app_id, _ = app_credentials()
    query = urllib.parse.urlencode(
        {
            "client_id": app_id,
            "redirect_uri": redirect_uri(),
            "response_type": "code",
            "scope": ",".join(scopes or READ_SCOPES),
            "state": state,
        }
    )
    return f"{AUTHORIZE}?{query}"


def exchange_code(code: str) -> dict:
    """`code` из адресной строки после согласия — живёт считаные минуты."""
    token = _post_token(
        {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri(),
            "continuous_refresh": "true",
        }
    )
    return _save(token)


def refresh(token: dict | None = None) -> dict:
    token = token or _read()
    if not token.get("refresh_token"):
        raise PinterestAuthError("в token.json нет refresh_token — пройди authorization_code заново")
    fresh = _post_token(
        {
            "grant_type": "refresh_token",
            "refresh_token": token["refresh_token"],
            "continuous_refresh": "true",
        }
    )
    # при continuous_refresh Pinterest не всегда возвращает refresh_token — сохраняем старый
    fresh.setdefault("refresh_token", token["refresh_token"])
    return _save(fresh)


def save_manual_token(token: str, expires_in: int = 30 * 86_400, scope: str = "") -> dict:
    """Маркер, выданный кнопкой «Создать маркер» в настройках приложения.

    Обновить его нельзя — когда истечёт, выдаётся новый той же кнопкой.
    """
    return _save(
        {
            "access_token": token.strip(),
            "token_type": "bearer",
            "expires_in": expires_in,
            "scope": scope or ",".join(READ_SCOPES + ["catalogs:read"]),
            "source": "manual_trial_token",
        }
    )


def client_credentials(scopes: list[str] | None = None) -> dict:
    token = _post_token(
        {
            "grant_type": "client_credentials",
            "scope": ",".join(scopes or READ_SCOPES),
        }
    )
    return _save(token)


def _save(token: dict) -> dict:
    token["obtained_at"] = int(time.time())
    SECRETS.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(json.dumps(token, indent=2), encoding="utf-8")
    TOKEN_FILE.chmod(0o600)
    return token


def _read() -> dict:
    if not TOKEN_FILE.exists():
        raise PinterestAuthError(
            f"нет {TOKEN_FILE} — запусти python -m pinterest.scripts.login"
        )
    return json.loads(TOKEN_FILE.read_text(encoding="utf-8"))


def access_token() -> str:
    """Действующий access_token; обновляет сам, если до истечения меньше суток."""
    token = _read()
    expires_at = token.get("obtained_at", 0) + token.get("expires_in", 0)
    if token.get("refresh_token") and expires_at - time.time() < 86_400:
        token = refresh(token)
    elif not token.get("refresh_token") and expires_at < time.time():
        raise PinterestAuthError(
            "маркер истёк, а refresh_token у него нет — выдай новый кнопкой "
            "«Создать маркер» и сохрани: python -m pinterest.scripts.login --token=<маркер>"
        )
    return token["access_token"]
