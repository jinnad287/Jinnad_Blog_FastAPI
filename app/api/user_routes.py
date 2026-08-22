from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.schemas.user import UserCreate, UserOut, TokenResponse
from app.models.user import User
from app.api.deps import get_db
from app.core.security import create_access_token, verify_password, hash_password
from app.core.logger import logger
from app.core.exceptions import ValidationException, ConflictException, AuthenticationException
from app.core.validators import PasswordValidator, EmailValidator


router = APIRouter(tags=["Authentication"])

#----------------------------User Registration-------------------------
@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    #validate email and password
    EmailValidator.validate(user_in.email)
    PasswordValidator.validate(user_in.password)

    logger.info(f"Attempting to register user: {user_in.email}")

    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        logger.warning(f"Registraion failed - email already exists: {user_in.email}")
        raise ConflictException("Email aready exists")

    try:
        user = User(
            email=user_in.email,
            hashed_password=hash_password(user_in.password)
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"User registered successfully: {user_in.email}")
        return user
    except IntegrityError as e:
        logger.error(f"Database error during registration: {str(e)}")
        raise ValidationException("Failed to register user")


# -----------------------User Login---------------------
@router.post("/login", response_model=TokenResponse)
def login(user_in: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Login attempt: {user_in.email}")

    user = db.query(User).filter(User.email == user_in.email).first()
    if not user:
        logger.warning(f"Login failed - user not found: {user_in.eamil}")
        raise AuthenticationException("Invalid email or password")

    if not verify_password(user_in.password, user.hashed_password):
        logger.warning(f"Login failed - incorrect password for: {user_in.email}")
        raise AuthenticationException("Invalid email or password")

    access_token = create_access_token(data={"user_id": user.id, "sub": user.email})
    logger.info(f"User logged in successfully: {user_in.email}")
    return TokenResponse(
        access_token=access_token, 
        token_type="bearer",
        user_id=user.id,
        email=user.email,
        role=user.role
        )


