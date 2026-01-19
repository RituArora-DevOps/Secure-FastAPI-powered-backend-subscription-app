# Routers = application layer (entry point for API requests)
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError

from ..database.models.user import User

from ..utils import verify_password
from ..crud.users import get_user_by_email
from ..database.schemas.token import Token
from ..database import connection
from sqlalchemy.orm import Session
from ..crud import users as user_crud

# Initialize a router for authentication routes
router = APIRouter(prefix="/auth", tags=["auth"])

# --- JWT Configuration ---
load_dotenv()  # Load environment variables from .env file

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# OAuth2 scheme for token extraction from requests
# This tells FastAPI: When a route requires authentication, I expect a Bearer Token in the HTTP header.
# Example header--> Authorization: Bearer <token>
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

# --- Token create function ---
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create a JWT token.
    Args:
        data (dict): The data to encode in the token.
        expires_delta (timedelta | None, optional): Expiration time for the token. Defaults to None.
    Returns:
        str: The encoded JWT token as a string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    
# --- Login Route ---
@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(connection.get_db)
    ):
    """Login route to authenticate users and provide JWT tokens.
    Args:
        form_data (OAuth2PasswordRequestForm, optional): Form data containing username and password. Defaults to Depends().
        db (Session, optional): Database session. Defaults to Depends(connection.get_db).
    Returns:
        Token: A Pydantic model containing the access token and token type.
    """
    # 1. Get user by email and verify password
    user = user_crud.get_user_by_email(db, form_data.username)

    # 2. verify credentials
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Create JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    # 4. Return token
    return {"access_token": access_token, "token_type": "bearer"}


# --- Current user dependency ---
# Validates and extracts user info from JWT token
def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(connection.get_db)):
    """Dependency to get the current user from the JWT token.
    Args:
        token (str, optional): The JWT token. Defaults to Depends(OAuth2PasswordRequestForm).
    Raises:
        HTTPException: If the token is invalid or expired.
    Returns:
        str: The username extracted from the token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user # If all good -> current user object is returned and injected into route dependencies

# --- Protected route example ---
@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    """Protected route to get the current user's information.
    Args:
        current_user (str, optional): The current user extracted from the token. Defaults to Depends(get_current_user).
        FastAPI sees 'Depends', pause the route and run get_current_user first!
    Returns:
        dict: A dictionary containing the current user's username.
    """
    return {"email": current_user.email}

def get_current_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="The user does not have enough privileges"
        )
    return current_user

"""
Final Flow in Steps

User logs in → /auth/login

Server verifies email + password

Server issues JWT (contains sub = email, exp = expiry)

Client saves token (usually in localStorage / cookies / memory)

Client makes API requests with header Authorization: Bearer <token>

Server checks token with get_current_user

If valid → gives access, else → 401
"""