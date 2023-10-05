import uuid
from datetime import datetime, timedelta

import ezcord


class DashboardDB(ezcord.DBHandler):
    def __init__(self):
        super().__init__("dashboard.db")

    async def setup(self):
        await self.exec(
            """CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT UNIQUE,
            token TEXT,
            refresh_token TEXT,
            token_expires_at TIMESTAMP,
            user_id INTEGER PRIMARY KEY,
            user_email TEXT
            )"""
        )

    async def add_session(self, token, refresh_token, expires_in, user_id, user_email):
        session_id = str(uuid.uuid4())
        expires = datetime.now() + timedelta(seconds=expires_in)

        await self.exec(
            """INSERT OR REPLACE INTO sessions (session_id, token, refresh_token, token_expires_at, user_id, user_email)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (session_id, token, refresh_token, expires, user_id, user_email),
        )
        return session_id

    async def get_session(self, session_id):
        return await self.one(
            "SELECT token, refresh_token, token_expires_at, user_id, user_email FROM sessions WHERE session_id = ?",
            session_id,
            detect_types=1
        )


db = DashboardDB()