from .database import get_connection


def task_from_row(row):
    return {
        "id": row[0],
        "title": row[1],
        "done": bool(row[2])
    }


# READ ALL
def get_all_tasks():
    conn = get_connection()

    rows = conn.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    conn.close()

    return [task_from_row(row) for row in rows]


# READ ONE
def get_task_by_id(task_id: int):
    conn = get_connection()

    row = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    conn.close()

    if row is None:
        return None

    return task_from_row(row)


# CREATE
def create_task(title: str):
    conn = get_connection()

    cursor = conn.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (title, 0)
    )

    conn.commit()

    new_id = cursor.lastrowid

    row = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (new_id,)
    ).fetchone()

    conn.close()

    return task_from_row(row)


# UPDATE
def update_task(task_id: int, title: str | None, done: bool | None):
    conn = get_connection()

    existing = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if existing is None:
        conn.close()
        return None

    current_title = existing[1]
    current_done = existing[2]

    if title is not None:
        current_title = title

    if done is not None:
        current_done = int(done)

    conn.execute(
        """
        UPDATE tasks
        SET title = ?, done = ?
        WHERE id = ?
        """,
        (current_title, current_done, task_id)
    )

    conn.commit()

    row = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    conn.close()

    return task_from_row(row)


# DELETE
def delete_task(task_id: int):
    conn = get_connection()

    existing = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if existing is None:
        conn.close()
        return False

    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()

    return True