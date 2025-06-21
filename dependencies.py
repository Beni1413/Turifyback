from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User

def get_current_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

def verificar_admin(user: User = Depends(get_current_user)):
    if user.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo administradores")
