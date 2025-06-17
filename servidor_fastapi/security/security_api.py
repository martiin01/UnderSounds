from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from model.extra.extra_models import TokenModel
import jwt
import os

bearer_auth = HTTPBearer(auto_error=True)
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"

def get_token_BearerAuth(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_auth),
) -> TokenModel:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("uid")   # ← ahora lee uid
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: no contiene uid",
            )
        return TokenModel(sub=user_id)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar el token",
        )

