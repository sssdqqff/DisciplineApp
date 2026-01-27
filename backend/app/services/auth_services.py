from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.schemas.auth import TokenResponse
from app.services.user_services import UserService
from app.utils.security import verify_password
from app.config import settings


class AuthService:
    def __init__(self, db: Session):
        self.user_service = UserService(db)

    def login(self, nickname: str, password: str) -> TokenResponse:
        user = self.user_service.user_repository.get_by_nickname(nickname)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        # создаём токен с user_id
        token = self.create_access_token({"sub": user.nickname, "user_id": user.id})
        return TokenResponse(access_token=token)

    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def get_current_user(self, token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: int = payload.get("user_id")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        # ищем пользователя по id, а не email
        user = self.user_service.user_repository.get_by_id(user_id)
        if not user:
            raise credentials_exception
        return user
