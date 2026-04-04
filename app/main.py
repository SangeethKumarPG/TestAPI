from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blog API with FastAPI",
    description="Sample REST API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

@app.post("/posts/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED, tags=["Posts"])
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """
    Create a new blog post.
    """
    return crud.create_post(db=db, post=post)

@app.get("/posts/", response_model=List[schemas.Post], tags=["Posts"])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of blog posts with optional pagination.
    """
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts

@app.get("/posts/{post_id}", response_model=schemas.Post, tags=["Posts"])
def read_post(post_id: int, db: Session = Depends(get_db)):
    """
    Retrieve details of a specific blog post by its ID.
    """
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.put("/posts/{post_id}", response_model=schemas.Post, tags=["Posts"])
def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    """
    Update a specific blog post partially or completely.
    """
    db_post = crud.update_post(db, post_id=post_id, post=post)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Posts"])
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific blog post.
    """
    db_post = crud.delete_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
