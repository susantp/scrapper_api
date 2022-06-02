from typing import List

from pydantic import BaseModel


class CreateAndUpdateComment(BaseModel):
    title: str
    body: str


class CommentModel(CreateAndUpdateComment):
    id: int

    class Config:
        orm_mode = True


class PaginatedCommentInfo(BaseModel):
    limit: int
    offset: int
    data: List[CommentModel]
