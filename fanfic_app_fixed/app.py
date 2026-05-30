
"""1. Пользователь регистрируется или входит через форму/Google OAuth.
2. Flask кладет минимальные данные пользователя в session.
3. Данные пользователя, избранное и фанфики хранятся в SQLAlchemy-моделях.
4. Пользователь вводит одного или нескольких персонажей.
5. Backend ищет их через TMDB search/multi (люди, фильмы, сериалы).
6. Backend отправляет найденный контекст в Mistral API.
7. Сгенерированный фанфик отображается на странице и сохраняется в историю.

Все секреты читаются из .env. В коде нет реальных API-ключей.
"""

from datetime import datetime  # штука работает со вресеменим,ставит даты на фанфиках
import os  # интрумент работает с операционкой , читаетключи
from pathlib import Path  # продвинутый инструмент для путей, помогает не путаться в слэшах файлов
import urllib.parse  # ссылки правильно собирает ,для гугла нужен

# Импортируем кучу полезностей из Flask для сборки сайта
from flask import Flask, flash, redirect, render_template, request, session, url_for
# Импортируем алхимию — главную читалку и писалку в базу данных
from flask_sqlalchemy import SQLAlchemy
import requests  # главный почтальон Питона, чтобиз инета что-то взять,  он таскает запросы на TMDB, Google и Mistral
#  чтобы хакеры ничего не украли
from werkzeug.security import check_password_hash, generate_password_hash

try:
    # Пытаемся импортировать библиотеку для чтения файлика .env с ключами
    from dotenv import load_dotenv
except ImportError:
    # Если библиотеки нет, создаём пустышку, чтобы код не падал с ошибкой
    def load_dotenv(*args, **kwargs):
        return False

# Загружаем .env именно из папки с app.py. Находим секреты и пароли.
load_dotenv(dotenv_path=Path(__file__).with_name(".env"), override=True)

app = Flask(__name__)  # создаём само веб-приложение Flask
# Читаем секретный ключ для сессий из .env, если его там нет — берём дефолтный (но это небезопасно!)
app.secret_key = os.getenv("FLASK_SECRET_KEY") or "dev-secret-change-me"

# DATABASE_URL: если пусто — SQLite; если postgresql:// — PostgreSQL.
# SQLAlchemy требует "postgresql://", некоторые хостинги дают "postgres://" —
# исправляем на лету.
_raw_db_url = os.getenv("DATABASE_URL") or ""
if _raw_db_url.startswith("postgres://"):
    # Пересобираем ссылку на базу, меняя "postgres://" на правильный "postgresql://"
    _raw_db_url = "postgresql://" + _raw_db_url[len("postgres://"):]
# Если в .env ничего нет про базу, создаём локальный файлик-базу fanfic_app.db прямо под боком
DATABASE_URI = _raw_db_url or "sqlite:///fanfic_app.db"

# Скармливаем Фласку ссылку на нашу базу данных
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
# Отключаем лишнюю слежку Алхимии за изменениями, чтобы сервер не тормозил
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# SQLAlchemy — единственный способ работы с БД в этом проекте

db = SQLAlchemy(app)  # подключаем Алхимию к нашему приложению Flask


class User(db.Model):
    """Таблица пользователей.

    Хранит как обычных пользователей (с хэшем пароля), так и вошедших
    через Google OAuth. Первичный ключ — email: удобно для учебного
    проекта и исключает дубли без отдельного UNIQUE-индекса.
    """

    __tablename__ = "users"  # задаём имя таблицы в базе данных

    email = db.Column(db.String(255), primary_key=True)  # почта
    name = db.Column(db.String(255), nullable=False)  # имя пользователя, пустому быть нельзя
    # password_hash = None для OAuth-пользователей.
    password_hash = db.Column(db.Text, nullable=True)  # зашифрованный пароль (для тех, кто зашёл без Гугла)
    google_id = db.Column(db.String(255), nullable=True)  # циферный ID от Гугла, если зашли через него
    # "password" или "google"
    auth_provider = db.Column(db.String(50), nullable=False, default="password")  # метка, как именно зашёл юзер

    #  при удалении пользователя исчезают его избранное и фанфики.
    favorites = db.relationship("Favorite", backref="user", cascade="all, delete-orphan", lazy=True)
    fanfics = db.relationship("Fanfic", backref="user", cascade="all, delete-orphan", lazy=True)


