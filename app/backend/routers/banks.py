from fastapi import APIRouter, Depends, Request, Response, UploadFile, File
from app.backend.db.database import get_db
from sqlalchemy.orm import Session
from app.backend.schemas import Employee, UpdateEmployee, SearchEmployee, UserLogin, EmployeeList, UploadSignature, UploadPicture
from app.backend.classes.employee_class import EmployeeClass
from app.backend.auth.auth_user import get_current_active_user
import base64
import os
from app.backend.classes.dropbox_class import DropboxClass

banks = APIRouter(
    prefix="/banks",
    tags=["Banks"]
)

@banks.post("/")
def index(employee: EmployeeList, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):

    return {"message": 1}