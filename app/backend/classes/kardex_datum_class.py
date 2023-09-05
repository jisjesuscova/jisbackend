from app.backend.db.models import DocumentEmployeeModel, DocumentTypeModel
from sqlalchemy import desc
from datetime import datetime
from app.backend.classes.dropbox_class import DropboxClass

class KardexDatumClass:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        try:
            data = self.db.query(DocumentEmployeeModel).filter(DocumentEmployeeModel.document_group_id == 1).order_by(DocumentEmployeeModel.document_type).all()

            if not data:
                return "No data found"
            return data
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
    
    def get(self, field, value, type = 1):
        try:
            if type == 1:
                data = self.db.query(DocumentEmployeeModel).filter(DocumentEmployeeModel.id == value).first()
            else:
                data = self.db.query(DocumentEmployeeModel.id, DocumentEmployeeModel.rut, DocumentTypeModel.document_type, DocumentEmployeeModel.added_date).\
                    outerjoin(DocumentTypeModel, DocumentEmployeeModel.document_type_id == DocumentTypeModel.id).\
                    filter(getattr(DocumentEmployeeModel, field) == value).\
                    filter(DocumentTypeModel.document_group_id == 1).\
                    order_by(desc(DocumentEmployeeModel.added_date)).\
                    all()
            
            
            return data
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"

    def download(self, id):
        try:
            data = self.db.query(DocumentEmployeeModel).filter(DocumentEmployeeModel.id == id).first()

            file = DropboxClass(self.db).get('/employee_documents/', data.support)

            return file
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
        
    def store(self, document_kardex_inputs, support):
        try:
            document_employee = DocumentEmployeeModel()
            document_employee.rut = document_kardex_inputs.rut
            document_employee.status_id = document_kardex_inputs.status_id
            document_employee.document_type_id = document_kardex_inputs.document_type_id
            document_employee.old_document_status_id = document_kardex_inputs.old_document_status_id
            document_employee.support = support
            document_employee.added_date = datetime.now()
            document_employee.updated_date = datetime.now()

            self.db.add(document_employee)
            self.db.commit()
            return 1
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
        
    def delete(self, id):
        try:
            data = self.db.query(DocumentEmployeeModel).filter(DocumentEmployeeModel.id == id).first()
            if data:
                self.db.delete(data)
                self.db.commit()
                return 1
            else:
                return "No data found"
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
        
    def update(self, id, DocumentType):
        existing_kardex = self.db.query(DocumentEmployeeModel).filter(DocumentEmployeeModel.id == id).one_or_none()

        if not existing_kardex:
            return "No data found"

        existing_kardex_data = DocumentType.dict(exclude_unset=True)
        for key, value in existing_kardex_data.items():
            setattr(existing_kardex, key, value)

        self.db.commit()

        return 1