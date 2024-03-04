import psycopg2
from psycopg2 import sql


# Отримати всі завдання певного користувача за його user_id
def get_tasks_by_user(cur, user_id):
    cur.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
    return cur.fetchall()


# Вибрати завдання за певним статусом
def get_tasks_by_status(cur, status):
    cur.execute(
        "SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE status_name = %s)",
        (status,),
    )
    return cur.fetchall()


# Оновити статус конкретного завдання
def update_task_status(conn, cur, task_id, new_status_name):
    try:
        cur.execute(
            "UPDATE tasks SET status_id = (SELECT id FROM status WHERE status_name = %s) WHERE id = %s",
            (new_status_name, task_id),
        )
        conn.commit()
        return "Updated"
    except psycopg2.Error as e:
        print("Error update_task_status:", e)
        conn.rollback()


# Отримати список користувачів, які не мають жодного завдання
def get_users_without_tasks(cur):
    cur.execute(
        "SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks)"
    )
    return cur.fetchall()


# Додати нове завдання для конкретного користувача
def add_task(conn, cur, title, description, status_id, user_id):
    try:
        cur.execute(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
            (title, description, status_id, user_id),
        )
        conn.commit()
        return "Added"
    except psycopg2.Error as e:
        print("Error add_task:", e)
        conn.rollback()


# Отримати всі завдання, які ще не завершено
def get_incomplete_tasks(cur):
    cur.execute(
        "SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE status_name = 'completed')"
    )
    return cur.fetchall()


# Видалити конкретне завдання
def delete_task(conn, cur, task_id):
    try:
        cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
        return "Deleted"
    except psycopg2.Error as e:
        print("Error delete_task:", e)
        conn.rollback()


# Знайти користувачів з певною електронною поштою
def find_users_by_email(cur, email_domain):
    cur.execute("SELECT * FROM users WHERE email LIKE %s", (f"%@{email_domain}",))
    return cur.fetchall()


# Оновити ім'я користувача
def update_user_name(conn, cur, user_id, new_name):
    try:
        cur.execute("UPDATE users SET fullname = %s WHERE id = %s", (new_name, user_id))
        conn.commit()
        return "Updated"
    except psycopg2.Error as e:
        print("Error update_user_name:", e)
        conn.rollback()


# Отримати кількість завдань для кожного статусу
def count_tasks_by_status(cur):
    cur.execute(
        "SELECT status_name, COUNT(*) FROM tasks JOIN status ON tasks.status_id = status.id GROUP BY status_name"
    )
    return cur.fetchall()


# Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
def get_tasks_by_email_domain(cur, email_domain):
    cur.execute(
        "SELECT tasks.* FROM tasks JOIN users ON tasks.user_id = users.id WHERE users.email LIKE %s",
        (f"%@{email_domain}",),
    )
    return cur.fetchall()


# Отримати список завдань, що не мають опису
def get_tasks_without_description(cur):
    cur.execute("SELECT * FROM tasks WHERE description IS NULL OR description = ''")
    return cur.fetchall()


# Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
def get_users_and_tasks(cur, status):
    cur.execute(
        "SELECT users.*, tasks.*, status.status_name FROM users INNER JOIN tasks ON users.id = tasks.user_id INNER JOIN status ON tasks.status_id = status.id WHERE status.status_name = %s",
        (status,),
    )
    return cur.fetchall()


# Отримати користувачів та кількість їхніх завдань
def get_users_with_tasks_count(cur):
    cur.execute(
        "SELECT users.id, users.fullname, COUNT(tasks.id) FROM users LEFT JOIN tasks ON users.id = tasks.user_id GROUP BY users.id, users.fullname"
    )
    return cur.fetchall()