class Favorite(db.Model):
    """Избранные персонажи / персоны / фильмы пользователя."""

    __tablename__ = "favorites"  # имя таблицы для любимчиков

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # просто порядковый номер строчки
    # Почта юзера, которая связана с таблицей пользователей. Если юзера удалят — избранные  тоже сотрутся (CASCADE)
    email = db.Column(db.String(255), db.ForeignKey("users.email", ondelete="CASCADE"), nullable=False)
    # person_id — числовой идентификатор из TMDB (актёр, фильм или сериал).
    person_id = db.Column(db.Integer, nullable=False)  # ID актёра/фильма из базы киношников
    person_name = db.Column(db.String(255), nullable=False)  # как зовут актёра или как называется фильм

    # Запрещаем юзеру добавлять одного и того же персонажа в избранное дважды
    __table_args__ = (db.UniqueConstraint("email", "person_id", name="uq_favorites_email_person"),)


class Fanfic(db.Model):
    """Сгенерированные фанфики, привязанные к аккаунту."""

    __tablename__ = "fanfics"  # имя таблицы для фанфиков

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID фанфика
    # Чья история? Связываем по почте с юзером. Если юзера удалят — фанфик тоже удалится
    email = db.Column(db.String(255), db.ForeignKey("users.email", ondelete="CASCADE"), nullable=False)
    character_name = db.Column(db.String(255), nullable=False)  # про каких персонажей история
    fanfic_text = db.Column(db.Text, nullable=False)  # огромный текст самого фанфика, который написала нейросеть
    created_at = db.Column(db.String(50), nullable=False)  # дата и время создания


#Вспомогательные функции БД , ПОМООООГИИТЕ

def current_user():
    """Возвращает dict {email, name} из session или None."""
    return session.get("user")  # заглядывает в браузерные куки (сессию) и смотрит, залогинен ли кто-то


def get_user(email: str):
    """Ищет пользователя по email (без учёта регистра)."""
    return db.session.get(User, email.lower())  # стучится в базу и ищет юзера по его почте


def create_user(name: str, email: str, password: str) -> None:
    """Создаёт нового пользователя с хэшированным паролем."""
    user = User(
        email=email.lower(),  # переводим почту в нижний регистр, чтобы не было дублей типа ТЕСТ и тест
        name=name.strip(),  # срезаем лишние пробелы по краям имени
        password_hash=generate_password_hash(password),  # превращаем пароль в кашу (хэш) для безопасности
        auth_provider="password",  # пишем, что регистрация обычная
    )
    db.session.add(user)  # кладём подготовленного юзера в корзину Алхимии
    db.session.commit()  # пишем всё на жёсткий диск в базу данных


def save_google_user(email: str, name: str, google_id: str) -> None:
    """Создаёт или обновляет пользователя Google OAuth."""
    user = db.session.get(User, email.lower())  # проверяем, может этот гуглер у нас уже регистрировался?
    if user:
        user.name = name  # если есть, просто обновляем его имя
        user.google_id = google_id  # обновляем его Google ID
        user.auth_provider = "google"  # на всякий случай подтверждаем, что он зашёл через Гугл
    else:
        # Если чел у нас впервые, создаём новую строчку для него
        user = User(email=email.lower(), name=name, google_id=google_id, auth_provider="google")
        db.session.add(user)  # добавляем в корзину
    db.session.commit()  # сохраняем изменения в базу


def login_user(email: str, name: str) -> None:
    """Кладёт минимальные данные пользователя в session."""
    session["user"] = {"email": email.lower(),
                       "name": name}  # запоминаем юзера в браузере, чтобы он не вылетал со страниц


def add_favorite(email: str, person_id: int, person_name: str) -> None:
    """Добавляет персонажа в избранное (без дублей)."""
    # Ищем в базе, нет ли уже у этого чела этого конкретного ID из TMDB
    exists = Favorite.query.filter_by(email=email, person_id=person_id).first()
    if not exists:
        # Если такого ещё нет, собираем новую карточку любимчика
        fav = Favorite(email=email, person_id=person_id, person_name=person_name)
        db.session.add(fav)  # добавляем в корзину
        db.session.commit()  # сохраняем в базу данных


def get_favorites(email: str):
    """Возвращает список избранных для пользователя."""
    # Лезем в базу, вытаскиваем любимчиков юзера и сортируем их красиво по алфавиту (по имени)
    return Favorite.query.filter_by(email=email).order_by(Favorite.person_name).all()


