 # Response for HTTP status codes | Status for HTTP status codes dynamic approach | HTTPException for raising an HTTP Exception | APIRouter for accessing the @app --> @router
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter

from typing import List, Optional

from .. import models, schemas, oauth2

from . .database import get_db

from sqlalchemy.orm import Session

from sqlalchemy import func # used for count() in our query


router = APIRouter(
    prefix="/posts", # prefix gives us the ability to remove "/posts" in our code --> use "/" instead
    tags=["Posts"] # tags gives us the ability to group our api requests into categories in our api documentation
)


# @router.get("/", response_model=List[schemas.PostResponse]) # from typing import List --> returns a list of posts
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = cur.execute("""SELECT * FROM posts""").fetchall()
    # return {"data": posts}
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # ?limit=# & skip=# & search=something%20something --- %20 -> means space lol
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()  
    
    """ [SAME AS BELOW] SELECT posts.*, count(votes.post_id) as likes from posts LEFT OUTER JOIN votes on posts.id = votes.post_id where posts.id = 10 group by posts.id; """
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
      
    return posts

@router.get("/{id}", response_model=schemas.PostOut) # {id} --> this {id} field represents a path paramater, in this case to a specific post id
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # id: int for validation -- numbers only | response: Response for HTTP status codes hard coded | status: Status for HTTP status codes dynamic approach
    
    # cur.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # one_post = cur.fetchone()
    # one_post = cur.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),)).fetchone()
    #  if not one_post:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            # detail=f"Post with id: {id} was not found.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id:{id} was not found."}
    # return {"post_detail": one_post}

    # one_post = db.query(models.Post).filter(models.Post.id == id).first()
    one_post = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    
    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} was not found.")
    return one_post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse) # standard convention is to use plurals like posts not post | return a 201 when creating something 
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print(post.title)
    # print(post.content)
    # print(post.published)
    # print(post.rating)
    # post_dict = post.dict()
    # post_dict['id'] = rr(1, 1000000)
    # my_posts.append(post_dict)
    
    # (%s, %s, %s) --> data santization place holders
    # new_post = cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published)).fetchone()
    # conn.commit()
    
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # return {"data:": new_post}
    
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # post: Post (class Post schema)
    # index = find_index_post(id)
    
    # updated_post = cur.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%sRETURNING * """, (post.title, post.content, post.published, str(id),)).fetchone()
    # conn.commit()
    
    # if post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    #                         detail=f"Post with id: {id} was not found.")
    # post_dict = post.dict() # convert data recieved to a python dictionary
    # post_dict['id'] = id # add the id to the dictionary
    # my_posts[index] = post_dict # replace the my_post index with the python dictionary
    # return {"data": post_query.first()}
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} was not found.")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform requested action.")
    
    post_query.update(updated_post.dict())
    db.commit()
    return post_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) # when deleting something use 204 and we do not want to return anything back except for the 204 status code
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # deleting post
    # find the index in the array that has Required ID
    # my_posts.pop(index)
    
    # deleted_post = cur.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),)).fetchone()
    # conn.commit()
    # if deleted_post.first() == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    #                         detail=f"Post with id: {id} was not found.")
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} was not found.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform requested action.")
    
    post_query.delete()
    db.commit()