import sqlite3
import threading
import datetime
import json
import os

class ChatStore:
    """A minimal SQLite-backed chat store.

    Messages table fields:
      - id (INTEGER PRIMARY KEY)
      - user_id (TEXT)
      - session_id (TEXT)
      - role (TEXT)  # 'user' or 'assistant'
      - content (TEXT)
      - timestamp (TEXT, ISO)
    """

    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), '..', 'chat_store.db')
        # normalize path
        self.db_path = os.path.abspath(db_path)
        self._lock = threading.Lock()
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS messages (
                   id INTEGER PRIMARY KEY,
                   user_id TEXT,
                   session_id TEXT,
                   role TEXT,
                   content TEXT,
                   timestamp TEXT
               )'''
        )
        conn.commit()
        conn.close()

    def add_message(self, user_id, session_id, role, content, timestamp=None):
        """Save a message to the DB."""
        if timestamp is None:
            timestamp = datetime.datetime.utcnow().isoformat()
        with self._lock:
            conn = self._get_conn()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO messages (user_id, session_id, role, content, timestamp) VALUES (?,?,?,?,?)',
                (user_id, session_id, role, content, timestamp),
            )
            conn.commit()
            conn.close()

    def get_conversation(self, user_id, session_id=None, limit=None):
        """Retrieve messages for a user. If session_id omitted, returns all sessions' messages for the user."""
        conn = self._get_conn()
        cur = conn.cursor()
        if session_id:
            q = 'SELECT role, content, timestamp FROM messages WHERE user_id=? AND session_id=? ORDER BY id ASC'
            params = (user_id, session_id)
        else:
            q = 'SELECT role, content, timestamp FROM messages WHERE user_id=? ORDER BY id ASC'
            params = (user_id,)
        if limit:
            q = q + ' LIMIT ?'
            params = params + (limit,)
        cur.execute(q, params)
        rows = cur.fetchall()
        conn.close()
        return [{'role': r, 'content': c, 'timestamp': t} for (r, c, t) in rows]

    def export_conversation(self, user_id, session_id=None, path='export.json'):
        conv = self.get_conversation(user_id, session_id)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(conv, f, indent=2, ensure_ascii=False)
        return os.path.abspath(path)
