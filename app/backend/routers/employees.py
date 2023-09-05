from fastapi import APIRouter, Depends, Request
from app.backend.db.database import get_db
from sqlalchemy.orm import Session
from app.backend.schemas import Employee, UpdateEmployee, SearchEmployee, UserLogin, EmployeeList
from app.backend.classes.employee_class import EmployeeClass
from app.backend.auth.auth_user import get_current_active_user

employees = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)

@employees.post("/")
def index(employee: EmployeeList, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    data = EmployeeClass(db).get_all(employee.rut, employee.rol_id, employee.page)

    return {"message": data}

@employees.post("/search")
def search(search_data: SearchEmployee, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    search_data = search_data.dict()

    employees = EmployeeClass(db).search(search_data, search_data['page'])

    return {"message": employees}

@employees.get("/get_birthdays")
def get_birthdays(session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    data = EmployeeClass(db).get_birthdays()

    return {"message": data}

@employees.get("/get_genders_total")
def gender_totals(session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    data = EmployeeClass(db).gender_totals()

    return {"message": data}

@employees.post("/store")
def store(employee:Employee, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    employee_inputs = employee.dict()
    data = EmployeeClass(db).store(employee_inputs)

    return {"message": data}

@employees.get("/edit/{id}")
def edit(id:int, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    data = EmployeeClass(db).get("rut", id)

    return {"message": data}

@employees.delete("/delete/{id}")
def delete(id:int, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    data = EmployeeClass(db).delete(id)

    return {"message": data}

@employees.patch("/update/{id}")
def update(id: int, employee: UpdateEmployee, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    employee_inputs = employee.dict()
    
    data = EmployeeClass(db).update(id, employee_inputs)

    return {"message": data}

@employees.get("/validate_cellphone/{cellphone}")
def validate(cellphone: int, session_user: UserLogin = Depends(get_current_active_user), db: Session = Depends(get_db)):
    data = EmployeeClass(db).validate_cellphone(cellphone)

    return {"message": data}