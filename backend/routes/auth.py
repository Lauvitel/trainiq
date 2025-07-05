from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from db.database import SessionLocal
from schemas.user import UserCreate, Token, TokenData, UserOut
from models.user import User
from utils import jwt as jwt_utils
from core.config import settings
from passlib.context import CryptContext
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Utils ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# --- Register ---
@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    hashed_pwd = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        hashed_password=hashed_pwd,
        full_name=user.full_name,
        avatar_url=user.avatar_url,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# --- Login ---
@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not db_user.hashed_password:
        raise HTTPException(status_code=400, detail="Identifiants invalides")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Mot de passe incorrect")

    data = {"sub": db_user.email}
    access_token = jwt_utils.create_access_token(data)
    refresh_token = jwt_utils.create_refresh_token(data)

    return Token(access_token=access_token, refresh_token=refresh_token)


# --- Refresh ---
@router.post("/refresh", response_model=Token)
def refresh_token(token: TokenData):
    payload = jwt_utils.decode_token(token.refresh_token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Token invalide")

    data = {"sub": payload["sub"]}
    new_access_token = jwt_utils.create_access_token(data)
    new_refresh_token = jwt_utils.create_refresh_token(data)

    return Token(access_token=new_access_token, refresh_token=new_refresh_token)
