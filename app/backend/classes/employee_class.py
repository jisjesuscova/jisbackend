from app.backend.db.models import EmployeeModel, EmployeeLaborDatumModel, ClockUserModel, BranchOfficeModel, OldEmployeeModel, OldEmployeeLaborDatumModel, SupervisorModel, EmployeeLaborDatumModel
from datetime import datetime
from sqlalchemy import func
from app.backend.classes.helper_class import HelperClass
from app.backend.classes.dropbox_class import DropboxClass

class EmployeeClass:
    def __init__(self, db):
        self.db = db

    def get_all(self, rut=None, rol_id=None, page=1, items_per_page=10):
        try:
            if page != 0:
                if rol_id == 3:
                    data_query = self.db.query(EmployeeModel, EmployeeLaborDatumModel, BranchOfficeModel, SupervisorModel). \
                        outerjoin(EmployeeLaborDatumModel, EmployeeLaborDatumModel.rut == EmployeeModel.rut). \
                        outerjoin(BranchOfficeModel, BranchOfficeModel.id == EmployeeLaborDatumModel.branch_office_id). \
                        outerjoin(SupervisorModel, SupervisorModel.branch_office_id == BranchOfficeModel.id). \
                        filter(SupervisorModel.rut == rut). \
                        order_by(EmployeeModel.rut)

                else:
                    data_query = self.db.query(EmployeeModel).order_by(EmployeeModel.rut)

                total_items = data_query.count()
                total_pages = (total_items + items_per_page - 1) // items_per_page

                if page < 1 or page > total_pages:
                    return "Invalid page number"

                data = data_query.offset((page - 1) * items_per_page).limit(items_per_page).all()

                if not data:
                    return "No data found"
                            
                return {
                    "total_items": total_items,
                    "total_pages": total_pages,
                    "current_page": page,
                    "items_per_page": items_per_page,
                    "data": data
                }
            else:
                data_query = self.db.query(EmployeeModel).order_by(EmployeeModel.rut).all()

                return data_query

        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
    
    def search(self, search_inputs, page=1, items_per_page=10):
        if len(search_inputs) > 0:
            search_rut = search_inputs['rut']
            search_names = search_inputs['names']
            search_father_lastname = search_inputs['father_lastname']
            search_mother_lastname = search_inputs['mother_lastname']
            search_status_id = search_inputs['status_id']
            search_branch_office_id = search_inputs['branch_office_id']
        
        if search_status_id == '2':
            data_query = self.db.query(OldEmployeeModel).join(OldEmployeeLaborDatumModel, OldEmployeeLaborDatumModel.rut == OldEmployeeModel.rut).add_columns(OldEmployeeModel.id, OldEmployeeModel.rut, OldEmployeeModel.visual_rut, OldEmployeeModel.nickname, OldEmployeeModel.names, OldEmployeeModel.father_lastname, OldEmployeeModel.mother_lastname).order_by('rut')

            if len(search_inputs) > 0:
                if search_rut:
                    data_query = data_query.filter(OldEmployeeModel.visual_rut.like(f"%{search_rut}%"))
                if search_names:
                    data_query = data_query.filter(OldEmployeeModel.nickname.like(f"%{search_names}%"))
                if search_father_lastname:
                    data_query = data_query.filter(OldEmployeeModel.father_lastname.like(f"%{search_father_lastname}%"))
                if search_mother_lastname:
                    data_query = data_query.filter(OldEmployeeModel.mother_lastname.like(f"%{search_mother_lastname}%"))
                if search_branch_office_id:
                    data_query = data_query.filter(OldEmployeeLaborDatumModel.branch_office_id == search_branch_office_id)
                if search_status_id:
                    data_query = data_query.filter(OldEmployeeLaborDatumModel.status_id == search_status_id)
            
            total_items = data_query.count()
            total_pages = (total_items + items_per_page - 1) // items_per_page

            if page < 1 or page > total_pages:
                return "Invalid page number"

            data = data_query.offset((page - 1) * items_per_page).limit(items_per_page).all()

            if not data:
                return "No data found"
        elif search_status_id == '3':
            data_query = self.db.query(OldEmployeeModel).join(OldEmployeeLaborDatumModel, OldEmployeeLaborDatumModel.rut == OldEmployeeModel.rut).add_columns(OldEmployeeModel.id, OldEmployeeModel.rut, OldEmployeeModel.visual_rut, OldEmployeeModel.nickname, OldEmployeeModel.names, OldEmployeeModel.father_lastname, OldEmployeeModel.mother_lastname).order_by('rut')

            if len(search_inputs) > 0:
                if search_rut:
                    data_query = data_query.filter(OldEmployeeModel.visual_rut.like(f"%{search_rut}%"))
                if search_names:
                    data_query = data_query.filter(OldEmployeeModel.names.like(f"%{search_names}%"))
                if search_father_lastname:
                    data_query = data_query.filter(OldEmployeeModel.father_lastname.like(f"%{search_father_lastname}%"))
                if search_mother_lastname:
                    data_query = data_query.filter(OldEmployeeModel.mother_lastname.like(f"%{search_mother_lastname}%"))
                if search_branch_office_id:
                    data_query = data_query.filter(OldEmployeeLaborDatumModel.branch_office_id == search_branch_office_id)
                if search_branch_office_id:
                    data_query = data_query.filter(OldEmployeeLaborDatumModel.branch_office_id == search_branch_office_id)
                if search_status_id:
                    data_query = data_query.filter(OldEmployeeLaborDatumModel.status_id == search_status_id)
            
            total_items = data_query.count()
            total_pages = (total_items + items_per_page - 1) // items_per_page

            if page < 1 or page > total_pages:
                return "Invalid page number"

            data = data_query.offset((page - 1) * items_per_page).limit(items_per_page).all()

            if not data:
                return "No data found"
        else:
            data_query = self.db.query(EmployeeModel).join(EmployeeLaborDatumModel, EmployeeLaborDatumModel.rut == EmployeeModel.rut).add_columns(EmployeeModel.id, EmployeeModel.rut, EmployeeModel.visual_rut, EmployeeModel.names, EmployeeModel.father_lastname, EmployeeModel.mother_lastname).order_by('rut')

            if len(search_inputs) > 0:
                if search_rut:
                    data_query = data_query.filter(EmployeeModel.visual_rut.like(f"%{search_rut}%"))
                if search_names:
                    data_query = data_query.filter(EmployeeModel.names.like(f"%{search_names}%"))
                if search_father_lastname:
                    data_query = data_query.filter(EmployeeModel.father_lastname.like(f"%{search_father_lastname}%"))
                if search_mother_lastname:
                    data_query = data_query.filter(EmployeeModel.mother_lastname.like(f"%{search_mother_lastname}%"))
                if search_branch_office_id:
                    data_query = data_query.filter(EmployeeLaborDatumModel.branch_office_id == search_branch_office_id)


            total_items = data_query.count()
            total_pages = (total_items + items_per_page - 1) // items_per_page

            if page < 1 or page > total_pages:
                return "Invalid page number"

            data = data_query.offset((page - 1) * items_per_page).limit(items_per_page).all()

            if not data:
                return "No data found"
                            
        return {
                "total_items": total_items,
                "total_pages": total_pages,
                "current_page": page,
                "items_per_page": items_per_page,
                "data": data
            }
        
    def get(self, field, value):
        try:
            data = self.db.query(EmployeeModel, ClockUserModel.privilege). \
                outerjoin(ClockUserModel, ClockUserModel.rut == EmployeeModel.rut). \
                filter(getattr(EmployeeModel, field) == value). \
                first()

            signature = DropboxClass(self.db).get('/signatures/', str(data[0].signature))

            if data[0].picture == '' or data[0].picture == None:
                picture = ''
            else:
                picture = DropboxClass(self.db).get('/pictures/', str(data[0].picture))

            result = {
                "employee_data": {
                    "data": data
                },
                "signature": signature,
                "picture": picture,
            }

            return result
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
    
    def one_simple_get(self, rut):
        try:
            employee = self.db.query(EmployeeModel).filter(EmployeeModel.rut==rut).first()

            return employee
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"

    def is_active(self, rut):
        employee = self.db.query(EmployeeModel).filter(EmployeeModel.rut==rut).count()

        return employee
    
    def store(self, employee_inputs):
        numeric_rut = HelperClass().numeric_rut(str(employee_inputs['rut']))

        employee = EmployeeModel()
        employee.rut = numeric_rut
        employee.visual_rut = employee_inputs['rut']
        employee.names = employee_inputs['names']
        employee.father_lastname = employee_inputs['father_lastname']
        employee.mother_lastname = employee_inputs['mother_lastname']
        employee.gender_id = employee_inputs['gender_id']
        employee.nationality_id = employee_inputs['nationality_id']
        employee.personal_email = employee_inputs['personal_email']
        employee.cellphone = employee_inputs['cellphone']
        employee.born_date = employee_inputs['born_date']
        employee.added_date = datetime.now()

        self.db.add(employee)

        try:
            self.db.commit()

            return 1
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
        
    def delete(self, id):
        try:
            data = self.db.query(EmployeeModel).filter(EmployeeModel.rut == id).first()
            if data:
                self.db.delete(data)
                self.db.commit()
                return 1
            else:
                return "No data found"
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
        
    def update(self, id, employee_inputs):
        employee =  self.db.query(EmployeeModel).filter(EmployeeModel.rut == id).one_or_none()

        if 'rut' in employee_inputs and employee_inputs['rut'] is not None:
            numeric_rut = HelperClass().numeric_rut(str(employee_inputs['rut']))
            employee.rut = numeric_rut
            employee.visual_rut = employee_inputs['rut']
        
        if 'names' in employee_inputs and employee_inputs['names'] is not None:
            employee.names = employee_inputs['names']
        
        if 'father_lastname' in employee_inputs and employee_inputs['father_lastname'] is not None:
            employee.father_lastname = employee_inputs['father_lastname']
        
        if 'mother_lastname' in employee_inputs and employee_inputs['mother_lastname'] is not None:
            employee.mother_lastname = employee_inputs['mother_lastname']

        if 'gender_id' in employee_inputs and employee_inputs['gender_id'] is not None:
            employee.gender_id = employee_inputs['gender_id']

        if 'nationality_id' in employee_inputs and employee_inputs['nationality_id'] is not None:
            employee.nationality_id = employee_inputs['nationality_id']
        
        if 'personal_email' in employee_inputs and employee_inputs['personal_email'] is not None:
            employee.personal_email = employee_inputs['personal_email']
        
        if 'cellphone' in employee_inputs and employee_inputs['cellphone'] is not None:
            employee.cellphone = employee_inputs['cellphone']
        
        if 'born_date' in employee_inputs and employee_inputs['born_date'] is not None:
            employee.born_date = employee_inputs['born_date']

        if 'signature' in employee_inputs and employee_inputs['signature'] is not None:
            employee.signature = employee_inputs['signature']

        if 'signature_type_id' in employee_inputs and employee_inputs['signature_type_id'] is not None:
            employee.signature_type_id = employee_inputs['signature_type_id']

        if 'picture' in employee_inputs and employee_inputs['picture'] is not None:
            employee.picture = employee_inputs['picture']

        employee.update_date = datetime.now()

        self.db.add(employee)

        try:
            self.db.commit()

            return 1
        except Exception as e:
            return 0
    
    def get_birthdays(self):
        today = datetime.today()

        employees = self.db.query(
            EmployeeModel.rut,
            EmployeeModel.names,
            EmployeeModel.father_lastname,
            BranchOfficeModel.branch_office,
            func.DATE_FORMAT(EmployeeModel.born_date, "%d").label('day'),
            func.DATE_FORMAT(EmployeeModel.born_date, "%M").label('month')
        ) \
        .join(EmployeeLaborDatumModel, EmployeeLaborDatumModel.rut == EmployeeModel.rut) \
        .join(BranchOfficeModel, BranchOfficeModel.id == EmployeeLaborDatumModel.branch_office_id) \
        .filter(func.DAY(EmployeeModel.born_date) >= today.day, func.MONTH(EmployeeModel.born_date) == today.month) \
        .order_by(func.DAY(EmployeeModel.born_date)) \
        .limit(4) \
        .all()

        return employees
    
    def gender_totals(self):
        men_total = self.db.query(EmployeeModel).filter(EmployeeModel.gender_id == 1).count()
        women_total = self.db.query(EmployeeModel).filter(EmployeeModel.gender_id == 2).count()

        totals = [
            {'gender': 'Men', 'total': men_total},
            {'gender': 'Women', 'total': women_total}
        ]
    
        return totals
    
    def validate_cellphone(self, cellphone):
        existence = self.db.query(EmployeeModel).filter(EmployeeModel.cellphone == cellphone).count()

        if existence == 1:
            return 1
        else:
            return 0