def remove_favorite(email: str, person_id: int) -> None:
    """Удаляет запись из избранного текущего пользователя."""
    # Находим нужную карточку в базе
    fav = Favorite.query.filter_by(email=email, person_id=person_id).first()
    if fav:
        db.session.delete(fav)  # говорим Алхимии: «сотри это»
        db.session.commit()  # применяем удаление в файле базы данных


def save_fanfic(email: str, character_name: str, fanfic_text: str) -> None:
    """Сохраняет сгенерированный фанфик в историю."""
    fanfic = Fanfic(
        email=email,
        character_name=character_name,
        fanfic_text=fanfic_text,
        # Засекаем текущее время на компе и переводим в красивую строчку Год-Месяц-День Часы:Минуты
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )
    db.session.add(fanfic)  # добавляем фанфик в корзину Алхимии
    db.session.commit()  # сохраняем историю в базу


def get_fanfics(email: str):
    """Возвращает фанфики пользователя, новые сверху."""
    # Достаем фанфики юзера из базы и сортируем по ID в обратном порядке (desc), чтобы свежие были первыми
    return Fanfic.query.filter_by(email=email).order_by(Fanfic.id.desc()).all()


# ─── Парсинг ввода ─────────────────────────────────────────────────────────────

def parse_characters(raw_text: str) -> list:
    """Позволяет ввести одного или нескольких персонажей через запятую/строку."""
    names = []  # создаем пустой список для чистых имён
    # Заменяем переносы строк на запятые, а потом режем всю строку по запятым
    for chunk in raw_text.replace("\n", ",").split(","):
        name = chunk.strip()  # убираем невидимые пробелы по бокам имени
        # Если имя не пустое и мы его ещё не добавляли — закидываем в список
        if name and name not in names:
            names.append(name)
    return names[:5]  # отдаём максимум 5 персонажей, чтобы у нейросети не взорвался мозг


# ─── TMDB API ──────────────────────────────────────────────────────────────────

def _tmdb_get(path: str, params: dict) -> dict:
    """Общий GET-запрос к TMDB v3 с проверкой ключа."""
    api_key = os.getenv("TMDB_API_KEY")  # достаём ключ от кинобазы из .env
    if not api_key:
        raise RuntimeError("TMDB_API_KEY не настроен в .env")  # ругаемся, если ключ забыли положить
    # Дописываем к параметрам запроса наш ключ и просим вернуть данные на русском языке
    params = {**params, "api_key": api_key, "language": "ru-RU"}

    # КУДА ОТПРАВЛЯЕТСЯ ЗАПРОС: Запрос летит на сервер TMDB (api.themoviedb.org) на конкретный адрес (path).
    # ЧТО ЗА ОТВЕТ ПОЛУЧАЕТСЯ: Возвращается огромный JSON (словарь) со статусом 200 OK, где лежит куча инфы про кино.
    response = requests.get(f"https://api.themoviedb.org/3{path}", params=params, timeout=20)
    response.raise_for_status()  # если сервер TMDB упал или выдал ошибку, эта штука сразу прервёт код ошибкой
    return response.json()  # превращаем сырой текст ответа в питоновский словарь


def search_media(name: str) -> list:
    """Ищет персонажа через search/multi — находит людей, фильмы и сериалы."""
    # Делаем запрос к поисковику TMDB, передавая имя или название в параметре query
    data = _tmdb_get("/search/multi", {"query": name})
    normalized = []  # список для красивых, очищенных результатов

    # Перебираем первые 8 результатов из того, что прислал сервер кинобазы
    for item in data.get("results", [])[:8]:
        media_type = item.get("media_type",
                              "person")  # узнаём, кто это: человек (person), фильм (movie) или сериал (tv)

        if media_type == "person":
            # Собираем названия фильмов, по которым известен этот актёр
            titles = [
                m.get("title") or m.get("name") or m.get("original_title") or ""
                for m in item.get("known_for", [])[:4]
                if m.get("title") or m.get("name")
            ]
            # Складываем в наш список только нужные поля для шаблона
            normalized.append({
                "id": item["id"],
                "name": item.get("name", ""),
                "profile_path": item.get("profile_path"),  # ссылка на фотку актёра
                "popularity": item.get("popularity", 0),
                "known_for_titles": titles,
                "media_type": "person",
            })
        elif media_type == "movie":
            title = item.get("title") or item.get("original_title", "")
            normalized.append({
                "id": item["id"],
                "name": title,
                "profile_path": item.get("poster_path"),  # для фильмов картинка — это постер
                "popularity": item.get("popularity", 0),
                "known_for_titles": [title],
                "media_type": "movie",
                "overview": item.get("overview", ""),  # краткое описание сюжета фильма
            })
        elif media_type == "tv":
            title = item.get("name") or item.get("original_name", "")
            normalized.append({
                "id": item["id"],
                "name": title,
                "profile_path": item.get("poster_path"),  # для сериала тоже постер
                "popularity": item.get("popularity", 0),
                "known_for_titles": [title],
                "media_type": "tv",
                "overview": item.get("overview", ""),  # сюжет сериала
            })
    return normalized  # возвращаем чистенький список карточек


