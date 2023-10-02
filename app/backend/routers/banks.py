from fastapi import APIRouter, Depends
from app.backend.db.database import get_db
from sqlalchemy.orm import Session
from app.backend.schemas import UserLogin, EmployeeList
from app.backend.auth.auth_user import get_current_active_user

banks = APIRouter(
    prefix="/banks",
    tags=["Banks"]
)

@banks.post("/")
def index(employee: EmployeeList, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):

    return {"message": 1}