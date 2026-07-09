from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:

    @staticmethod
    def register(db, data):
        existing = UserRepository.get_by_email(
            db,
            data.email,
        )

        if existing:
            raise ValueError("Email already exists.")

        user = User(
            full_name=data.full_name,
            email=data.email,
            password_hash=data.password,   # Temporary
        )

        return UserRepository.create(db, user)