def get_person_movies(person_id: int) -> list:
    """Возвращает фильмографию актёра/персоны (первые 8 позиций)."""
    # Запрос улетает на /person/{id}/movie_credits. Возвращает список фильмов, где играл этот актёр.
    data = _tmdb_get(f"/person/{person_id}/movie_credits", {})
    return data.get("cast", [])[:8]  # забираем первые 8 фильмов из актёрского состава (cast)


def get_media_details(media_id: int, media_type: str) -> dict:
    """Получает детали фильма или сериала (overview, genres и т.д.)."""
    try:
        # Запрос идёт на /movie/{id} или /tv/{id}. Возвращает подробную карточку фильма/сериала.
        return _tmdb_get(f"/{media_type}/{media_id}", {})
    except Exception:
        return {}  # если что-то сломалось, возвращаем пустой словарь, чтобы сайт не падал


def get_movie_characters(movie_id: int, media_type: str = "movie") -> list:
    """Возвращает список персонажей из фильма/сериала (из credits)."""
    try:
        # Запрос летит в титры фильма/сериала. Возвращает списки актёров и их ролей.
        data = _tmdb_get(f"/{media_type}/{movie_id}/credits", {})
        cast = data.get("cast", [])[:12]  # берём первые 12 строчек из титров
        # Вытаскиваем именно имена вымышленных персонажей (поле character)
        return [c["character"] for c in cast if c.get("character")]
    except Exception:
        return []  # если упало — отдаём пустой список


def load_search_results(character_names: list) -> list:
    """Готовит данные для страницы поиска: несколько вариантов TMDB на каждый запрос."""
    results = []  # финальный мешок с результатами
    for name in character_names:
        candidates = search_media(name)  # ищем варианты в TMDB по каждому введённому имени
        # Упаковываем: что ввёл юзер + какие карточки нашлись в TMDB
        results.append({"typed_name": name, "candidates": candidates})
    return results


def parse_selected_people(selected_values: list) -> list:
    """Разбирает выбранные карточки из формы генерации."""
    selected = []  # список для разобранных данных чекбоксов
    for value in selected_values:
        # Строка из чекбокса склеина через палочку: 'id|name|typed_name|media_type'. Режем её.
        parts = value.split("|", 3)
        if len(parts) < 3:
            continue  # если данных мало, это какой-то битый чекбокс, пропускаем
        person_id, person_name, typed_name = parts[0], parts[1], parts[2]
        media_type = parts[3] if len(parts) > 3 else "person"  # если типа нет, думаем, что это актёр (person)
        if person_id.isdigit():
            # Если ID это число, переводим его в int и бережно сохраняем в словарик
            selected.append({
                "id": int(person_id),
                "name": person_name,
                "typed_name": typed_name,
                "media_type": media_type,
            })
    return selected


def load_movie_context(character_names: list, selected_people: list = None) -> list:
    """Собирает контекст из TMDB для каждого выбранного персонажа."""
    context = []  # сюда складываем весь кино-багаж для нейросети
    selected_people = selected_people or []  # если чекбоксы пустые, делаем пустой список

    if selected_people:
        # Если юзер сам отметил галочками нужных актёров/фильмы на экране
        for person in selected_people:
            media_type = person.get("media_type", "person")
            entry = {
                "typed_name": person["typed_name"],
                "found_name": person["name"],
                "media_type": media_type,
                "movies": [],
                "overview": "",
                "characters": [],
            }
            if media_type == "person":
                # Если это актёр — вытягиваем список его фильмов
                entry["movies"] = get_person_movies(person["id"])
            else:
                # Фильм или сериал: получаем описание и список персонажей.
                details = get_media_details(person["id"], media_type)
                entry["overview"] = details.get("overview", "")
                entry["characters"] = get_movie_characters(person["id"], media_type)
            context.append(entry)
        return context

    # Fallback: Если юзер не ставил галочки, берём самый первый попавшийся результат TMDB для каждого имени
    for name in character_names:
        results = search_media(name)
        entry = {
            "typed_name": name,
            "found_name": name,
            "media_type": "person",
            "movies": [],
            "overview": "",
            "characters": [],
        }
        if results:
            first = results[0]  # берём самую первую карточку из поиска
            entry["found_name"] = first["name"]
            entry["media_type"] = first["media_type"]
            if first["media_type"] == "person":
                entry["movies"] = get_person_movies(first["id"])
            else:
                details = get_media_details(first["id"], first["media_type"])
                entry["overview"] = details.get("overview", "")
                entry["characters"] = get_movie_characters(first["id"], first["media_type"])
        context.append(entry)
    return context


