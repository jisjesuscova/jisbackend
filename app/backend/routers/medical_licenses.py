from fastapi import APIRouter, Depends, File, UploadFile
from app.backend.db.database import get_db
from sqlalchemy.orm import Session
from app.backend.schemas import MedicalLicense, UpdateMedicalLicense, UserLogin, UploadMedicalLicense
from app.backend.classes.medical_license_class import MedicalLicenseClass
from app.backend.auth.auth_user import get_current_active_user
from app.backend.classes.dropbox_class import DropboxClass
from app.backend.classes.document_employee_class import DocumentEmployeeClass
from app.backend.classes.document_type_class import DocumentTypeClass
import os

medical_licenses = APIRouter(
    prefix="/medical_licenses",
    tags=["MedicalLicenses"]
)

@medical_licenses.get("/")
def index(session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    data = MedicalLicenseClass(db).get_all()

    return {"message": data}

@medical_licenses.post("/store")
def store(form_data: MedicalLicense = Depends(MedicalLicense.as_form), support: UploadFile = File(...), session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    document_type = DocumentTypeClass(db).get("id", form_data.document_type_id)

    dropbox_client = DropboxClass(db)

    filename = dropbox_client.upload(name=str(form_data.rut), description=str(document_type.document_type), data=support,
                                 dropbox_path='/medical_licenses/', computer_path=os.path.join('C:\\', 'Users', 'jesus', 'OneDrive', 'Desktop', 'erpjis_fastapi', 'backend', 'app', 'backend'))
    
    document_employee_id = DocumentEmployeeClass(db).medical_license_store(form_data)

    DocumentEmployeeClass(db).update_file(document_employee_id, filename)

    data = MedicalLicenseClass(db).store(form_data, document_employee_id)

    return {"message": data}

@medical_licenses.delete("/delete/{id}")
def delete(id:int, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    medical_license = MedicalLicenseClass(db).get("id", id, 1, 1, 1)
    document_employee = DocumentEmployeeClass(db).get('id', medical_license.document_employee_id)
    document_employee_response = DocumentEmployeeClass(db).delete(medical_license.document_employee_id)
    medical_license_response = MedicalLicenseClass(db).delete(id)

    if document_employee_response ==  1 and medical_license_response == 1:
        if document_employee.support != None or document_employee.support != '':
            response = DropboxClass(db).delete('/medical_licenses/', document_employee.support)

        if response == 1:
            data = 1
        else:
            data = response
    else:
        data = 0
    
    return {"message": data}

@medical_licenses.get("/edit/{rut}/{page}")
def edit(rut:int, page:int = None, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    data = MedicalLicenseClass(db).get("rut", rut, 2, page)

    return {"message": data}

@medical_licenses.patch("/update/{id}")
def update(id: int, medical_license: UpdateMedicalLicense, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    data = MedicalLicenseClass(db).update(id, medical_license)

    return {"message": data}

@medical_licenses.get("/download/{id}")
def download(id:int, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    data = MedicalLicenseClass(db).download(id)

    return {"message": data}

@medical_licenses.post("/upload")
def upload(form_data: UploadMedicalLicense = Depends(UploadMedicalLicense.as_form), support: UploadFile = File(...), session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    dropbox_client = DropboxClass(db)

    filename = dropbox_client.upload(name=form_data.rut, description='contrato', data=support,
                                 dropbox_path='/medical_licenses/', computer_path=os.path.join('C:\\', 'Users', 'jesus', 'OneDrive', 'Desktop', 'erpjis_fastapi', 'backend', 'app', 'backend'))
    
    medical_license = MedicalLicenseClass(db).get("id", form_data.medical_license_id)
    data = DocumentEmployeeClass(db).update_file(medical_license.document_employee_id, filename)

    return {"message": data}
