"""
Shared dependency: extract and validate the authenticated user_id from the
Authorization: Bearer <token> header.
"""
from fastapi import Header, HTTPException
from typing import Optional
from services.supabase_service import get_client


def get_user_id(authorization: Optional[str] = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ", 1)[1]
    client = get_client()
    try:
        user_response = client.auth.get_user(token)
        return str(user_response.user.id)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