# ─── Mistral API ───────────────────────────────────────────────────────────────

def generate_fanfic(character_names: list, movie_context: list) -> str:
    """Генерирует фанфик через Mistral Chat Completions API."""
    api_key = os.getenv("MISTRAL_API_KEY")  # дёргаем токен Мистрали из .env
    if not api_key:
        raise RuntimeError("MISTRAL_API_KEY не настроен в .env")

    context_lines = []  # строчки контекста, которые мы скормим нейросети в промпте
    for item in movie_context:
        name = item.get("found_name") or item["typed_name"]
        media_type = item.get("media_type", "person")

        if media_type == "person":
            movies = item.get("movies", [])
            # Склеиваем названия первых 5 фильмов актёра через запятую
            titles = ", ".join(
                m.get("title") or m.get("original_title", "") for m in movies[:5] if
                m.get("title") or m.get("original_title")
            )
            context_lines.append(f"- Актёр/персонаж: {name}. Известные фильмы: {titles or 'нет данных'}")
        else:
            label = "Фильм" if media_type == "movie" else "Сериал"
            overview = item.get("overview", "")
            chars = item.get("characters", [])
            chars_str = ", ".join(chars[:6]) if chars else "нет данных"
            line = f"- {label}: «{name}»."
            if overview:
                line += f" Описание: {overview[:200]}."  # берём только первые 200 символов сюжета, чтобы не спамить нейросеть
            line += f" Персонажи: {chars_str}."
            context_lines.append(line)

    # Собираем ТЗ (промпт) для Мистрали
    prompt = (
            "Напиши короткий фанфик на русском языке на 700–1000 слов. "
            "Используй атмосферу приключения, живые диалоги и понятный финал. "
            "Используй свои знания о персонажах — TMDB-контекст ниже является лишь дополнением. "
            "Не добавляй запрещённый или взрослый контент.\n"
            f"Персонажи: {', '.join(character_names)}.\n"
            "Контекст из API фильмов:\n" + "\n".join(context_lines)
    )

    # КУДА ОТПРАВЛЯЕТСЯ ЗАПРОС: Пост-запрос (requests.post) улетает на сервера нейросети (по дефолту: https://api.mistral.ai/v1/chat/completions).
    # Мы передаем заголовок с секретным Bearer токеном и JSON-пакет: какую модель использовать, инструкции для системного промпта и сам текст задания (prompt).
    response = requests.post(
        os.getenv("MISTRAL_API_URL") or "https://api.mistral.ai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": os.getenv("MISTRAL_MODEL") or "mistral-small-latest",
            "messages": [
                {"role": "system", "content": "Ты пишешь добрые учебные фанфики по заданным персонажам."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.8,  # уровень креативности (0.8 — золотая середина, будет не скучно, но и не бред)
            "max_tokens": 1400,  # лимит на размер ответа от нейросети
        },
        timeout=60,  # ждём автора-нейросеть целую минуту, если думает дольше — обрываем связь
    )
    if not response.ok:
        # Если API Мистрали лежит или ключ забанен — выкидываем ошибку
        raise RuntimeError(f"Mistral API вернул HTTP {response.status_code}. Проверьте ключ и модель.")
    data = response.json()  # парсим ответ от нейросети из JSON формата
    try:
        # ЧТО ЗА ОТВЕТ ПОЛУЧАЕТСЯ: Нам возвращается большой словарь. Мы залезаем вглубь по ключам choices -> первый элемент [0] -> message -> content.
        # Там и лежит готовый, свежеиспечённый текст фанфика на русском языке. Очищаем его пробелы по краям с помощью .strip().
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError):
        raise RuntimeError("Mistral API вернул неожиданный формат ответа.")


# ─── Хелперы маршрутов ─────────────────────────────────────────────────────────

