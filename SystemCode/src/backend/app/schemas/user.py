from typing import Optional

from pydantic import BaseModel


class LoginParms(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    token: str


class RegisterParams(BaseModel):
    username: str
    email: str
    password: str


class RegisterResponse(BaseModel):
    token: str


class UserParams(BaseModel):
    id: int
    email: str
    username: str
    last_chat_session_id: int


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    last_chat_session_id: int
