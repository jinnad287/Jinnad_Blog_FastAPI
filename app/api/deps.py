from fastapi import Depends
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.core.config import settings
from app.core.security import outh2_scheme
from app.database.session import SessionLocal
from app.models.user import User
from app.core.exceptions import AuthenticationException
from app.core.logger import logger

# Dependency to get the database session
# working of this function is: 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency to get the current authenticated user
def get_current_user(
        token: str = Depends(outh2_scheme),
        db: Session = Depends(get_db)
    ) -> User:
    
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
            )
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise AuthenticationException("Invalid token: user ID not found")
    except JWTError as e:
        logger.error(f"JWTError: {str(e)}")
        raise AuthenticationException("Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise AuthenticationException("User not found")

    logger.info(f"Authenticated user: {user.email} (ID: {user.id})")
    return user

