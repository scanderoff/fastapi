from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import func
from sqlalchemy.orm import Session, Query

from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate,
                db: Session = Depends(get_db),
                user: models.User = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=user.id, **post.dict())

    db.add(new_post)
    db.commit()
    # вернет в new_post все поля нового созданного поста из бд
    # т.к. в PostCreate можно указывать не все поля
    # id и created_at получают знач-я по умолчанию
    # обновляем инстанс поста данными, к-е установились в бд по умолчанию
    db.refresh(new_post)

    return new_post


@router.get("/", response_model=list[schemas.PostOut])
# @router.get("/")
def get_posts(limit: int = 3,
              offset: int = 0,
              search: str = "",
              db: Session = Depends(get_db),
              user: models.User = Depends(oauth2.get_current_user)):
    posts: list[models.Post] = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
            .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
            .group_by(models.Post.id)
            .filter(models.Post.title.contains(search))
            .limit(limit)
            .offset(offset)
            .all()
    )

    return posts


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int,
             db: Session = Depends(get_db),
             user: models.User = Depends(oauth2.get_current_user)):
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
            .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
            .group_by(models.Post.id)
            .filter(models.Post.id == id)
            .first()
    )

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,
                db: Session = Depends(get_db),
                user: models.User = Depends(oauth2.get_current_user)):
    post_query: Query[models.Post] = db.query(models.Post) \
        .filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist",
        )

    if post.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int,
                updated_post: schemas.PostCreate,
                db: Session = Depends(get_db),
                user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exists",
        )

    if post.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()
