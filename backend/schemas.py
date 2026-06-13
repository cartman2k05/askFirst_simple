from pydantic import BaseModel


class ChatRequest(BaseModel):
    thread_id: int
    message: str


class MemoryRequest(BaseModel):
    key: str
    value: str