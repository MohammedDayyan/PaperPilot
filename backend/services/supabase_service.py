import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def get_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # Service role for backend operations
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
    return create_client(url, key)


# ── CRUD helpers ──────────────────────────────────────────────────────────────

def insert(table: str, data: dict) -> dict:
    result = get_client().table(table).insert(data).execute()
    return result.data[0] if result.data else {}


def select(table: str, filters: dict | None = None) -> list[dict]:
    query = get_client().table(table).select("*")
    if filters:
        for key, value in filters.items():
            query = query.eq(key, value)
    result = query.execute()
    return result.data or []


def select_one(table: str, filters: dict) -> dict | None:
    rows = select(table, filters)
    return rows[0] if rows else None


def update(table: str, filters: dict, data: dict) -> dict:
    query = get_client().table(table).update(data)
    for key, value in filters.items():
        query = query.eq(key, value)
    result = query.execute()
    return result.data[0] if result.data else {}


def delete_row(table: str, filters: dict) -> None:
    query = get_client().table(table).delete()
    for key, value in filters.items():
        query = query.eq(key, value)
    query.execute()
