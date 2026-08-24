# Аналитика Pinterest по API — США

Инструменты под аккаунт **ridnavyshyvka**, Pinterest API v5 (спецификация 5.28.0).

## Рабочий сценарий

**Даёшь пины (или темы) → получаешь частотность запросов по США.**
Отдельно по запросу — тренды.

```bash
python -m pinterest.scripts.volume_us "ukrainian embroidery" "cross stitch pattern"
python -m pinterest.scripts.volume_us --from-config --expand   # + соседние запросы
python -m pinterest.scripts.trends_us --types=growing,seasonal # тренды, когда спросишь
```

Частотность берётся из `GET /v5/ad_accounts/{id}/keywords/metrics` —
единственного эндпоинта v5, где число запросов привязано к стране
(`country_code=US`). Значение приходит **корзиной, а не точным числом**:
`5M+`, `100K-1M`, `10K`. Для сравнения ключей между собой этого хватает, для
отчёта «столько-то показов» — нет.

`--expand` доращивает список: `/terms/related` даёт логически связанные запросы,
`/terms/suggested` — популярные продолжения, и оба меряются той же частотностью.
Так из одной темы пина вырастает готовая карта спроса.

## Что API про США даёт, а что нет

| Задача | Эндпоинт | Гео |
| --- | --- | --- |
| Частотность запроса в США | `/v5/ad_accounts/{id}/keywords/metrics` | **есть, `country_code`** |
| Соседние и подсказанные запросы | `/v5/terms/related`, `/v5/terms/suggested` | нет (глобально) |
| Что растёт в США | `/v5/trends/keywords/US/top/{growing\|monthly\|yearly\|seasonal}` | **есть, `region=US`** |
| Свои показы, клики, сохранения | `/v5/user_account/analytics`, `/analytics/top_pins`, `/v5/pins/analytics` | **нет** |
| Гео-разрез аудитории и показов | `/v5/ad_accounts/{id}/targeting_analytics` (`COUNTRY`, `GEO`, `REGION`), `/audience_insights` | есть, но по платным показам |

Ключевое: **у органической аналитики гео-разреза нет вообще.** У
`/v5/user_account/analytics` параметр `split_field` принимает только
`NO_SPLIT | APP_TYPE | OWNED_CONTENT | SOURCE | PIN_FORMAT`, у
`/v5/pins/{pin_id}/analytics` — только `NO_SPLIT | APP_TYPE`. Ни фильтра по
стране, ни сплита по гео. Разбивку «сколько показов пришло из США» Pinterest
показывает в веб-интерфейсе Business Hub, но наружу не отдаёт.

Значит США задаётся **на входе** (какие запросы брать в работу), а на выходе
доля США по своим пинам через Pinterest API не измеряется — только через GA4 на
ridnavyshyvka.com.ua по источнику `pinterest` либо через рекламный кабинет.

## Доступ

Приложение **1587527**, секрет — в `secrets/pinterest.env` (в git не попадает).

Быстрый путь, без OAuth и браузерного согласия — кнопка **«Создать маркер»** в
настройках приложения на developers.pinterest.com. Она выдаёт токен со скоупами
`pins:read, boards:read, user_accounts:read, ads:read, catalogs:read` — этого
хватает на всё выше:

```bash
python -m pinterest.scripts.login --token=<маркер>
python -m pinterest.scripts.whoami          # что реально открыто
```

Маркер живёт около 30 дней и **не обновляется** — когда истечёт, жмёшь кнопку
заново. Если нужен самообновляющийся токен, есть полный OAuth:

```bash
python -m pinterest.scripts.login           # печатает ссылку
python -m pinterest.scripts.login --code=<code>
python -m pinterest.scripts.login --refresh
```

Redirect URI берётся из `secrets/pinterest.env` и должен совпадать с одним из
зарегистрированных в приложении: `https://ridnavyshyvka.com.ua/` или
`https://vmi2948432.contaboserver.net/rest/oauth2-credential/callback`.

Третий путь, `client_credentials`, проверен 24.08.2026 и **не работает**:
Pinterest отвечает `code 1201 Two-factor authentication required` — токен
приложения выдаётся только при включённой двухфакторной аутентификации на
аккаунте-владельце. Пара app_id/secret при этом валидна (с неверным секретом
ответ другой — `code 2 Authentication failed`). Даже с 2FA этот токен не пустил
бы к `/user_account/analytics` и `/trends/*`: там по спецификации разрешён
только `pinterest_oauth2`.

## Рекламный кабинет

`keywords/metrics`, `targeting_analytics` и `audience_insights` живут под
`ad_account_id`. Кабинет заводится бесплатно на ads.pinterest.com, тратить
бюджет не обязательно. `volume_us.py` находит его сам и кэширует в
`secrets/ad_account.json`; если кабинета нет — скажет об этом прямо.

## Trial vs standard access

Пока приложение в trial access, оно работает только с аккаунтом владельца, и
часть эндпоинтов закрыта. `whoami` пробует пять эндпоинтов и печатает по
каждому OK или код ошибки — после выдачи standard access прогнать его снова и
сравнить.

## Прочие отчёты

```bash
python -m pinterest.scripts.account_report --days=30        # свои метрики
python -m pinterest.scripts.account_report --split=APP_TYPE
```

`keywords_us.json` — интересы ниши (`diy_and_crafts`, `home_decor`, `wedding`,
`womens_fashion`, `art`) и англоязычные ключи. Правится руками.

## Мелочи, о которые спотыкаются отчёты

- сегодняшний день Pinterest ещё не досчитал: `account_report` берёт окно по вчерашний;
- дни с `data_status: NOT_READY` пропускаются, чтобы не занижать средние;
- `keywords[]` режется пачками по 25 — предел Pinterest не документирует;
- 429 и 5xx клиент повторяет с паузами 2/4/8/16 с.

## Файлы

| Файл | Что |
| --- | --- |
| `pin_api/auth.py` | маркер, authorization_code, refresh, client_credentials |
| `pin_api/client.py` | GET, bookmark-пагинация, ретраи, сериализация списков |
| `scripts/login.py` | сохранение и обновление токена |
| `scripts/whoami.py` | аккаунт + карта доступных эндпоинтов |
| `scripts/volume_us.py` | **частотность запросов по США** → CSV |
| `scripts/trends_us.py` | тренды США → CSV |
| `scripts/account_report.py` | свои метрики и топ пинов → CSV |
| `keywords_us.json` | интересы и ключи ниши |

Зависимостей нет — только стандартная библиотека Python 3.10+.
