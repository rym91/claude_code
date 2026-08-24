"""Тонкий клиент Pinterest API v5: пагинация, лимиты, сериализация списков."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Iterator

from .auth import API, access_token

# параметры, которые по спецификации сериализуются через запятую (explode: false).
# остальные списки Pinterest ждёт повторяющимися ключами.
COMMA_JOINED = {"metric_types", "columns", "targeting_types", "attribution_types"}


class PinterestAPIError(RuntimeError):
    def __init__(self, status: int, payload: str, path: str):
        self.status = status
        self.payload = payload
        super().__init__(f"HTTP {status} на {path}: {payload}")


def _encode(params: dict[str, Any]) -> str:
    pairs: list[tuple[str, str]] = []
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, (list, tuple)):
            if not value:
                continue
            if key in COMMA_JOINED:
                pairs.append((key, ",".join(str(item) for item in value)))
            else:
                pairs.extend((key, str(item)) for item in value)
        elif isinstance(value, bool):
            pairs.append((key, "true" if value else "false"))
        else:
            pairs.append((key, str(value)))
    return urllib.parse.urlencode(pairs)


class PinterestClient:
    def __init__(self, token: str | None = None, max_retries: int = 4):
        self._token = token
        self.max_retries = max_retries

    @property
    def token(self) -> str:
        if self._token is None:
            self._token = access_token()
        return self._token

    def get(self, path: str, **params: Any) -> dict:
        query = _encode(params)
        url = f"{API}{path}" + (f"?{query}" if query else "")
        request = urllib.request.Request(
            url, headers={"Authorization": f"Bearer {self.token}", "Accept": "application/json"}
        )
        delay = 2.0
        for attempt in range(self.max_retries):
            try:
                with urllib.request.urlopen(request, timeout=90) as response:
                    return json.loads(response.read())
            except urllib.error.HTTPError as error:
                payload = error.read().decode(errors="replace")
                retryable = error.code == 429 or 500 <= error.code < 600
                if retryable and attempt < self.max_retries - 1:
                    time.sleep(delay)
                    delay *= 2
                    continue
                raise PinterestAPIError(error.code, payload, path) from error
        raise PinterestAPIError(0, "исчерпаны попытки", path)

    def paginate(self, path: str, page_size: int = 100, **params: Any) -> Iterator[dict]:
        """Обходит bookmark-пагинацию и отдаёт элементы по одному."""
        bookmark = None
        while True:
            page = self.get(path, page_size=page_size, bookmark=bookmark, **params)
            yield from page.get("items", [])
            bookmark = page.get("bookmark")
            if not bookmark:
                return