def require_login() -> bool:
    """Проверяет авторизацию. Если нет — flash и False."""
    if not current_user():
        flash("Сначала войдите или зарегистрируйтесь.")  # выводим плашку-предупреждение на экране
        return False  # юзер не залогинен!
    return True  # всё ок, проходи


# ─── Маршруты ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Главная страница сайта."""
    user = current_user()  # проверяем, кто зашёл на сайт
    # Отрисовываем шаблон index.html, подкидывая туда данные юзера, его избранное и 3 последних сохраненных фанфика
    return render_template(
        "index.html",
        user=user,
        favorites=get_favorites(user["email"]) if user else [],
        saved_fanfics=get_fanfics(user["email"])[:3] if user else [],
    )


@app.errorhandler(405)
def method_not_allowed(error):
    """Ловим ошибку, если кто-то ломится на страницы генерации или поиска напрямую через браузерную строку (GET)."""
    flash("Эту страницу нельзя открыть напрямую. Используйте кнопки и формы на сайте.")
    return redirect(url_for("index"))  # пинком отправляем шутника на главную страницу


@app.route("/login", methods=["GET"])
def login_page():
    """Страница входа."""
    if current_user():
        return redirect(url_for("index"))  # если юзер уже вошёл, нечего ему тут делать — шлём на главную
    return render_template("login.html")  # открываем окошко логина


@app.route("/register", methods=["GET"])
def register_page_redirect():
    """Если юзер пытается просто зайти на /register глазками — шлём его на форму логина (она общая)."""
    return redirect(url_for("login_page"))


@app.route("/register", methods=["POST"])
def register():
    """Сюда прилетают данные формы, когда нажимают кнопку 'Зарегистрироваться'."""
    name = request.form.get("name", "").strip()  # вытаскиваем имя из HTML-формы input name="name"
    email = request.form.get("email", "").strip().lower()  # достаём email из input name="email"
    password = request.form.get("password", "")  # достаём пароль из input name="password"

    # Валидация: проверяем, что всё заполнено и пароль не слишком короткий
    if not name or not email or len(password) < 6:
        flash("Укажите имя, email и пароль минимум из 6 символов.")
        return redirect(url_for("login_page"))
    if get_user(email):
        # Если в базе уже есть строка с такой почтой — ругаемся
        flash("Пользователь с таким email уже существует.")
        return redirect(url_for("login_page"))

    create_user(name, email, password)  # пишем нового юзера в базу данных (пароль захешируется внутри!)
    login_user(email, name)  # сразу авторизуем его (кладём данные в сессию куки)
    return redirect(url_for("index"))  # отправляем на главную страницу уже авторизованным


@app.route("/login", methods=["POST"])
def login():
    """Сюда прилетают данные формы, когда нажимают кнопку 'Войти'."""
    email = request.form.get("email", "").strip().lower()  # считываем почту из формы
    password = request.form.get("password", "")  # считываем пароль
    user = get_user(email)  # ищем юзера в базе по почте

    # Проверяем: есть ли юзер? Есть ли у него пароль (вдруг он гуглер)? Совпадает ли хэш пароля с тем, что ввели?
    if not user or not user.password_hash or not check_password_hash(user.password_hash, password):
        flash("Неверный email или пароль.")
        return redirect(url_for("login_page"))  # если косяк — шлём обратно на вход

    login_user(user.email, user.name)  # если всё супер — логиним юзера в сессию
    return redirect(url_for("index"))  # улетаем на главную


@app.route("/auth/google")
@app.route("/google_login")
def google_login():
    """Кнопка 'Войти через Google'."""
    client_id = os.getenv("GOOGLE_CLIENT_ID")  # берём ID нашего гугл-приложения из .env
    if not client_id:
        flash("Google OAuth не настроен: добавьте GOOGLE_CLIENT_ID в .env.")
        return redirect(url_for("login_page"))

    # Собираем обратный адрес: куда Гугл должен швырнуть юзера после успешного входа
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI") or url_for("google_callback", _external=True)
    # Настраиваем параметры для запроса к Гуглу
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",  # просим вернуть временный 'код', который мы потом обменяем на профиль
        "scope": "openid email profile",  # какие данные нам нужны от Гугла (почта и имя)
        "access_type": "online",
        "prompt": "select_account",  # заставляем Гугл всегда показывать окошко выбора аккаунта
    }
    # КУДА ОТПРАВЛЯЕТСЯ ЗАПРОС: Мы перенаправляем (redirect) самого ПОЛЬЗОВАТЕЛЯ его браузером на сервера Гугла.
    # Ссылка собирается через urllib.parse.urlencode, превращаясь в огромный адрес авторизации.
    # ЧТО ЗА ОТВЕТ ПОЛУЧАЕТСЯ: Пользователь видит красивое окно Гугла: «Приложение запрашивает доступ...». Юзер тыкает на свой аккаунт.
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}")


