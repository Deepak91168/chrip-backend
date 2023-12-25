from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from utils.auth.token import decode_token


async def isAuthenticated(request: Request) -> bool:
    try:
        access_token = request.cookies.get("access_token")
        if access_token:
            payload = decode_token(access_token)
            return True
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized!")
    except HTTPException as e:
        raise e