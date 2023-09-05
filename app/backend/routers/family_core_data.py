from fastapi import APIRouter, Depends, File, UploadFile
from app.backend.db.database import get_db
from sqlalchemy.orm import Session
from app.backend.schemas import FamilyCoreDatum, UpdateFamilyCoreDatum, UserLogin
from app.backend.classes.family_core_datum_class import FamilyCoreDatumClass
from app.backend.auth.auth_user import get_current_active_user
import os
from app.backend.classes.dropbox_class import DropboxClass
from typing import Optional

family_core_data = APIRouter(
    prefix="/family_core_data",
    tags=["Family_Core_Data"]
)

@family_core_data.get("/")
def index(session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    data = FamilyCoreDatumClass(db).get_all()

    return {"message": data}

@family_core_data.post("/store")
def store(form_data: FamilyCoreDatum = Depends(FamilyCoreDatum.as_form), support: UploadFile = File(...), session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    dropbox_client = DropboxClass(db)

    filename = dropbox_client.upload(name=str(form_data.employee_rut) + "_" + str(form_data.rut), description='partida_nacimiento', data=support,
                                 dropbox_path='/intranet_jisparking_files/', computer_path=os.path.join('C:\\', 'Users', 'jesus', 'OneDrive', 'Desktop', 'erpjis_fastapi', 'app', 'backend'))

    data = FamilyCoreDatumClass(db).store(form_data, filename)

    return {"message": data}

@family_core_data.get("/edit/{rut}/{get_type_id}")
def edit(rut:int, get_type_id:int, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):

    data = FamilyCoreDatumClass(db).get("employee_rut", rut, get_type_id)

    return {"message": data}

@family_core_data.delete("/delete/{id}")
def delete(id:int, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    family_core_data = FamilyCoreDatumClass(db).get("id", id, 1)

    response = FamilyCoreDatumClass(db).delete(id)

    if response == 1:
        if family_core_data.support != None or family_core_data.support != '':
            response = DropboxClass(db).delete('/intranet_jisparking_files/', family_core_data.support)

        if response == 1:
            data = 1
        else:
            data = response
    else:
        data = 0
    
    return {"message": data}

@family_core_data.patch("/update/{id}")
def update(id: int, form_data: UpdateFamilyCoreDatum = Depends(UpdateFamilyCoreDatum.as_form), support: Optional[UploadFile] = File(None), session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    family_core_data = FamilyCoreDatumClass(db).get("id", id, 1)

    if support != '' and support != None:
        dropbox_client = DropboxClass(db)

        filename = dropbox_client.upload(name=str(form_data.employee_rut) + "_" + str(form_data.rut), description='partida_nacimiento', data=support,
                                 dropbox_path='/intranet_jisparking_files/', computer_path=os.path.join('C:\\', 'Users', 'jesus', 'OneDrive', 'Desktop', 'erpjis_fastapi', 'app', 'backend'))

        if family_core_data.support != None or family_core_data.support != '': 
            response = DropboxClass(db).delete('/intranet_jisparking_files/', str(family_core_data.support))

        data = FamilyCoreDatumClass(db).update(id, form_data, filename)
    else:
        data = FamilyCoreDatumClass(db).update(id, form_data)

    return {"message": data}