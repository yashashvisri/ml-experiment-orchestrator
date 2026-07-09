from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import hash_password

from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from app.schemas.user import (
    UserCreate,
    UserLogin,
)

from app.core.security import (
    create_access_token,
    verify_password,
)


class UserService:

    @staticmethod
    def register(db: Session, data: UserCreate):
        existing = UserRepository.get_by_email(db, data.email)

        if existing:
            raise ValueError("Email already exists.")

        user = User(
            full_name=data.full_name,
            email=data.email,
            password_hash=hash_password(data.password),
        )

        return UserRepository.create(db, user)
    

    @staticmethod
    def login(db: Session, data: UserLogin):
        user = UserRepository.get_by_email(db, data.email)

        if not user:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(
            data.password,
            user.password_hash,
        ):
            raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            )

        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }