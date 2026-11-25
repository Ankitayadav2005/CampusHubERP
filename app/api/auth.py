
import os
import hashlib
import secrets
import smtplib

from datetime import datetime, timedelta, timezone
from email.message import EmailMessage

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import User


router = APIRouter(prefix="/auth", tags=["Authentication"])


# Password hashing
def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)

    password_hash = hashlib.scrypt(
        password.encode("utf-8"),
        salt=bytes.fromhex(salt),
        n=16384,
        r=8,
        p=1
    ).hex()

    return f"{salt}${password_hash}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt, original_hash = stored_hash.split("$")

        new_hash = hashlib.scrypt(
            password.encode("utf-8"),
            salt=bytes.fromhex(salt),
            n=16384,
            r=8,
            p=1
        ).hex()

        return secrets.compare_digest(new_hash, original_hash)

    except (ValueError, TypeError):
        return False


# Request models
class RegisterData(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginData(BaseModel):
    email: EmailStr
    password: str


class ForgotPasswordData(BaseModel):
    email: EmailStr


class ResetPasswordData(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


# Send password reset email
def send_reset_email(email: str, token: str):
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_APP_PASSWORD")
    base_url = os.getenv("APP_BASE_URL", "http://127.0.0.1:8000")

    if not smtp_email or not smtp_password:
        raise RuntimeError("Gmail SMTP settings are not configured.")

    reset_link = f"{base_url}/?token={token}"

    message = EmailMessage()
    message["Subject"] = "CampusHub ERP - Password Reset"
    message["From"] = smtp_email
    message["To"] = email

    message.set_content(
        f"""Hello,

We received a request to reset your CampusHub ERP password.

Open this link to reset your password:
{reset_link}

This link expires in 15 minutes.

If you did not request this, ignore this email.
"""
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(smtp_email, smtp_password)
        server.send_message(message)


# Registration
@router.post("/register")
def register(data: RegisterData, db: Session = Depends(get_db)):

    email = str(data.email).lower()

    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email is already registered."
        )

    user = User(
        name=data.name.strip(),
        email=email,
        password_hash=hash_password(data.password)
    )

    db.add(user)
    db.commit()

    return {"message": "Registration successful. Please login."}


# Login
@router.post("/login")
def login(
    data: LoginData,
    request: Request,
    db: Session = Depends(get_db)
):

    email = str(data.email).lower()

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user or not verify_password(
        data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    request.session.clear()
    request.session["user_id"] = user.id

    return {
        "message": "Login successful.",
        "name": user.name,
        "email": user.email
    }


# Current logged-in user
@router.get("/me")
def current_user(
    request: Request,
    db: Session = Depends(get_db)
):

    user_id = request.session.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Please login first."
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        request.session.clear()
        raise HTTPException(
            status_code=401,
            detail="Please login first."
        )

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }


# Logout
@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out successfully."}


# Forgot password
@router.post("/forgot-password")
def forgot_password(
    data: ForgotPasswordData,
    db: Session = Depends(get_db)
):

    email = str(data.email).lower()

    user = db.query(User).filter(
        User.email == email
    ).first()

    generic_message = (
        "If this email is registered, a password reset link will be sent."
    )

    if not user:
        return {"message": generic_message}

    token = secrets.token_urlsafe(32)

    user.reset_token_hash = hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()

    user.reset_token_expiry = (
        datetime.now(timezone.utc) + timedelta(minutes=15)
    )

    db.commit()

    try:
        send_reset_email(user.email, token)
    except Exception:
        user.reset_token_hash = None
        user.reset_token_expiry = None
        db.commit()

        raise HTTPException(
            status_code=503,
            detail="Email could not be sent. Please check Gmail settings."
        )

    return {"message": generic_message}


# Reset password
@router.post("/reset-password")
def reset_password(
    data: ResetPasswordData,
    db: Session = Depends(get_db)
):

    token_hash = hashlib.sha256(
        data.token.encode("utf-8")
    ).hexdigest()

    user = db.query(User).filter(
        User.reset_token_hash == token_hash
    ).first()

    if not user or not user.reset_token_expiry:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset link."
        )

    expiry = user.reset_token_expiry

    if expiry.tzinfo is None:
        expiry = expiry.replace(tzinfo=timezone.utc)

    if datetime.now(timezone.utc) > expiry:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset link."
        )

    user.password_hash = hash_password(data.new_password)
    user.reset_token_hash = None
    user.reset_token_expiry = None

    db.commit()

    return {"message": "Password reset successful. Please login."}
