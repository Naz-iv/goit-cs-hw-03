import psycopg2
import os
from psycopg2 import sql
from seed import populate_db
import queries


def create_db(conn, cur):
    create_script = os.path.abspath("create_db.sql")

    if os.path.exists(create_script):
        with open(create_script, "r") as f:
            script = f.read()
        try:
            cur.execute(script)
            conn.commit()
        except psycopg2.Error as e:
            print("Error tables creation:", e)
            conn.rollback()
    else:
        print(f"File {create_script} not found.")


def main():
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432",
    )

    cursor = connection.cursor()

    create_db(connection, cursor)

    populate_db(connection, cursor)

    # Отримати всі завдання певного користувача.
    print(queries.get_tasks_by_user(cursor, 1))

    # Вибрати завдання за певним статусом.
    print(queries.get_tasks_by_status(cursor, "in progress"))

    # Оновити статус конкретного завдання.
    print(queries.update_task_status(connection, cursor, 1, "completed"))

    # Отримати список користувачів, які не мають жодного завдання.
    print(queries.get_users_without_tasks(cursor))

    # Додати нове завдання для конкретного користувача.
    print(queries.add_task(connection, cursor, "New task", "Test description", 1, 1))

    # Отримати всі завдання, які ще не завершено.
    print(queries.get_incomplete_tasks(cursor))

    # Видалити конкретне завдання.
    print(queries.delete_task(connection, cursor, 9))

    # Знайти користувачів з певною електронною поштою.
    print(queries.find_users_by_email(cursor, "example.com"))

    # Оновити ім'я користувача.
    print(queries.update_user_name(connection, cursor, 13, "New user name"))

    # Отримати кількість завдань для кожного статусу.
    print(queries.count_tasks_by_status(cursor))

    # Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти.
    print(queries.get_tasks_by_email_domain(cursor, "example.org"))

    # Отримати список завдань, що не мають опису.
    print(queries.get_tasks_without_description(cursor))

    # Вибрати користувачів та їхні завдання у статусі in progress.
    print(queries.get_users_and_tasks(cursor, "in progress"))

    # Отримати користувачів та кількість їхніх завдань.
    print(queries.get_users_with_tasks_count(cursor))

    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()
