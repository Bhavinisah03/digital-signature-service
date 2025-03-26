from sqlalchemy.orm import Session
from model.dao.AuthorMessage import AuthorMessage

# ✅ API to Insert Data into Existing SQLite Table
def add_author_message(author_message: AuthorMessage, db: Session):
    print(f"Adding author message to DB. author_message: {author_message}...")
    db.add(author_message)
    db.commit()
    db.refresh(author_message)
    print(f"Author message added to DB. author_message: {author_message}...")