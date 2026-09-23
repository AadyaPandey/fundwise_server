from typing import Any

from fastapi import FastAPI, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from graph.workflow import graph
from auth import (
    SessionLocal,
    User,
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)


app = FastAPI(
    title="Fundwise API",
    version="1.0.0",
)


# -----------------------
# CORS
# -----------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://fundwise-navy.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------
# Auth schemas
# -----------------------

class AuthRequest(BaseModel):
    username: str
    password: str


# -----------------------
# JWT authentication
# -----------------------

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        username = decode_access_token(token)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )

    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.username == username
        ).first()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found",
            )

        return user

    finally:
        db.close()


# -----------------------
# Health
# -----------------------

@app.get("/")
def health():
    return {"status": "running"}


# -----------------------
# Register
# -----------------------

@app.post("/register")
def register(data: AuthRequest):

    db = SessionLocal()

    try:
        existing_user = db.query(User).filter(
            User.username == data.username
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Username already exists",
            )

        user = User(
            username=data.username,
            password_hash=hash_password(data.password),
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return {
            "message": "User registered successfully",
            "username": user.username,
        }

    finally:
        db.close()


# -----------------------
# Login
# -----------------------

@app.post("/login")
def login(data: AuthRequest):

    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.username == data.username
        ).first()

        if not user or not verify_password(
            data.password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password",
            )

        token = create_access_token(user.username)

        return {
            "access_token": token,
            "token_type": "bearer",
        }

    finally:
        db.close()


# -----------------------
# Protected evaluate
# -----------------------

@app.post("/evaluate")
def evaluate(
    application: dict[str, Any],
    current_user: User = Depends(get_current_user),
):

    state = {
        "application": application,
        "plan": None,
        "tool_results": {},
        "review": None,
        "security_review": None,
        "worker_result": "",
        "final_decision": "",
    }

    result = graph.invoke(state)

    return jsonable_encoder(result)