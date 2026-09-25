from typing import AsyncGenerator
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.core.security import decode_access_token
from app.core.exceptions import CredentialsException
from app.db.session import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise CredentialsException("Invalid authentication token or token expired")
    
    user_id_str: str = payload.get("sub")
    if not user_id_str:
        raise CredentialsException("Token payload missing subject")
    
    try:
        user_id = int(user_id_str)
    except ValueError:
        raise CredentialsException("Invalid user ID in token")
        
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise CredentialsException("User account not found")
        
    return user
