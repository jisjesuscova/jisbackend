from app.backend.db.models import DocumentEmployeeModel
from datetime import datetime

class DocumentEmployeeClass:
    def __init__(self, db):
        self.db = db

    def get_all(self, rut):
        try:
            data = self.db.query(DocumentEmployeeModel).filter(DocumentEmployeeModel.rut == rut).order_by(DocumentEmployeeModel.id).all()
            if not data:
                return "No data found"
            return data
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
    
    def get_all_where(self, document_type_id):
        try:
            data = self.db.query(DocumentEmployeeModel).filter(DocumentEmployeeModel.document_type_id==document_type_id).order_by(DocumentEmployeeModel.id).all()
            if not data:
                return "No data found"
            return data
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
        
    def get(self, field, value):
        try:
            data = self.db.query(DocumentEmployeeModel).filter(getattr(DocumentEmployeeModel, field) == value).first()
            return data
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
    
    def store(self, document_employee_inputs):
        try:
            document_employee = DocumentEmployeeModel()
            document_employee.status_id = document_employee_inputs['status_id']
            document_employee.rut = document_employee_inputs['rut']
            document_employee.document_type_id = document_employee_inputs['document_type_id']
            document_employee.added_date = datetime.now()
            document_employee.updated_date = datetime.now()

            self.db.add(document_employee)
            self.db.commit()
            
            return document_employee.id
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
        
    def medical_license_store(self, document_employee_inputs):
        try:
            document_employee = DocumentEmployeeModel()
            document_employee.status_id = document_employee_inputs.status_id
            document_employee.rut = document_employee_inputs.rut
            document_employee.document_type_id = document_employee_inputs.document_type_id
            document_employee.added_date = datetime.now()
            document_employee.updated_date = datetime.now()

            self.db.add(document_employee)
            self.db.commit()
            
            return document_employee.id
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
    
    def update_file(self, id, file):
        document_employee = self.db.query(DocumentEmployeeModel).filter(DocumentEmployeeModel.id==id).first()
        document_employee.support = file
        document_employee.updated_date = datetime.now()

        self.db.add(document_employee)
        self.db.commit()
        
        return 1
    
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
        
    def update(self, id, document_employee):
        existing_document_employee = self.db.query(DocumentEmployeeModel).filter(DocumentEmployeeModel.id == id).one_or_none()

        if not existing_document_employee:
            return "No data found"

        existing_document_employee_data = document_employee.dict(exclude_unset=True)
        for key, value in existing_document_employee_data.items():
            setattr(existing_document_employee, key, value)

        self.db.commit()

        return 1