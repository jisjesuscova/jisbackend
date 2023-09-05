from fastapi import APIRouter, Depends
from app.backend.db.database import get_db
from sqlalchemy.orm import Session
from app.backend.schemas import User, UpdateUser, UserLogin, RecoverUser
from app.backend.classes.user_class import UserClass
from app.backend.auth.auth_user import get_current_active_user

users = APIRouter(
    prefix="/users",
    tags=["User"]
)

@users.get("/")
def index(session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    data = UserClass(db).get_all()

    return {"message": data}

@users.post("/store")
def store(user:User, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_inputs = user.dict()
    data = UserClass(db).store(user_inputs)

    return {"message": data}

@users.get("/edit/{id}")
def edit(id:int, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    data = UserClass(db).get("rut", id)

    return {"message": data}

@users.delete("/delete/{id}")
def delete(id:int, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    data = UserClass(db).delete(id)

    return {"message": data}

@users.patch("/update/{id}")
def update(id: int, user: UpdateUser, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_inputs = user.dict()
    data = UserClass(db).update(id, user_inputs)

    return {"message": data}

@users.post("/recover")
def recover(user:RecoverUser, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_inputs = user.dict()
    data = UserClass(db).recover(user_inputs)

    return {"message": data}