from app.backend.db.models import UserModel
from app.backend.auth.auth_user import generate_bcrypt_hash
from datetime import datetime
from app.backend.classes.helper_class import HelperClass

class UserClass:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        try:
            data = self.db.query(UserModel).order_by(UserModel.id).all()
            if not data:
                return "No data found"
            return data
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
    
    def get(self, field, value):
        try:
            data = self.db.query(UserModel).filter(getattr(UserModel, field) == value).first()
            return data
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
    
    def store(self, user_inputs):
        numeric_rut = HelperClass().numeric_rut(user_inputs['rut'])
        nickname = HelperClass().nickname(user_inputs['names'], user_inputs['father_lastname'])

        user = UserModel()
        user.rut = numeric_rut
        user.rol_id = 1
        user.clock_rol_id = user_inputs['clock_rol_id']
        user.status_id = 1
        user.visual_rut = user_inputs['rut']
        user.nickname = nickname
        user.hashed_password = generate_bcrypt_hash(user_inputs['password'])
        user.disabled = 0
        user.added_date = datetime.now()
        user.updated_date = datetime.now()

        self.db.add(user)
        try:
            self.db.commit()

            return 1
        except Exception as e:
            return 0
        
    def delete(self, id):
        try:
            data = self.db.query(UserModel).filter(UserModel.rut == id).first()
            if data:
                self.db.delete(data)
                self.db.commit()
                return 1
            else:
                return "No data found"
        except Exception as e:
            error_message = str(e)
            return f"Error: {error_message}"
        
    def update(self, id, user_inputs):
        user = self.db.query(UserModel).filter(UserModel.rut == id).one_or_none()

        if 'rut' in user_inputs and user_inputs['rut'] is not None:
            numeric_rut = HelperClass().numeric_rut(user_inputs['rut'])
            user.rut = numeric_rut

        if 'rol_id' in user_inputs and user_inputs['rol_id'] is not None:
            user.rol_id = user_inputs['rol_id']

        if 'clock_rol_id' in user_inputs and user_inputs['clock_rol_id'] is not None:
            user.clock_rol_id = user_inputs['clock_rol_id']
        
        if 'status_id' in user_inputs and user_inputs['status_id'] is not None:
            user.status_id = user_inputs['status_id']

        if 'rut' in user_inputs and user_inputs['rut'] is not None:
            user.visual_rut = user_inputs['rut']

        if 'names' in user_inputs and user_inputs['names'] is not None and 'father_lastname' in user_inputs and user_inputs['father_lastname'] is not None:
            nickname = HelperClass().nickname(user_inputs['names'], user_inputs['father_lastname'])
            user.nickname = nickname

        if 'password' in user_inputs and user_inputs['password'] is not None:
            user.hashed_password = generate_bcrypt_hash(user_inputs['password'])
        
        if 'disabled' in user_inputs and user_inputs['disabled'] is not None:
            user.disabled = user_inputs['disabled']

        user.updated_date = datetime.now()

        self.db.add(user)
        try:
            self.db.commit()

            return 1
        except Exception as e:
            return 0