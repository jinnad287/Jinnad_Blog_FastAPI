from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class BlogCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)

class BlogOut(BaseModel):
    id: int
    title: str
    slug: str # slug is a URL-friendly version of the title, typically used for SEO and routing purposes
    content: str
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# blog pagination
# Pagination is a technique used to divide a large set of data into smaller,
# more manageable chunks or pages.
# It is commonly used in web applications
# to improve performance and user experience when displaying lists of items,
# such as blog posts, products, or search results. 
# Instead of loading all the data at once,
# pagination allows users to navigate through the data in smaller portions.
class PaginationParams(BaseModel):
    skip: int = Field(0, ge=0)
    limit: int = Field(10, ge=1, le=100)

class PaginatedResponse(BaseModel):
    items: list[BlogOut]
    total: int
    skip: int
    limit: int
    has_more: bool

class DeleteBlogResponse(BaseModel):
    message: str
    deleted_blog: BlogOut