@app.route("/google_callback")
def google_callback():
    """Сюда Гугл возвращает пользователя из своего окна авторизации."""
    code = request.args.get("code")  # вытаскиваем из адресной строки параметр ?code=...
    if not code:
        flash("Google не вернул код авторизации.")
        return redirect(url_for("login_page"))

    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")  # секретный ключ приложения Гугл из .env
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI") or url_for("google_callback", _external=True)
    if not client_id or not client_secret:
        flash("Google OAuth не настроен: добавьте GOOGLE_CLIENT_ID и GOOGLE_CLIENT_SECRET.")
        return redirect(url_for("login_page"))

    # КУДА ОТПРАВЛЯЕТСЯ ЗАПРОС: Наш бэкенд берёт полученный код и сам тайно отправляет POST-запрос на сервера Гугла (oauth2.googleapis.com/token).
    # Мы доказываем Гуглу, что мы — это мы, передавая client_id и секретный client_secret.
    token_response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        },
        timeout=30,
    )
    if not token_response.ok:
        flash("Не удалось получить Google-токен. Проверьте OAuth-настройки.")
        return redirect(url_for("login_page"))

    # ЧТО ЗА ОТВЕТ ПОЛУЧАЕТСЯ: Гугл возвращает JSON со специальным ключом access_token (пропуском к данным юзера).
    access_token = token_response.json().get("access_token")
    if not access_token:
        flash("Google не вернул access token.")
        return redirect(url_for("login_page"))

    # КУДА ОТПРАВЛЯЕТСЯ ЗАПРОС: Наш бэкенд делает GET-запрос на googleapis.com/oauth2/v1/userinfo, приложив в заголовок Authorization: Bearer <токен>.
    # ЧТО ЗА ОТВЕТ ПОЛУЧАЕТСЯ: Гугл присылает JSON-карточку профиля: имя, фамилия, почта и аватарка юзера.
    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    if not user_info.ok:
        flash("Не удалось получить профиль Google.")
        return redirect(url_for("login_page"))

    profile = user_info.json()  # переводим JSON с данными юзера в питоновский словарь
    email = profile.get("email", "").lower()
    name = profile.get("name") or email
    if not email:
        flash("Google-профиль не содержит email.")
        return redirect(url_for("login_page"))

    save_google_user(email, name, profile.get("id", ""))  # сохраняем или обновляем гуглера в нашей базе данных
    login_user(email, name)  # закидываем его данные в сессию куки
    return redirect(url_for("index"))  # отправляем на главную, вход выполнен!


@app.route("/logout")
def logout():
    """Кнопка 'Выйти'."""
    session.clear()  # полностью очищаем браузерный мешок сессий (стираем куки юзера)
    return redirect(url_for("login_page"))  # выпроваживаем на страницу логина


@app.route("/search", methods=["GET"])
def search_page_redirect():
    """Защита от перехода на /search руками. Кидаем на главную."""
    return redirect(url_for("index"))


@app.route("/search", methods=["POST"])
def search():
    """Сюда прилетает запрос, когда юзер вводит имена персонажей в строку поиска на главной."""
    if not require_login():
        return redirect(url_for("login_page"))  # выкидываем неавторизованных

    # Вытаскиваем из инпута текст, чистим его нашей функцией parse_characters (превращаем в список до 5 штук)
    character_names = parse_characters(request.form.get("character_names", ""))
    user = current_user()
    if not character_names:
        flash("Введите хотя бы одного персонажа.")
        return redirect(url_for("index"))

    try:
        results = load_search_results(character_names)  # бежим в TMDB искать карточки кандидатов для каждого имени
    except requests.RequestException:
        flash("API фильмов временно недоступен. Попробуйте позже.")
        return redirect(url_for("index"))
    except RuntimeError as error:
        flash(str(error))  # если забыли API-ключ в .env — покажется эта ошибка
        return redirect(url_for("index"))

    # Снова рендерим главную страницу index.html, но теперь подкидываем туда результаты поиска (search_results=results)
    # Наш HTML-шаблон увидит их и развернёт красивые карточки с чекбоксами и кнопкой «Сгенерировать фанфик»
    return render_template(
        "index.html",
        user=user,
        favorites=get_favorites(user["email"]),
        saved_fanfics=get_fanfics(user["email"])[:3],
        search_query=", ".join(character_names),
        search_results=results,
    )


