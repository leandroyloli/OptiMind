import sqlite3
from contextlib import contextmanager
from typing import List, Dict, Any
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'optimind.db')

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            created_at TEXT,
            user_input TEXT,
            job_title TEXT,
            status TEXT,
            final_message TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT,
            sender TEXT,
            message TEXT,
            timestamp TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS agent_outputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT,
            agent_name TEXT,
            json_output TEXT,
            timestamp TEXT
        )''')
        conn.commit()

def insert_job(job: Dict[str, Any]):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO jobs (id, created_at, user_input, job_title, status, final_message)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (job['id'], job['created_at'], job['user_input'], job['job_title'], job['status'], job.get('final_message', '')))
        conn.commit()

def insert_conversation(job_id: str, sender: str, message: str, timestamp: str):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO conversations (job_id, sender, message, timestamp)
                     VALUES (?, ?, ?, ?)''', (job_id, sender, message, timestamp))
        conn.commit()

def insert_agent_output(job_id: str, agent_name: str, json_output: str, timestamp: str):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO agent_outputs (job_id, agent_name, json_output, timestamp)
                     VALUES (?, ?, ?, ?)''', (job_id, agent_name, json_output, timestamp))
        conn.commit()

def get_jobs() -> List[Dict[str, Any]]:
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM jobs ORDER BY created_at DESC')
        rows = c.fetchall()
        return [dict(row) for row in rows]

def get_conversations(job_id: str) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM conversations WHERE job_id = ? ORDER BY timestamp', (job_id,))
        rows = c.fetchall()
        return [dict(row) for row in rows]

def get_agent_outputs(job_id: str) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM agent_outputs WHERE job_id = ? ORDER BY timestamp', (job_id,))
        rows = c.fetchall()
        return [dict(row) for row in rows]

# Inicializa o banco ao importar
init_db() 