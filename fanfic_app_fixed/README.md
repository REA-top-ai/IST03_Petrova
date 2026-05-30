# Fanfic App

Учебный Flask-сервис: регистрация, обычный вход, Google OAuth, поиск персон через TMDB и генерация фанфика через Mistral API.

## Запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Заполните `.env`, затем запустите:

```bash
flask --app app run
```

Откройте: http://127.0.0.1:5000

## Переменные окружения

- `FLASK_SECRET_KEY` - секрет Flask-сессий.
- `FLASK_DEBUG` - `1` для режима разработки.
- `DATABASE_URL` - строка подключения PostgreSQL. Если пусто, используется SQLite `fanfic_app.db`.
- `TMDB_API_KEY` - ключ TMDB API для поиска персон и фильмов.
- `MISTRAL_API_KEY` - ключ Mistral API для генерации фанфика.
- `MISTRAL_MODEL` - модель Mistral, по умолчанию `mistral-small-latest`.
- `MISTRAL_API_URL` - endpoint Mistral Chat Completions.
- `GOOGLE_CLIENT_ID` - client id Google OAuth.
- `GOOGLE_CLIENT_SECRET` - client secret Google OAuth.
- `GOOGLE_REDIRECT_URI` - redirect URI, например `http://127.0.0.1:5000/google_callback`.

## PostgreSQL

Самый простой вариант:

```bash
createdb fanfic_app
```

В `.env`:

```bash
DATABASE_URL=postgresql://postgres:password@localhost:5432/fanfic_app
```

Если PostgreSQL не нужен для локальной демонстрации, оставьте `DATABASE_URL` пустым: приложение автоматически создаст SQLite-базу.

## Что умеет сервис

- Регистрация пользователя с хэшированием пароля.
- Вход по email и паролю.
- Google OAuth, если заполнены Google-переменные.
- Поиск одного или нескольких персонажей через TMDB.
- Добавление найденных персон в избранное.
- Генерация фанфика через Mistral и сохранение истории в БД.
- Просмотр сохраненных фанфиков.
