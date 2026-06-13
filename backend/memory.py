from database import SessionLocal
from models import Memory


def get_memory():

    db = SessionLocal()

    memories = db.query(Memory).all()

    text = "\n".join(
        [f"{m.key}: {m.value}" for m in memories]
    )

    db.close()

    return text


def save_memory(key, value):

    db = SessionLocal()

    existing = (
        db.query(Memory)
        .filter(Memory.key == key)
        .first()
    )

    if existing:
        existing.value = value
    else:
        db.add(
            Memory(
                key=key,
                value=value
            )
        )

    db.commit()
    db.close()