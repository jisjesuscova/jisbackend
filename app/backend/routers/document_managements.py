from fastapi import APIRouter, Depends
from app.backend.db.database import get_db
from sqlalchemy.orm import Session
from app.backend.schemas import DocumentManagement
from app.backend.classes.document_management_class import DocumentManagementClass
from app.backend.auth.auth_user import get_current_active_user
from app.backend.schemas import UserLogin

document_managements = APIRouter(
    prefix="/document_managements",
    tags=["DocumentManagements"]
)

@document_managements.get("/{rut}/{page}")
def index(rut:int, page:int, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    data = DocumentManagementClass(db).get_all(rut, page)

    return {"message": data}

@document_managements.post("/store")
def store(document_management:DocumentManagement, db: Session = Depends(get_db)):
    document_management_inputs = document_management.dict()
    data = DocumentManagementClass(db).store(document_management_inputs)

    return {"message": data}
