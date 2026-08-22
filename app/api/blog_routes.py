from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
import re

from app.schemas.blog import BlogCreate, BlogOut, PaginationParams, PaginatedResponse, DeleteBlogResponse
from app.models.blog import Blog
from app.api.deps import get_db, get_current_user
from app.core.logger import logger
from app.core.exceptions import ValidationException, ConflictException, AuthenticationException, AuthorizationException


router = APIRouter(tags=["Blog"])
# generate slug
def generate_slug(title: str) -> str:
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9]', '-', slug) # remove special characters
    return slug.strip('-')


# ------------------------ Fetch all Blogs ----------------------------
@router.get("/blogs", response_model=PaginatedResponse)
def get_blogs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
    ):

        total = db.query(Blog).count()
        blogs = db.query(Blog).offset(skip).limit(limit).all()
        blog_items = [BlogOut.model_validate(blog) for blog in blogs]

        return {
              "items": blog_items,
              "total": total,
              "skip": skip,
              "limit": limit,
              "has_more": (skip+limit) < total
        }

# ---------------------------- For Creating Blog ------------------------------
@router.post("/blogs", response_model=BlogOut, status_code=status.HTTP_201_CREATED)
def create_blog(
      blog: BlogCreate,
      db: Session = Depends(get_db),
      user = Depends(get_current_user)
) -> Blog:

            if not user:
                    raise AuthenticationException("Authentication required to Create a Blog")

            slug = generate_slug(blog.title)
            new_blog = Blog(
                title=blog.title,
                content=blog.content,
                author_id=user.id,
                slug=slug
            )

            db.add(new_blog)
            try:
                db.commit()
                db.refresh(new_blog)
            except IntegrityError:
                   db.rollback()
                   logger.error(f"Blog creation failed due to slug conflict: {slug}")
                   raise ConflictException("A blog with the same title alrady exist. Please choose a different title.")

            return BlogOut.model_validate(new_blog)


# ---------------------------- Update a Blog -------------------------------
@router.put("/blogs/{blog_id}", response_model=BlogOut)
def update_blog(
       blog_id: int,
       blog: BlogCreate,
       db: Session = Depends(get_db),
       user = Depends(get_current_user)
) -> Blog:

        if not user:
                raise AuthenticationException("Authentication required to update a Blog")

        updated_blog = db.query(Blog).filter(Blog.id == blog_id).first()
        if not updated_blog:
                raise ValidationException("Blog not found")

        if updated_blog.author_id != user.id:
                raise AuthorizationException("You do not have permission to update this blog!")

        slug = generate_slug(blog.title)
        updated_blog.title = blog.title
        updated_blog.content = blog.content
        updated_blog.slug = slug

        try:
            db.commit()
            db.refresh(updated_blog)
            return updated_blog
        except IntegrityError:
            db.rollback()
            logger.error(f"Blog update failed to slug conflict: {slug}")
            raise ConflictException("A blog with the same title aleady exists. Please")

      
@router.delete("/blogs/{blog_id}", response_model=DeleteBlogResponse)
def delete_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
) -> DeleteBlogResponse:

    if not user:
        raise AuthenticationException("Authentication required to delete a Blog")

    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise ValidationException("Blog not found")

    if blog.author_id != user.id:
        raise AuthorizationException("You do not have permission to delete this blog!")

    # 1. Convert to Pydantic schema BEFORE deleting from DB
    deleted_blog_data = BlogOut.model_validate(blog)  # Use .from_orm(blog) if on Pydantic v1

    # 2. Delete and commit
    db.delete(blog)
    db.commit()

    # 3. Return response with pre-captured data
    return DeleteBlogResponse(
        message="Blog deleted successfully",
        deleted_blog=deleted_blog_data
    )
        
       


    


