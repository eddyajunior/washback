from jose import JWTError, jwt

from fastapi import Depends, status
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from app.core.config import settings
from app.core.exceptions import BusinessException

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    credentials_exception = BusinessException(
        "Token inválido",
        status.HTTP_401_UNAUTHORIZED
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        email = payload.get("sub")

        company_id = payload.get("company_id")

        if email is None:
            raise credentials_exception

        return {
            "email": email,
            "company_id": company_id
        }

    except JWTError:
        raise credentials_exception