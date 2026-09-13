from pydantic import BaseModel, ConfigDict


class CreateAndUpdateComment(BaseModel):
    title: str
    body: str


class CommentModel(CreateAndUpdateComment):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PaginatedCommentInfo(BaseModel):
    limit: int
    offset: int
    data: list[CommentModel]
