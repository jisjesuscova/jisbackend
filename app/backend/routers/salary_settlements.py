from fastapi import APIRouter, Depends
from app.backend.db.database import get_db
from sqlalchemy.orm import Session
from app.backend.schemas import UserLogin
from app.backend.classes.salary_settlement_class import SalarySettlementClass
from app.backend.auth.auth_user import get_current_active_user
import os

salary_settlements = APIRouter(
    prefix="/salary_settlements",
    tags=["SalarySettlements"]
)

@salary_settlements.get("/")
def index(session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    data = SalarySettlementClass(db).get_all()

    return {"message": data}


@salary_settlements.get("/edit/{rut}/{page}")
def edit(rut:int, page:int = None, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    data = SalarySettlementClass(db).get("rut", rut, 2, page)

    return {"message": data}


@salary_settlements.get("/download/{id}")
def download(id:int, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    data = SalarySettlementClass(db).download(id)

    return {"message": data}