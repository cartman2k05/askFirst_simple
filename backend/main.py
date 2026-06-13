import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from database import SessionLocal

from models import Base
from models import Thread
from models import Message

from schemas import ChatRequest
from schemas import MemoryRequest

from llm import ask_llm
from memory import get_memory
from memory import save_memory

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/threads")
def create_thread():

    db = SessionLocal()

    thread = Thread(title="New Chat")

    db.add(thread)

    db.commit()
    db.refresh(thread)

    db.close()

    return thread


@app.get("/threads")
def get_threads():

    db = SessionLocal()

    data = db.query(Thread).all()

    result = [
        {
            "id": t.id,
            "title": t.title
        }
        for t in data
    ]

    db.close()

    return result


@app.delete("/threads/{thread_id}")
def delete_thread(thread_id: int):

    db = SessionLocal()

    thread = (
        db.query(Thread)
        .filter(Thread.id == thread_id)
        .first()
    )

    if thread:
        db.delete(thread)
        db.commit()

    db.close()

    return {"success": True}


@app.get("/threads/{thread_id}")
def get_messages(thread_id: int):

    db = SessionLocal()

    msgs = (
        db.query(Message)
        .filter(Message.thread_id == thread_id)
        .all()
    )

    result = [
        {
            "role": m.role,
            "content": m.content
        }
        for m in msgs
    ]

    db.close()

    return result


@app.post("/memory")
def add_memory(req: MemoryRequest):

    save_memory(
        req.key,
        req.value
    )

    return {"success": True}


@app.post("/chat")
def chat(req: ChatRequest):

    db = SessionLocal()

    db.add(
        Message(
            thread_id=req.thread_id,
            role="user",
            content=req.message
        )
    )

    db.commit()

    messages = (
        db.query(Message)
        .filter(
            Message.thread_id == req.thread_id
        )
        .all()
    )

    history = [
        {
            "role": m.role,
            "content": m.content
        }
        for m in messages
    ]

    memory = get_memory()

    answer = ask_llm(
        history,
        memory
    )

    db.add(
        Message(
            thread_id=req.thread_id,
            role="assistant",
            content=answer
        )
    )

    db.commit()

    db.close()

    return {
        "response": answer
    }