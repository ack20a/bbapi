from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from api.config import get_settings

settings = get_settings()
APP_SECRET = settings.APP_SECRET
security = HTTPBearer()

def verify_app_secret(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != APP_SECRET:
        raise HTTPException(status_code=403, detail="Invalid APP_SECRET")
    return credentials.credentials
