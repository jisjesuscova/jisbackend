from fastapi import APIRouter, Depends
from app.backend.schemas import UserLogin, GetCollection
from app.backend.classes.collection_class import CollectionClass
from app.backend.auth.auth_user import get_current_active_user

collections = APIRouter(
    prefix="/collections",
    tags=["Collections"]
)

@collections.post("/total")
def total(user: GetCollection, session_user: UserLogin = Depends(get_current_active_user)):
    user_inputs = user.dict()
    print(user_inputs)
    data = CollectionClass.get_total(user_inputs)

    return {"message": data}