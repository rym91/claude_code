# Аналитика Pinterest по API — США

Инструменты под аккаунт **ridnavyshyvka** (Pinterest API v5, спецификация 5.28.0).

## Главное ограничение, от которого всё зависит

**В органической аналитике Pinterest API нет разреза по странам.** У
`GET /v5/user_account/analytics` параметр `split_field` принимает только
`NO_SPLIT | APP_TYPE | OWNED_CONTENT | SOURCE | PIN_FORMAT`, у
`GET /v5/pins/{pin_id}/analytics` — только `NO_SPLIT | APP_TYPE`. Ни фильтра
по стране, ни сплита по гео там нет. Разбивку «сколько показов пришло из США»
Pinterest отдаёт только в веб-интерфейсе Business Hub, наружу — нет.

Поэтому «аналитика по США» через API складывается из трёх источников:

| Что | Эндпоинт | Гео | Чем платим |
| --- | --- | --- | --- |
| Спрос: что ищут и что растёт в США | `/v5/trends/keywords/US/top/{growing\|monthly\|yearly\|seasonal}` | **есть, `region=US`** | нужен standard access |
| Свои показы/клики/сохранения | `/v5/user_account/analytics`, `/analytics/top_pins`, `/v5/pins/analytics` | нет | — |
| Гео-разрезы аудитории и показов | `/v5/ad_accounts/{id}/targeting_analytics` (`targeting_types=COUNTRY,GEO,REGION`), `/v5/ad_accounts/{id}/audience_insights` | **есть** | нужен рекламный кабинет; `targeting_analytics` считает платные показы |

Практический вывод: **США задаётся на входе (Trends → какие пины делать), а не
на выходе** (в отчёте по своим пинам страну не увидеть). Если нужна именно доля
США в своём трафике — это либо Google Analytics на ridnavyshyvka.com.ua по
источнику `pinterest`, либо рекламный кабинет.

## Доступ

Приложение: **1587527**. Секрет — в `secrets/pinterest.env` (в git не попадает).

Проверено 24.08.2026: пара app_id/secret рабочая (неверный секрет даёт
`code 2 Authentication failed`, наш — доходит до валидации параметров), но
`grant_type=client_credentials` возвращает **`code 1201 Two-factor
authentication required`**. Токен приложения Pinterest выдаёт только когда на
аккаунте-владельце включена двухфакторная аутентификация.

Два пути:

1. **Включить 2FA** на аккаунте Pinterest → работает `--app-only`, всё
   headless. Но токен приложения не пускает к `/user_account/analytics` и
   `/trends/*` — по спецификации у них разрешён только `pinterest_oauth2`.
2. **authorization_code** — один раз через браузер, дальше `refresh_token`
   обновляется сам. Это единственный путь к трендам и аналитике аккаунта.
   Нужен redirect URI, добавленный в настройках приложения.

```bash
python -m pinterest.scripts.login                # печатает ссылку
# открыть, разрешить, скопировать code= из адреса
python -m pinterest.scripts.login --code=<code>  # code живёт минуты
python -m pinterest.scripts.whoami               # что реально открыто токеном
```

`whoami` пробует пять эндпоинтов и печатает по каждому OK или код ошибки —
так сразу видно, что упирается в trial access, а что в скоупы.

## Отчёты

```bash
python -m pinterest.scripts.trends_us                      # спрос США → out/trends_us.csv
python -m pinterest.scripts.trends_us --types=seasonal --limit=50
python -m pinterest.scripts.account_report --days=30       # свои метрики → out/account_daily.csv, out/top_pins.csv
python -m pinterest.scripts.account_report --split=APP_TYPE
```

`keywords_us.json` — что спрашиваем у Trends: интересы ниши
(`diy_and_crafts`, `home_decor`, `wedding`, `womens_fashion`, `art`) и список
англоязычных ключей под нишу. Правится руками.

## Trial vs standard access

Пока приложение в trial access, оно работает только с аккаунтом владельца, и
часть эндпоинтов закрыта. `whoami` покажет, какие именно. После standard access
перепроверить его же — список OK должен вырасти.

## Ограничения, о которые спотыкаются отчёты

- дата «сегодня» ещё не досчитана: `account_report` по умолчанию берёт окно,
  заканчивающееся вчерашним днём;
- дни с `data_status: NOT_READY` пропускаются, чтобы не занижать средние;
- `access_token` живёт 30 дней, `refresh_token` — год; `access_token()`
  обновляет сам, если до истечения меньше суток;
- 429 и 5xx клиент повторяет с экспоненциальной паузой (2/4/8/16 с).

## Файлы

| Файл | Что |
| --- | --- |
| `pin_api/auth.py` | OAuth: authorization_code, refresh, client_credentials |
| `pin_api/client.py` | GET, bookmark-пагинация, ретраи, сериализация списков |
| `scripts/login.py` | получение и обновление токена |
| `scripts/whoami.py` | аккаунт + карта доступных эндпоинтов |
| `scripts/trends_us.py` | спрос по США → CSV |
| `scripts/account_report.py` | свои метрики и топ пинов → CSV |
| `keywords_us.json` | интересы и ключи ниши для Trends |

Зависимостей нет — только стандартная библиотека Python 3.10+.
