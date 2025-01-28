from typing import List, Optional
from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str | list


class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    stream: Optional[bool] = False
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9
    max_tokens: Optional[int] = 8192
