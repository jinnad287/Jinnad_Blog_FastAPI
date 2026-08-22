from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# when a user logs in,
# we return a token response that includes the access token and user information
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")
    user_id: int
    email: EmailStr
    role: str