from fastapi import APIRouter, Depends
from app.backend.db.database import get_db
from sqlalchemy.orm import Session
from app.backend.db.models import EmployeeExtraModel
from app.backend.schemas import EmployeeExtra, UpdateEmployeeExtra

employee_extras = APIRouter(
    prefix="/employee_extras",
    tags=["Employee_Extras"]
)

@employee_extras.get("/")
def index(db: Session = Depends(get_db)):
    data = db.query(EmployeeExtraModel).all()

    return {"message": data}

@employee_extras.post("/store")
def store(employee_extra:EmployeeExtra, db: Session = Depends(get_db)):
    employee_extra_inputs = employee_extra.dict()
    data = EmployeeExtraModel(**employee_extra_inputs)

    db.add(data)
    db.commit()

    return {"message": data}

@employee_extras.get("/edit/{rut}")
def edit(rut:int, db: Session = Depends(get_db)):
    data = db.query(EmployeeExtraModel).filter(EmployeeExtraModel.rut == rut).first()

    return {"message": data}

@employee_extras.delete("/delete/{id}")
def delete(rut:int, db: Session = Depends(get_db)):
    data = db.query(EmployeeExtraModel).filter(EmployeeExtraModel.rut == rut)

    if not data.first():
        return {"message": "Datos no encontrados!"}
    
    data.delete(synchronize_session=False)

    db.commit()

    return {"message": "Datos eliminados!"}

@employee_extras.patch("/update/{rut}")
def update(rut:int, employee:UpdateEmployeeExtra, db: Session = Depends(get_db)):
    existing_employee = db.query(EmployeeExtraModel).filter(EmployeeExtraModel.rut == rut).one_or_none()

    if not existing_employee:
        return {"message": "Empleado no encontrado!"}

    existing_employee_data = employee.dict(exclude_unset=True)
    for key, value in existing_employee_data.items():
        setattr(existing_employee, key, value)

    db.commit()

    return {"message": "Empleado actualizado", "data": existing_employee}