@app.route("/generate", methods=["GET"])
def generate_page_redirect():
    """Защита от перехода на /generate через адресную строку."""
    return redirect(url_for("index"))


@app.route("/generate", methods=["POST"])
def generate():
    """Сюда прилетает запрос, когда юзер выбрал галочками персонажей и нажал заветную кнопку генерации фанфика."""
    if not require_login():
        return redirect(url_for("login_page"))

    # Собираем список всех выбранных чекбоксов из формы (каждый чекбокс имеет имя name="selected_people")
    selected_people = parse_selected_people(request.form.getlist("selected_people"))
    character_names = parse_characters(request.form.get("character_names", ""))
    if selected_people:
        # Если юзер выбрал конкретные карточки, то имена персонажей берём строго из этих карточек!
        character_names = [p["name"] for p in selected_people]
    user = current_user()
    if not character_names:
        flash("Введите персонажей для генерации.")
        return redirect(url_for("index"))

    try:
        # 1. Собираем кино-контекст по персонажам (фильмографии актёров, сюжеты фильмов и т.д.) через TMDB
        movie_context = load_movie_context(character_names, selected_people)
        # 2. Отправляем промпт и контекст в Mistral API и ждём, пока нейросеть напишет рассказ
        fanfic = generate_fanfic(character_names, movie_context)
    except requests.RequestException:
        flash("Внешний API временно недоступен. Попробуйте позже.")
        return redirect(url_for("index"))
    except RuntimeError as error:
        flash(str(error))
        return redirect(url_for("index"))

    character_label = ", ".join(character_names)  # склеиваем имена героев через запятую для красивой метки
    save_fanfic(user["email"], character_label, fanfic)  # сохраняем этот шедевр в базу данных истории фанфиков

    # Снова открываем index.html, но передаём туда fanfic_result=fanfic. HTML-код увидит это и выведет готовый текст на экран.
    return render_template(
        "index.html",
        user=user,
        favorites=get_favorites(user["email"]),
        saved_fanfics=get_fanfics(user["email"])[:3],
        search_query=character_label,
        search_results=None,  # прячем карточки поиска, они больше не нужны
        fanfic_result=fanfic,  # передаём текст фанфика
        fanfic_character=character_label,  # передаём строку с героями фанфика
    )


@app.route("/favorite/add/<int:person_id>/<path:person_name>")
def add_favorite_route(person_id, person_name):
    """Быстрый маршрут (ссылка-кнопка) для добавления персонажа/актера в избранное."""
    if not require_login():
        return redirect(url_for("login_page"))
    # Вызываем нашу функцию, передавая почту текущего юзера, ID и имя из ссылки
    add_favorite(current_user()["email"], person_id, person_name)
    return redirect(url_for("index"))  # перезагружаем страницу, вернув на главную


@app.route("/favorite/remove/<int:person_id>")
def remove_favorite_route(person_id):
    """Маршрут для удаления персонажа из сердечек (избранного)."""
    if not require_login():
        return redirect(url_for("login_page"))
    remove_favorite(current_user()["email"], person_id)  # стираем запись из базы
    return redirect(url_for("index"))  # возвращаем юзера на главную


@app.route("/my-fanfics")
def my_fanfics():
    """Страница 'Моя библиотека' — где лежит вообще вся история сгенерированных фанфиков юзера."""
    if not require_login():
        return redirect(url_for("login_page"))
    user = current_user()
    # Отрисовываем отдельный шаблон fanfic.html, передавая туда ПОЛНЫЙ список фанфиков юзера из базы
    return render_template("fanfic.html", user=user, saved_fanfics=get_fanfics(user["email"]))


# Создаём таблицы при первом старте (SQLAlchemy делает это безопасно через IF NOT EXISTS).
# Заходим в контекст приложения Flask, чтобы Алхимия знала, к какому приложению она привязана
with app.app_context():
    db.create_all()  # Создаёт файлы таблиц и колонок в базе данных, если их ещё нет на диске

if __name__ == "__main__":
    # Если мы запускаем этот файл напрямую руками, стартуем встроенный веб-сервер Flask.
    # Проверяем переменную FLASK_DEBUG из .env: если там "1", включаем автоперезагрузку кода при изменениях
    app.run(debug=os.getenv("FLASK_DEBUG", "1") == "1")

