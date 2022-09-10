from email.policy import HTTP
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session, Query

from .. import schemas, database, models, oauth2

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote,
         db: Session = Depends(database.get_db),
         user: models.User = Depends(oauth2.get_current_user)):
    post: models.Post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} doesn't exist",
        )

    vote_query: Query[models.Vote] = db.query(models.Vote) \
        .filter(models.Vote.post_id == vote.post_id,
                models.Vote.user_id == user.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {user.id} has already voted on post {vote.post_id}",
            )
        
        new_vote = models.Vote(post_id=vote.post_id, user_id=user.id)

        db.add(new_vote)
        db.commit()

        return {
            "message": "Successfully added vote",
        }
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote doesn't exist",
            )
        
        vote_query.delete(synchronize_session=False)

        db.commit()

        return {
            "message": "Successfully deleted vote",
        }
