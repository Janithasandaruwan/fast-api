from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=['Posts'])

#Get method
@router.get("/", response_model= List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip:int = 0, search: Optional[str] = ""):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()

    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    #Query parameters limit, skip, search
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results


#Get post with specific id
@router.get("/{id}", response_model= schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    # #post = find_post(id)
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} not found"}

    # if post.owner_id != current_user.id:
    #     return HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")
    return post


#Post method
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # # use this %s placeholders avoid from errors if user gives input data with SQL commands
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s ) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # # push changes to the database
    # conn.commit()
    # # post_dict = post.dict()
    # # post_dict["id"] = randrange(0, 10000000)
    # # my_post.append(post_dict)
    #new_post = models.Post(title=post.title, content=post.content, published= post.published)
    new_post = models.Post(**post.dict(), owner_id =current_user.id)
    db.add(new_post) #Add post to the database
    db.commit() #Make changes in the database
    db.refresh(new_post) #Store back in to the variable post


    #Pydentic orm_mode will tell the pydentic model to read the data even if it is not a dict, but an ORM model
    return new_post


#Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # #index = find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not existing!")

    if post.owner_id != current_user.id:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    #my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#Update post
@router.put("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # #index = find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not existing!")

    if post.owner_id != current_user.id:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")


    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_post[index] = post_dict
    return post_query.first()