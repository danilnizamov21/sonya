# Sonya

Проект для сбора ссылок на Telegram-каналы с TGStat и проверки каналов.

## Требования

- Python 3.13 или новее
- uv
- PostgreSQL

## Установка

```bash
uv sync
```

Перед запуском настройте подключение к PostgreSQL в `src/sonya/database/session.py`.

## Запуск

```bash
uv run python -m sonya.orchestrator
```