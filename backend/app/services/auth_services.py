from datetime import datetime, timedelta
from fastapi import HTTPException, status
from jose import jwt, JWTError

from app.schemas.auth import TokenResponse
from app.utils.security import verify_password
from app.config import settings
from backend.app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, db):
        self.user_repository = UserRepository(db)

    async def login(self, nickname: str, password: str) -> TokenResponse:
        user = await self.user_repository.get_by_nickname(nickname)

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        token = self.create_access_token(
            data={
                "sub": user.nickname,
                "user_id": user.id
            }
        )

        return TokenResponse(access_token=token)

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()

        expire = datetime.utcnow() + (
            expires_delta
            if expires_delta
            else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        to_encode.update({"exp": expire})

        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )

