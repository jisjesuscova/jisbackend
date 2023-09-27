from app.backend.db.models import MedicalLicenseModel, DocumentEmployeeModel, EmployeeModel
from datetime import datetime
from sqlalchemy import desc
from app.backend.classes.dropbox_class import DropboxClass
from app.backend.classes.helper_class import HelperClass
import json

class MedicalLicenseClass:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        try:
            data = self.db.query(MedicalLicenseModel).order_by(MedicalLicenseModel.id).all()
            if not data:
                return "No hay registros"
            return data
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
    
    def get(self, field, value, type=1, page=1, items_per_page=10):
        try:
            if type == 1:
                data = self.db.query(MedicalLicenseModel).filter(getattr(MedicalLicenseModel, field) == value).first()
                if data:
                    # Serializar el objeto MedicalLicenseModel a un diccionario
                    serialized_data = {
                        "document_employee_id": data.document_employee_id,
                        "document_type_id": data.document_type_id,
                        "folio": data.folio,
                        "since": data.since.strftime('%Y-%m-%d') if data.since else None,
                        "until": data.until.strftime('%Y-%m-%d') if data.until else None,
                        "days": data.days,
                        "support": data.support,
                        "status_id": data.status_id,
                        "id": data.id
                    }
                    return serialized_data
                else:
                    return "No data found"
            else:
                data_query = self.db.query(
                    MedicalLicenseModel.document_employee_id,
                    DocumentEmployeeModel.document_type_id,
                    MedicalLicenseModel.folio,
                    EmployeeModel.visual_rut,
                    MedicalLicenseModel.since,
                    MedicalLicenseModel.until,
                    MedicalLicenseModel.days,
                    DocumentEmployeeModel.support,
                    DocumentEmployeeModel.status_id,
                    MedicalLicenseModel.id
                ).outerjoin(DocumentEmployeeModel, DocumentEmployeeModel.id == MedicalLicenseModel.document_employee_id).outerjoin(EmployeeModel, EmployeeModel.rut == MedicalLicenseModel.rut).filter(getattr(MedicalLicenseModel, field) == value).filter(DocumentEmployeeModel.document_type_id == 35).order_by(desc(MedicalLicenseModel.since))

                total_items = data_query.count()
                total_pages = (total_items + items_per_page - 1) // items_per_page

                if page < 1 or page > total_pages:
                    return "Invalid page number"

                data = data_query.offset((page - 1) * items_per_page).limit(items_per_page).all()

                if not data:
                    return "No data found"

                # Serializar la lista de objetos MedicalLicenseModel a una lista de diccionarios
                serialized_data = {
                    "total_items": total_items,
                    "total_pages": total_pages,
                    "current_page": page,
                    "items_per_page": items_per_page,
                    "data": [
                        {
                            "document_employee_id": item.document_employee_id,
                            "document_type_id": item.document_type_id,
                            "folio": item.folio,
                            "visual_rut": item.visual_rut,
                            "since": item.since.strftime('%Y-%m-%d') if item.since else None,
                            "until": item.until.strftime('%Y-%m-%d') if item.until else None,
                            "days": item.days,
                            "support": item.support,
                            "status_id": item.status_id,
                            "id": item.id
                        }
                        for item in data
                    ]
                }

                serialized_result = json.dumps(serialized_data)

                return serialized_result
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
    
    def store(self, medicalLicense_inputs, document_employee_id):
        try:
            get_periods = HelperClass().get_periods(medicalLicense_inputs.since, medicalLicense_inputs.until)

            for i in range(len(get_periods)):
                period = HelperClass().split(get_periods[i][0], '-')
                period = period[1] +'-'+ period[0]

                medical_license = MedicalLicenseModel()
                medical_license.document_employee_id = document_employee_id
                medical_license.medical_license_type_id = medicalLicense_inputs.medical_license_type_id
                medical_license.patology_type_id = medicalLicense_inputs.patology_type_id 
                medical_license.period = period
                medical_license.rut = medicalLicense_inputs.rut
                medical_license.folio = medicalLicense_inputs.folio
                medical_license.since = get_periods[i][0]
                medical_license.until = get_periods[i][1]
                medical_license.days = get_periods[i][2]
                medical_license.added_date = datetime.now()
                medical_license.updated_date = datetime.now()

                self.db.add(medical_license)
                self.db.commit()

            return 1
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
        
    def delete(self, id):
        try:
            data = self.db.query(MedicalLicenseModel).filter(MedicalLicenseModel.id == id).first()
            if data:
                self.db.delete(data)
                self.db.commit()
                return 1
            else:
                return "No se encontró el registro"
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
        
    def update(self, id, medical_license):
        existing_medical_license = self.db.query(MedicalLicenseModel).filter(MedicalLicenseModel.id == id).one_or_none()

        if not existing_medical_license:
            return "No se encontró el registro"

        existing_medical_license_data = medical_license.dict(exclude_unset=True)
        for key, value in existing_medical_license_data.items():
            setattr(existing_medical_license, key, value)

        self.db.commit()

        return "Registro actualizado"
    
    def download(self, id):
        try:
            data = self.db.query(DocumentEmployeeModel).filter(DocumentEmployeeModel.id == id).first()

            file = DropboxClass(self.db).get('/medical_licenses/', data.support)

            return file
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"