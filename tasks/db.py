import sqlite3
import threading
import logging
from pathlib import Path
from django.conf import settings
import datetime
import json

logger = logging.getLogger(__name__)

DB_PATH = Path(settings.DATABASES["default"]["NAME"])

_lock = threading.Lock()

def get_conn():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db_if_needed():
    with _lock:
        conn = get_conn()
        try:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date TEXT,           
                    status TEXT NOT NULL,    
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.commit()
        finally:
            conn.close()


def row_to_task(row):
    if row is None:
        return None
    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "due_date": row["due_date"],
        "status": row["status"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }

def list_tasks(limit=100, offset=0):
    init_db_if_needed()
    conn = get_conn()
    try:
        cur = conn.execute(
            "SELECT * FROM tasks ORDER BY id DESC LIMIT ? OFFSET ?", (limit, offset)
        )
        rows = cur.fetchall()
        return [row_to_task(r) for r in rows]
    finally:
        conn.close()

def create_task(title, description=None, due_date=None, status="pending"):
    init_db_if_needed()
    now = datetime.datetime.utcnow().isoformat()
    conn = get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO tasks (title, description, due_date, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
            (title, description, due_date, status, now, now),
        )
        conn.commit()
        last_id = cur.lastrowid
        return get_task(last_id)
    finally:
        conn.close()

def get_task(task_id):
    init_db_if_needed()
    conn = get_conn()
    try:
        cur = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cur.fetchone()
        return row_to_task(row)
    finally:
        conn.close()

def update_task(task_id, **fields):
    init_db_if_needed()
    allowed = {"title", "description", "due_date", "status"}
    set_parts = []
    values = []
    for k, v in fields.items():
        if k in allowed:
            set_parts.append(f"{k} = ?")
            values.append(v)
    if not set_parts:
        return get_task(task_id)
    values.append(datetime.datetime.utcnow().isoformat())
    set_clause = ", ".join(set_parts) + ", updated_at = ?"
    values.append(task_id)
    sql = f"UPDATE tasks SET {set_clause} WHERE id = ?"
    conn = get_conn()
    try:
        conn.execute(sql, tuple(values))
        conn.commit()
        return get_task(task_id)
    finally:
        conn.close()

def delete_task(task_id):
    init_db_if_needed()
    conn = get_conn()
    try:
        cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()
