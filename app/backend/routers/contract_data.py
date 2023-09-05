from fastapi import APIRouter, Depends, Response
from app.backend.db.database import get_db
from sqlalchemy.orm import Session
from app.backend.schemas import ContractDatum, UploadContract, UserLogin, SelectDocumentEmployee
from app.backend.classes.document_employee_class import DocumentEmployeeClass
from app.backend.classes.dropbox_class import DropboxClass
from app.backend.auth.auth_user import get_current_active_user
import os
import requests
import pdfkit

contract_data = APIRouter(
    prefix="/contract_data",
    tags=["ContractData"]
)

@contract_data.post("/")
def index(select_document_employee: SelectDocumentEmployee, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    data = DocumentEmployeeClass(db).get_all(select_document_employee.rut)

    return {"message": data}

@contract_data.post("/store")
def store(contract_datum:ContractDatum, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    contract_datum_inputs = contract_datum.dict()
    document_id = DocumentEmployeeClass(db).store(contract_datum_inputs)

    return {"document_message": document_id}

@contract_data.delete("/delete/{id}")
def delete(id:int, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    document_employee = DocumentEmployeeClass(db).get("id", id)
    response = DocumentEmployeeClass(db).delete(id)

    if response == 1:
        if document_employee.support != None:
            response = DropboxClass(db).delete('/contracts/', document_employee.support)

        if response == 1:
            data = 1
        else:
            data = 0
    else:
        data = 0
    
    return {"message": data}

@contract_data.post("/upload")
def upload(form_data: UploadContract = Depends(UploadContract), session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    dropbox_client = DropboxClass(db)

    filename = dropbox_client.upload(name=form_data.rut, description='contrato', data=form_data.support,
                                 dropbox_path='/contracts/', computer_path=os.path.join('C:\\', 'Users', 'jesus', 'OneDrive', 'Desktop', 'erpjis_fastapi', 'app', 'backend'))
    
    data = DocumentEmployeeClass(db).update_file(form_data.id, filename)

    return {"message": data}

@contract_data.get("/download/{id}")
def download(id:int, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    document_employee = DocumentEmployeeClass(db).get("id", id)
    response = DropboxClass(db).get('/contracts/', document_employee.support)

    response = requests.get(response)
    
    content_disposition = "attachment; filename="+ str(document_employee.support) +""

    return Response(content=response.content, headers={"Content-Disposition": content_disposition})