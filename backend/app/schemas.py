from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str