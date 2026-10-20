# Sonya
**Sonya**: **S**can, **O**bserve, **N**otice, **Y**ield, **A**rchive.

Sonya собирает ссылки на Telegram-каналы с TGStat, проверяет доступность каналов и извлекает ссылки из их сообщений.



## Возможности

- Сбор ссылок на каналы из раздела TGStat и сохранение их в PostgreSQL.
- Проверка каналов через Telegram Web. HTML сообщений сохраняется в `src/sonya/storage/html/`.
- Каналы, для которых не удалось получить сообщения (в том числе из-за таймаута), помечаются в базе как приватные.
- Обработка сохранённых HTML-файлов и сохранение результатов в `src/sonya/storage/json/`.

## Требования

- Python 3.13 или новее.
- [uv](https://docs.astral.sh/uv/getting-started/installation/) для установки зависимостей и запуска проекта.
- PostgreSQL.
- Google Chrome для команды проверки Telegram-каналов.

## Установка

Склонируйте репозиторий и перейдите в его папку:

```powershell
git clone https://github.com/danilnizamov21/sonya.git
cd sonya
```

Установите зависимости проекта:

```powershell
uv sync
```

### Настройка базы данных

Создайте в PostgreSQL базу данных `sonya_db` (или укажите другое имя в строке подключения). Затем задайте строку подключения SQLAlchemy в `src/sonya/database/session.py`, в переменной `DATABASE_URL`. Например:

```python
DATABASE_URL = "postgresql+psycopg://USER:PASSWORD@localhost:5432/sonya_db"
```

Замените `USER` и `PASSWORD` на данные пользователя PostgreSQL. Не сохраняйте реальные пароли в публичном репозитории.

Создайте таблицы:

```powershell
uv run python -m sonya.database.init_db
```

## Использование

Посмотреть список команд и доступных параметров:

```powershell
uv run sonya --help
```

### Собрать каналы из TGStat

Вместо `gambling` укажите раздел TGStat:

```powershell
uv run sonya tgstat gambling
```

Команда добавляет найденные URL в таблицу каналов. Уже существующие каналы повторно не добавляются.

### Проверить Telegram-каналы

```powershell
uv run sonya telegram
```

По умолчанию проверяются до 20 каналов за запуск, партиями по 10. Можно изменить эти значения:

```powershell
uv run sonya telegram --limit 50 --batch-size 5
```

- `--limit` (`-l`) — максимальное количество каналов для проверки.
- `--batch-size` (`-b`) — количество каналов в одной партии.

Проверяются каналы, которые ещё не помечены приватными. HTML сообщений сохраняется в `src/sonya/storage/html/`, а статус проверки и дата записываются в базу данных.

### Обработать сохранённые сообщения

```powershell
uv run sonya pars
```

Команда обрабатывает HTML-файлы из `src/sonya/storage/html/` и сохраняет результаты в JSON-файлы в `src/sonya/storage/json/`.

## Примечания

- Команды `tgstat` и `telegram` требуют доступную базу PostgreSQL с созданными таблицами.
- Проверка каналов запускает установленный Google Chrome и сохраняет его профиль в `src/sonya/collectors/telegram/telegram_profile/`.
- Сбор данных с TGStat использует профиль Camoufox в `src/sonya/collectors/tg_stat/camoufox_profile/`.
- Сейчас получение следующих страниц TGStat настроено на путь `/gambling`; пагинация для других разделов может потребовать дополнительной настройки.
