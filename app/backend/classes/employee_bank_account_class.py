from app.backend.db.models import EmployeeBankAccountModel
from app.backend.classes.helper_class import HelperClass
from datetime import datetime

class EmployeeBankAccountClass:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        try:
            data = self.db.query(EmployeeBankAccountModel).order_by(EmployeeBankAccountModel.id).all()
            if not data:
                return "No data found"
            return data
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
    
    def get(self, field, value):
        try:
            data = self.db.query(EmployeeBankAccountModel).filter(getattr(EmployeeBankAccountModel, field) == value).first()
            return data
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
    
    def store(self, EmployeeBankAccount_inputs):
        try:
            data = EmployeeBankAccountModel(**EmployeeBankAccount_inputs)
            self.db.add(data)
            self.db.commit()
            return 1
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
        
    def delete(self, id):
        try:
            data = self.db.query(EmployeeBankAccountModel).filter(EmployeeBankAccountModel.id == id).first()
            if data:
                self.db.delete(data)
                self.db.commit()
                return 1
            else:
                return "No data found"
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
        
    def update(self, id, employee_bank_account_inputs):
        employee_bank_account =  self.db.query(EmployeeBankAccountModel).filter(EmployeeBankAccountModel.rut == id).one_or_none()

        if employee_bank_account_inputs['bank_id'] != None:
            employee_bank_account.bank_id = employee_bank_account_inputs['bank_id']
        
        if employee_bank_account_inputs['account_type_id'] != None:
            employee_bank_account.account_type_id = employee_bank_account_inputs['account_type_id']
        
        if employee_bank_account_inputs['rut'] != None:
            employee_bank_account.rut = employee_bank_account_inputs['rut']

        if employee_bank_account_inputs['account_number'] != None:
            employee_bank_account.account_number = employee_bank_account_inputs['account_number']

        employee_bank_account.update_date = datetime.now()

        self.db.add(employee_bank_account)

        try:
            self.db.commit()

            return 1
        except Exception as e:
            return 0