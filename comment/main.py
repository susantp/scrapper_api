from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from comment.models import CreateAndUpdateComment
from comment.schemas import CommentSchema
from app.dependencies import get_database_session

router = APIRouter()


@cbv(router)
class Comments:
    db: Session = Depends(get_database_session)

    @router.get('/comment')
    def get_comments(self):
        records = self.db.execute('select * from comments')
        data = records.fetchall()
        return {'data': data}

    @router.get('/comment/{comment_id}')
    async def find_comment(self, comment_id: int):
        record = self.db.query(CommentSchema).filter(CommentSchema.id == comment_id).first()
        return {"data": record}

    @router.post('/comment')
    async def add_comment(self, comment_info: CreateAndUpdateComment):
        details = self.db.query(CommentSchema).filter(
            CommentSchema.title == comment_info.title).first()
        if details is not None:
            return {'error': 'data already there'}
        try:
            new_comment = CommentSchema(**comment_info.dict())
            self.db.add(new_comment)
            self.db.commit()
            self.db.refresh(new_comment)
            return {'data': new_comment}
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {"error": error}
