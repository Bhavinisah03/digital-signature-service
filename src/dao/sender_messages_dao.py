from sqlalchemy.orm import Session
from model.dao.SenderMessage import SenderMessage

# ✅ API to Insert Data into Existing SQLite Table
def add_sender_message(sender_message: SenderMessage, db: Session):
    print(f"Adding sender message to DB. sender_message: {sender_message}...")
    db.add(sender_message)
    db.commit()
    db.refresh(sender_message)
    print(f"Sender message added to DB. sender_message: {sender_message}...")