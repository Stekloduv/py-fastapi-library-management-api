from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.engine import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/authors/", response_model=List[schemas.Author])
def get_authors(db: Session = Depends(get_db)):
    return crud.get_authors(db)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorBaseCreate,
    db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=List[schemas.Book])
def get_books(db: Session = Depends(get_db)):
    return crud.get_books(db)


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookBaseCreate,
    db: Session = Depends(get_db),
):
    db_book = crud.get_book_by_title(db=db, title=book.title)

    if db_book is None:
        raise HTTPException(status_code=404, detail="book not found")

    return crud.create_book(db=db, book=book)
