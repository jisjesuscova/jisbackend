from app.backend.db.models import VacationModel, TotalVacationDaysModel, OldVacationModel, OldDocumentEmployeeModel, DocumentEmployeeModel
from app.backend.classes.employee_labor_datum_class import EmployeeLaborDatumClass
from app.backend.classes.employee_extra_datum_class import EmployeeExtraDatumClass
from app.backend.classes.helper_class import HelperClass
from app.backend.classes.employee_class import EmployeeClass
from datetime import date
from datetime import datetime
from sqlalchemy import desc
from sqlalchemy import or_
from app.backend.classes.dropbox_class import DropboxClass
import json

class VacationClass:
    def __init__(self, db):
        self.db = db

    def get_all(self, rut, page=1, items_per_page=10):
        try:
            data_query = self.db.query(DocumentEmployeeModel.status_id, DocumentEmployeeModel.document_type_id, VacationModel.document_employee_id, DocumentEmployeeModel.support, VacationModel.rut, VacationModel.id, VacationModel.since, VacationModel.until, VacationModel.days, VacationModel.no_valid_days).\
                    outerjoin(DocumentEmployeeModel, DocumentEmployeeModel.id == VacationModel.document_employee_id).\
                    filter(VacationModel.rut == rut).\
                    filter(DocumentEmployeeModel.document_type_id == 6).\
                    order_by(desc(VacationModel.since))
            
            total_items = data_query.count()
            total_pages = (total_items + items_per_page - 1) // items_per_page

            if page < 1 or page > total_pages:
                return "Invalid page number"

            data = data_query.offset((page - 1) * items_per_page).limit(items_per_page).all()

            if not data:
                return "No data found"

            # Serializar los datos en una estructura de diccionario
            serialized_data = {
                "total_items": total_items,
                "total_pages": total_pages,
                "current_page": page,
                "items_per_page": items_per_page,
                "data": [
                    {
                        "status_id": item.status_id,
                        "document_type_id": item.document_type_id,
                        "document_employee_id": item.document_employee_id,
                        "support": item.support,
                        "rut": item.rut,
                        "id": item.id,
                        "since": item.since.strftime('%Y-%m-%d') if item.since else None,
                        "until": item.until.strftime('%Y-%m-%d') if item.until else None,
                        "days": item.days,
                        "no_valid_days": item.no_valid_days
                    }
                    for item in data
                ]
            }

            # Convierte el resultado a una cadena JSON
            serialized_result = json.dumps(serialized_data)

            return serialized_result
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"

    
    def pdf_get_all(self, rut, page=1, items_per_page=10):
        try:
            data_query = self.db.query(
                DocumentEmployeeModel.status_id,
                DocumentEmployeeModel.document_type_id,
                VacationModel.document_employee_id,
                DocumentEmployeeModel.support,
                VacationModel.rut,
                VacationModel.id,
                VacationModel.since,
                VacationModel.until,
                VacationModel.days,
                VacationModel.no_valid_days
            ).outerjoin(DocumentEmployeeModel, DocumentEmployeeModel.id == VacationModel.document_employee_id).filter(VacationModel.rut == rut).filter(DocumentEmployeeModel.document_type_id == 6).order_by(desc(VacationModel.since))

            total_items = data_query.count()
            total_pages = (total_items + items_per_page - 1) // items_per_page

            if page < 1 or page > total_pages:
                return "Invalid page number"

            data = data_query.offset((page - 1) * items_per_page).limit(items_per_page).all()

            if not data:
                return "No data found"

            # Serializar los datos en una estructura de diccionario
            serialized_data = {
                "total_items": total_items,
                "total_pages": total_pages,
                "current_page": page,
                "items_per_page": items_per_page,
                "data": [
                    {
                        "status_id": item.status_id,
                        "document_type_id": item.document_type_id,
                        "document_employee_id": item.document_employee_id,
                        "support": item.support,
                        "rut": item.rut,
                        "id": item.id,
                        "since": item.since.strftime('%Y-%m-%d') if item.since else None,
                        "until": item.until.strftime('%Y-%m-%d') if item.until else None,
                        "days": item.days,
                        "no_valid_days": item.no_valid_days
                    }
                    for item in data
                ]
            }

            # Convierte el resultado a una cadena JSON
            serialized_result = json.dumps(serialized_data)

            return serialized_result
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
        
    def get(self, field, value):
        try:
            data = self.db.query(VacationModel).filter(getattr(VacationModel, field) == value).first()
            return data
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
    
    def store(self, vacation_inputs):
        days = HelperClass().days(vacation_inputs['since'], vacation_inputs['until'], vacation_inputs['no_valid_days'])

        vacation = VacationModel()
        vacation.document_employee_id = vacation_inputs['document_employee_id']
        vacation.rut = vacation_inputs['rut']
        vacation.since = vacation_inputs['since']
        vacation.until = vacation_inputs['until']
        vacation.days = days
        vacation.no_valid_days = vacation_inputs['no_valid_days']
        vacation.support = ''
        vacation.added_date = datetime.now()
        vacation.updated_date = datetime.now()

        self.db.add(vacation)
        try:
            self.db.commit()

            return 1
        except Exception as e:
            return 0
        
    def download(self, id):
        try:
            data = self.db.query(DocumentEmployeeModel).filter(DocumentEmployeeModel.id == id).first()

            file = DropboxClass(self.db).get('/signatures/', data.support)

            return file
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
        
    def delete(self, id):
        try:
            data = self.db.query(VacationModel).filter(VacationModel.document_employee_id == id).first()
            if data:
                self.db.delete(data)
                self.db.commit()
                return 1
            else:
                return "No se encontró el registro"
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
        
    def update(self, id, vacation):
        existing_vacation = self.db.query(VacationModel).filter(VacationModel.id == id).one_or_none()

        if not existing_vacation:
            return "No se encontró el registro"

        existing_vacation_data = vacation.dict(exclude_unset=True)
        for key, value in existing_vacation_data.items():
            setattr(existing_vacation, key, value)

        self.db.commit()

        return "Registro actualizado"
    
    def legal(self, rut):
        employee_labor_data = EmployeeLaborDatumClass(self.db).get("rut", rut)
        employee_extra_data = EmployeeExtraDatumClass(self.db).get("rut", rut)
        months = HelperClass().months(employee_labor_data.entrance_company, date.today())
        vacation_days = HelperClass().vacation_days(months, employee_extra_data.extreme_zone_id)

        return vacation_days
    
    def calculate_total_vacation_days(self):
        total_vacation_days = self.db.query(TotalVacationDaysModel).filter(TotalVacationDaysModel.id == 1).first()

        total = total_vacation_days.total_employee_vacation_days - (total_vacation_days.total_days - total_vacation_days.total_no_valid_days)

        return total

    def taken(self, rut):
        status_id = EmployeeClass(self.db).is_active(rut)

        if status_id == 1:
            vacations = self.db.query(VacationModel). \
                outerjoin(DocumentEmployeeModel, DocumentEmployeeModel.id == VacationModel.document_employee_id). \
                filter(
                    DocumentEmployeeModel.rut == rut,
                    DocumentEmployeeModel.document_type_id == 6,
                    or_(
                        DocumentEmployeeModel.status_id == 4,
                        DocumentEmployeeModel.status_id == 3
                    )
                ).order_by(desc(DocumentEmployeeModel.added_date)).all()

            taken_days = 0
            
            for vacation in vacations:
                if vacation.no_valid_days is None:
                    no_valid_days = 0
                else:
                    no_valid_days = vacation.no_valid_days

                taken_days = taken_days + vacation.days - no_valid_days
        else:
            vacations = OldVacationModel.query\
                        .join(OldDocumentEmployeeModel, OldDocumentEmployeeModel.id == OldVacationModel.document_employee_id)\
                        .add_columns(OldVacationModel.no_valid_days, OldVacationModel.id, OldVacationModel.rut, OldVacationModel.since, OldVacationModel.until, OldVacationModel.days, OldDocumentEmployeeModel.status_id)\
                        .filter(OldDocumentEmployeeModel.rut == rut, OldDocumentEmployeeModel.document_type_id == 6, or_(OldDocumentEmployeeModel.status_id == 4, OldDocumentEmployeeModel.status_id == 3)) \
                        .order_by(desc(OldDocumentEmployeeModel.added_date))

            taken_days = 0

            for vacation in vacations:
                if vacation.no_valid_days is None:
                    no_valid_days = 0
                else:
                    no_valid_days = vacation.no_valid_days

                taken_days = taken_days + vacation.days - no_valid_days

        return taken_days
    