from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import jwt

from app.database import get_db
from app.models import User
from app.schemas import RegisterIn, UserOut, TokenOut
from app.security import hash_password, verify_password, create_token, decode_token

router = APIRouter(tags=["auth"])
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register", response_model=UserOut)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email already registered")
    user = User(name=data.name, email=data.email,
                hashed_password=hash_password(data.password))
    db.add(user); db.commit(); db.refresh(user)
    return user

@router.post("/login", response_model=TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "Wrong email or password")
    return {"access_token": create_token(user.id)}

def get_current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)):
    try:
        user_id = int(decode_token(token)["sub"])
    except jwt.PyJWTError:
        raise HTTPException(401, "Invalid or expired token")
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(401, "User not found")
    return user

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user