from fastapi import APIRouter, Depends
from app.backend.schemas import UserLogin, GetDte
from app.backend.classes.dte_class import DteClass
from app.backend.auth.auth_user import get_current_active_user

dtes = APIRouter(
    prefix="/dtes",
    tags=["Dtes"]
)

@dtes.post("/total_quantity")
def total_quantity(user: GetDte, session_user: UserLogin = Depends(get_current_active_user)):
    user_inputs = user.dict()
    data = DteClass.get_total_quantity(user_inputs)

    return {"message": data}

@dtes.post("/total_amount")
def total_amount(user: GetDte, session_user: UserLogin = Depends(get_current_active_user)):
    user_inputs = user.dict()
    data = DteClass.get_total_amount(user_inputs)

    return {"message": data}