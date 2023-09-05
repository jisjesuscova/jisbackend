from app.backend.db.models import HonoraryModel, EmployeeModel, EmployeeLaborDatumModel, UserModel, BranchOfficeModel, SupervisorModel, BankModel, RegionModel, CommuneModel, HonoraryReasonModel
from sqlalchemy import desc
from datetime import datetime
from app.backend.classes.hr_setting_class import HrSettingClass
from app.backend.classes.commune_class import CommuneClass
from app.backend.classes.helper_class import HelperClass
import requests
import json

class HonoraryClass:
    def __init__(self, db):
        self.db = db

    def get_all(self, rut=None, rol_id=None, page=1, items_per_page=10):
        try:
            if rol_id == 3:
                data_query = self.db.query(HonoraryModel, EmployeeLaborDatumModel, BranchOfficeModel, SupervisorModel). \
                    outerjoin(EmployeeLaborDatumModel, EmployeeLaborDatumModel.rut == HonoraryModel.rut). \
                    outerjoin(BranchOfficeModel, BranchOfficeModel.id == EmployeeLaborDatumModel.branch_office_id). \
                    outerjoin(SupervisorModel, SupervisorModel.branch_office_id == BranchOfficeModel.id). \
                    filter(SupervisorModel.rut == rut). \
                    order_by(EmployeeModel.rut)
            else:
                data_query = self.db.query(HonoraryModel) \
                                .join(BankModel, BankModel.id == HonoraryModel.bank_id) \
                                .join(BranchOfficeModel, BranchOfficeModel.id == HonoraryModel.branch_office_id) \
                                .join(RegionModel, RegionModel.id == HonoraryModel.region_id) \
                                .join(CommuneModel, CommuneModel.id == HonoraryModel.commune_id) \
                                .join(EmployeeModel, EmployeeModel.rut == HonoraryModel.requested_by) \
                                .join(HonoraryReasonModel, HonoraryReasonModel.id == HonoraryModel.reason_id) \
                                .join(UserModel, UserModel.rut == EmployeeModel.rut) \
                                .add_columns(
                                    HonoraryModel.status_id,
                                    HonoraryModel.id,
                                    HonoraryModel.rut,
                                    HonoraryModel.full_name,
                                    UserModel.nickname,
                                    HonoraryReasonModel.reason,
                                    HonoraryModel.start_date
                                ) \
                                .order_by(desc(HonoraryModel.added_date))


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
        
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
    
    def get(self, field, value):
        try:
            data = self.db.query(HonoraryModel).filter(getattr(HonoraryModel, field) == value).first()
            return data
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
    
    def store(self, honorary_inputs):
        try:
            honorary = HonoraryModel()
            honorary.reason_id = honorary_inputs['reason_id']
            honorary.branch_office_id = honorary_inputs['branch_office_id']
            honorary.foreigner_id = honorary_inputs['foreigner_id']
            honorary.bank_id = honorary_inputs['bank_id']
            honorary.schedule_id = honorary_inputs['schedule_id']
            honorary.region_id = honorary_inputs['region_id']
            honorary.commune_id = honorary_inputs['commune_id']
            honorary.requested_by = honorary_inputs['requested_by']
            honorary.status_id = honorary_inputs['status_id']
            honorary.accountability_status_id = honorary_inputs['accountability_status_id']
            honorary.employee_to_replace = honorary_inputs['employee_to_replace']
            honorary.rut = honorary_inputs['rut']
            honorary.full_name = honorary_inputs['full_name']
            honorary.email = honorary_inputs['email']
            honorary.address = honorary_inputs['address']
            honorary.account_number = honorary_inputs['account_number']
            honorary.start_date = honorary_inputs['start_date']
            honorary.end_date = honorary_inputs['end_date']
            honorary.added_date = datetime.now()
            honorary.updated_date = datetime.now()

            self.db.add(honorary)
            self.db.commit()
            return 1
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
        
    def delete(self, id):
        try:
            data = self.db.query(HonoraryModel).filter(HonoraryModel.id == id).first()
            if data:
                self.db.delete(data)
                self.db.commit()
                return 1
            else:
                return "No data found"
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
        
    def update(self, id, honorary_inputs):
        honorary = self.db.query(HonoraryModel).filter(HonoraryModel.id == id).one_or_none()

        if honorary_inputs.reason_id != None:
            honorary.reason_id = honorary_inputs.reason_id

        if honorary_inputs.branch_office_id != None:
            honorary.branch_office_id = honorary_inputs.branch_office_id

        if honorary_inputs.foreigner_id != None:
            honorary.foreigner_id = honorary_inputs.foreigner_id

        if honorary_inputs.bank_id != None:
            honorary.bank_id = honorary_inputs.bank_id

        if honorary_inputs.schedule_id != None:
            honorary.schedule_id = honorary_inputs.schedule_id

        if honorary_inputs.region_id != None:
            honorary.region_id = honorary_inputs.region_id
        
        if honorary_inputs.commune_id != None:
            honorary.commune_id = honorary_inputs.commune_id

        if honorary_inputs.requested_by != None:
            honorary.requested_by = honorary_inputs.requested_by

        if honorary_inputs.status_id != None:
            honorary.status_id = honorary_inputs.status_id

        if honorary_inputs.accountability_status_id != None:
            honorary.accountability_status_id = honorary_inputs.accountability_status_id

        if honorary_inputs.employee_to_replace != None:
            honorary.employee_to_replace = honorary_inputs.employee_to_replace

        if honorary_inputs.rut != None:
            honorary.rut = honorary_inputs.rut

        if honorary_inputs.full_name != None:
            honorary.full_name = honorary_inputs.full_name

        if honorary_inputs.email != None:
            honorary.email = honorary_inputs.email

        if honorary_inputs.address != None:
            honorary.address = honorary_inputs.address

        if honorary_inputs.account_number != None:
            honorary.account_number = honorary_inputs.account_number

        if honorary_inputs.account_number != None:
            honorary.account_number = honorary_inputs.account_number

        if honorary_inputs.start_date != None:
            honorary.start_date = honorary_inputs.start_date

        if honorary_inputs.end_date != None:
            honorary.end_date = honorary_inputs.end_date

        if honorary_inputs.amount != None:
            honorary.amount = honorary_inputs.amount

        if honorary_inputs.observation != None:
            honorary.observation = honorary_inputs.observation

        honorary.updated_date = datetime.now()

        self.db.add(honorary)
        
        try:
            self.db.commit()

            return 1
        except Exception as e:
            return 0
        
    
    def send(self, data):
        hr_settings = HrSettingClass(self.db).get()

        commune = CommuneClass(self.db).get('id', data.commune_id)
        current_date = HelperClass().get_time_Y_m_d()
        
        amount = HelperClass().remove_from_string('.', str(data.amount))
        amount = round(int(amount) / float(hr_settings.percentage_honorary_bill))

        url = "https://apigateway.cl/api/v1/sii/bte/emitidas/emitir"

        payload = json.dumps({
                                "auth": {
                                    "pass": {
                                    "rut": "76063822-6",
                                    "clave": "JYM1"
                                    }
                                },
                                "boleta": {
                                    
                                    "Encabezado": {
                                        "IdDoc": {
                                            "FchEmis": current_date
                                        },
                                        "Emisor": {
                                            "RUTEmisor": '76063822-6'
                                        },
                                        "Receptor": {
                                            "RUTRecep": data.rut,
                                            "RznSocRecep": data.full_name,
                                            "DirRecep": data.address,
                                            "CmnaRecep": commune.commune
                                        }
                                    },
                                    "Detalle": [
                                        {
                                            "NmbItem": 'Boleta de Honorarios para ' + data.full_name,
                                            "MontoItem": amount
                                        }
                                    ]
                                }
                            })
        
        headers = {
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiYWIyYWUwOGVmYjI1Y2MwMWU5ODUzOWViMDRhNjJkYzEzN2UxMDQyODRmNjY5MTNjMTAxMWM3Yzg1N2Q0NmZmNzY1NGM4NGQzYzM0YzRhMTAiLCJpYXQiOjE2NDk1Mjg4ODMsIm5iZiI6MTY0OTUyODg4MywiZXhwIjo0ODA1MjAyNDgzLCJzdWIiOiI1NzYiLCJzY29wZXMiOltdfQ.K03TeHk5geCY4NARl9UiV8SeeR6Pe4YT1E_Z_z5VLhTJwI36_780NiwxlBIE58hlX9XdjBZiVgpW3FSEYvGQo-6pv6tp9r6Yh9LB6Hi1j5YirwWQgOgPE_2kXBjtXVS84r97unEhpCGA0mGpbIJH0YNNFLYgZauoLzGjmooOYbAT6buhOG5_xTX25VhgscoaPeh_-KnbJVxpMf0YxMkDC7nE5VsI8mMloR3pOyfXpLUH5f3yjl2F8QNPtjRB25MJZnhetMozPUoDX8h5Lh5gcbYItQYtzZrU-3Cs8JMG7bu3fH74a5bej_HmLfdAP-3HP0CxOOhAY4Oppamf8zGwkvzPSeXZdPW79pZ9JEkfRFOfwuYbJA79-nawo_UiKc73HIHgGMFoR9wvfla5JDKrzTh3xoa2JsZUbMZ93iYqsurVMJt-suaqM1Lqcqa1nGZ8HovGgYeVf6RbQH1TJT-ckeGwgfor0Pi_vhhUc9Coxd9qQOAyiY_jHUVy16CQ4BlFkgsOQ9mwBuL5k4xHwNd3VBa_ktLeW36rrXSsaGXwoVLO9Bi19_-fijvrNRmAez3NTiODrMLNNLqXIk9MbUy0PWYAV1Ylq_gdJhJXEED0_iTe6MwA_OrAwVN18U0DQopKwIDLqQoRTAPlcWR1PEO5sBs3jHFclc_BaoHqfG5_W2U',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

        return 1