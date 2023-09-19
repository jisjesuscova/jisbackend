from fastapi import APIRouter, Depends
from app.backend.db.database import get_db
from sqlalchemy.orm import Session
from app.backend.schemas import DocumentEmployee, UpdateDocumentEmployee, UploadDocumentEmployee
from app.backend.classes.document_employee_class import DocumentEmployeeClass
from app.backend.classes.dropbox_class import DropboxClass
import os

documents_employees = APIRouter(
    prefix="/documents_employees",
    tags=["DocumentsEmployees"]
)

@documents_employees.get("/")
def index(db: Session = Depends(get_db)):
    data = DocumentEmployeeClass(db).get_all()

    return {"message": data}

@documents_employees.post("/store")
def store(document_employee:DocumentEmployee, db: Session = Depends(get_db)):
    document_employee_inputs = document_employee.dict()
    data = DocumentEmployeeClass(db).store(document_employee_inputs)

    return {"message": data}

@documents_employees.post("/upload")
def upload(form_data: UploadDocumentEmployee = Depends(UploadDocumentEmployee), db: Session = Depends(get_db)):
    dropbox_client = DropboxClass(db)

    filename = dropbox_client.upload(name=form_data.rut, description=form_data.file_name, data=form_data.picture,
                                 dropbox_path='/'+ form_data.dropbox_path +'/', computer_path=os.path.join('C:\\', 'Users', 'jesus', 'OneDrive', 'Desktop', 'erpjis_fastapi', 'app', 'backend'))
    
    data = DocumentEmployeeClass(db).update_file(form_data.id, filename)

    return {"message": data}

@documents_employees.get("/edit/{id}")
def edit(id:int, db: Session = Depends(get_db)):
    data = DocumentEmployeeClass(db).get("id", id)

    return {"message": data}

@documents_employees.delete("/delete/{id}")
def delete(id:int, dropbox_path:str, db: Session = Depends(get_db)):
    document_employee = DocumentEmployeeClass(db).get("id", id)

    response = DocumentEmployeeClass(db).delete(id)

    if response == 1:
        response = DropboxClass(db).delete('/'+ dropbox_path +'/', document_employee.support)

        if response == 1:
            data = 1
        else:
            data = response
    else:
        data = 0
    
    return {"message": data}

@documents_employees.patch("/update/{id}")
def update(id: int, document_employee: UpdateDocumentEmployee, db: Session = Depends(get_db)):
    data = DocumentEmployeeClass(db).update(id, document_employee)

    return {"message": data}