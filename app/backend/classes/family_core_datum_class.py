from app.backend.db.models import FamilyCoreDatumModel
from datetime import datetime

class FamilyCoreDatumClass:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        try:
            data = self.db.query(FamilyCoreDatumModel).order_by(FamilyCoreDatumModel.id).all()
            if not data:
                return "No data found"
            return data
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
    
    def get(self, field, value, one=1):
        try:
            if one == 1:
                data = self.db.query(FamilyCoreDatumModel).filter(getattr(FamilyCoreDatumModel, field) == value).order_by(FamilyCoreDatumModel.rut).first()
            else:
                data = self.db.query(FamilyCoreDatumModel).filter(getattr(FamilyCoreDatumModel, field) == value).order_by(FamilyCoreDatumModel.rut).all()

            return data
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
    
    def store(self, family_core_datum_inputs, support):
        try:
            family_core_datum = FamilyCoreDatumModel()
            family_core_datum.family_type_id = family_core_datum_inputs.family_type_id
            family_core_datum.employee_rut = family_core_datum_inputs.employee_rut
            family_core_datum.gender_id = family_core_datum_inputs.gender_id
            family_core_datum.rut = family_core_datum_inputs.rut
            family_core_datum.names = family_core_datum_inputs.names
            family_core_datum.father_lastname = family_core_datum_inputs.father_lastname
            family_core_datum.mother_lastname = family_core_datum_inputs.mother_lastname
            family_core_datum.born_date = family_core_datum_inputs.born_date
            family_core_datum.support = support
            family_core_datum.added_date = datetime.now()
            family_core_datum.updated_date = datetime.now()

            self.db.add(family_core_datum)
            self.db.commit()
            return 1
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
        
    def delete(self, id):
        try:
            data = self.db.query(FamilyCoreDatumModel).filter(FamilyCoreDatumModel.id == id).first()
            if data:
                self.db.delete(data)
                self.db.commit()
                return 1
            else:
                return "No data found"
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
        
    def update(self, id, family_core_datum_inputs, support = None):
        family_core_datum = self.db.query(FamilyCoreDatumModel).filter(FamilyCoreDatumModel.id == id).one_or_none()
        if family_core_datum_inputs.family_type_id != None:
            family_core_datum.family_type_id = family_core_datum_inputs.family_type_id

        if family_core_datum_inputs.gender_id != None:
            family_core_datum.gender_id = family_core_datum_inputs.gender_id

        if family_core_datum_inputs.rut != None:
            family_core_datum.rut = family_core_datum_inputs.rut

        if family_core_datum_inputs.names != None:
            family_core_datum.names = family_core_datum_inputs.names

        if family_core_datum_inputs.father_lastname != None:
            family_core_datum.father_lastname = family_core_datum_inputs.father_lastname

        if family_core_datum_inputs.mother_lastname != None:
            family_core_datum.mother_lastname = family_core_datum_inputs.mother_lastname
        
        if family_core_datum_inputs.born_date != None:
            family_core_datum.born_date = family_core_datum_inputs.born_date

        if support != None and support != "":
            family_core_datum.support = support

        family_core_datum.updated_date = datetime.now()

        self.db.add(family_core_datum)
        
        try:
            self.db.commit()

            return 1
        except Exception as e:
            return 0