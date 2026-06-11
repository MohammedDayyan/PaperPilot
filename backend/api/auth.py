from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.supabase_service import get_client

router = APIRouter()


class SignupRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/signup")
async def signup(request: SignupRequest):
    client = get_client()
    try:
        result = client.auth.sign_up(
            {"email": request.email, "password": request.password}
        )
        if result.user:
            return {
                "message": "Signup successful. Check your email to confirm your account.",
                "user_id": str(result.user.id),
                "email": result.user.email,
            }
        raise HTTPException(status_code=400, detail="Signup failed — no user returned")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(request: LoginRequest):
    client = get_client()
    try:
        result = client.auth.sign_in_with_password(
            {"email": request.email, "password": request.password}
        )
        if result.session:
            return {
                "access_token": result.session.access_token,
                "refresh_token": result.session.refresh_token,
                "user": {
                    "id": str(result.user.id),
                    "email": result.user.email,
                },
            }
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/logout")
async def logout():
    # Logout is client-side (clear the stored token).
    # Optionally call client.auth.sign_out() here if using server-side sessions.
    return {"message": "Logged out successfully"}
