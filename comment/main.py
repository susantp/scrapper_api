from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.dependencies import get_database_session
from comment.models import CreateAndUpdateComment
from comment.schemas import CommentSchema

router = APIRouter()
DatabaseSession = Annotated[Session, Depends(get_database_session)]


@router.get("/comment")
def get_comments(db: DatabaseSession):
    records = db.execute(text("SELECT * FROM comments")).mappings().all()
    return {"data": records}


@router.get("/comment/{comment_id}")
def find_comment(comment_id: int, db: DatabaseSession):
    record = db.query(CommentSchema).filter(CommentSchema.id == comment_id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"data": record}


@router.post("/comment")
def add_comment(
    comment_info: CreateAndUpdateComment,
    db: DatabaseSession,
):
    details = (
        db.query(CommentSchema)
        .filter(CommentSchema.title == comment_info.title)
        .first()
    )
    if details is not None:
        raise HTTPException(status_code=409, detail="Comment title already exists")

    try:
        new_comment = CommentSchema(**comment_info.model_dump())
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return {"data": new_comment}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to save comment")
