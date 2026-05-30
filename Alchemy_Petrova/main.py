from IST03_Petrova.Alchemy_Petrova.database import SessionLocal, engine, Base
from IST03_Petrova.Alchemy_Petrova.crud import *
from datetime import datetime


def main():
    # Пересоздаём таблицы, чтобы скрипт можно было запускать многократно
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Создаём сессию для работы с БД
    session = SessionLocal()

    try:
        print("Начинаем тестирование...\n")

        # 1. Создаём тестовых авторов
        print("Создаём авторов...")
        author1 = create_author(session, "Анна Петрова", "anna@example.com")
        author2 = create_author(session, "Иван Сидоров", "ivan@example.com")
        print(f"{author1.name} (id={author1.id})\n")
        print(f"{author2.name} (id={author2.id})\n")

        # 2. Создаём посты для Анны
        print("Создаём посты...")
        post1 = create_post(session, "Первый пост", "Это содержание первого поста. Оно достаточно длинное.", author1.id,
                            published=True)
        post2 = create_post(session, "Черновик", "Этот пост пока не опубликован.", author1.id, published=False)
        post3 = create_post(session, "Пост Ивана", "Текст от Ивана.", author2.id, published=True)
        print(f"'{post1.title}' (опубликован)")
        print(f"'{post2.title}' (черновик)")
        print(f"'{post3.title}' (опубликован)\n")

        # 3. Добавляем комментарии к первому посту
        print("Добавляем комментарии...")
        add_comment(session, post1.id, "Читатель1", "Отличная статья, очень полезно!")
        add_comment(session, post1.id, "Читатель2", "Спасибо за материал, жду продолжения.")
        add_comment(session, post1.id, "Аноним", "Коротко.")  # Этот комментарий тоже учтётся
        print("3 комментария добавлены к первому посту\n")

        # 4. Публикуем черновик
        print("Публикуем черновик...")
        success = update_post_status(session, post2.id, published=True)
        if success:
            print(f"'{post2.title}' теперь опубликован\n")

        # 5. Выводим все опубликованные посты
        print("Все опубликованные посты:")
        published = get_published_posts(session)
        for post in published:
            print(f"'{post.title}' — автор: {post.author.name}")
        print()

        # 6. Топ авторов по количеству постов
        print("Топ авторов по количеству постов:")
        top_authors = get_top_authors_by_posts(session, limit=3)
        for rank, (name, count) in enumerate(top_authors, 1):
            print(f"{rank}. {name}: {count} пост(ов)")
        print()

        # 7. Проверка: поиск автора по email
        print("Поиск автора по email...")
        found = get_author_by_email(session, "anna@example.com")
        if found:
            print(f"Найдено: {found.name}")
        else:
            print("Автор не найден")


#=====================
# Самостоятельная работа :)))
        # Поиск автора по имени
        found_author = fetch_author_by_name(session, "Артем Белов")
        if found_author:
            print(f"{found_author.name} ({found_author.email})\n")

        # Выводит все посты за сегодняшнюю дату
        current_date_posts = fetch_published_posts_by_date(session, datetime.utcnow().date())
        for single_post in current_date_posts:
            print(f"'Посты за сегодня: {single_post.title}' - автор: {single_post.author.name}")

        # Сразу несколько авторов
        created_authors = insert_authors_from_list(session, [
            ("Михаил Чернов", "m.chernov@example.org"),
            ("Елена Григорьева", "helen.g@inbox.ru"),
            ("Дмитрий Соколов", "dima.sokolov@mail.com")])
        for author_obj in created_authors:
            print(f"{author_obj.name} (id={author_obj.id})")

        # Пост с комментариями
        detailed_post = fetch_post_with_comments_by_id(session, first_post.id)
        if detailed_post:
            print(f"'{detailed_post.title}' - комментариев: {len(detailed_post.comments)}")
            for comment_item in detailed_post.comments:
                print(f"  - {comment_item.author_name}: {comment_item.text}")
        print()

        except Exception as error:
            print(f"Ошибка: {error}")
            session.rollback()

if __name__ == "__main__":
    main()