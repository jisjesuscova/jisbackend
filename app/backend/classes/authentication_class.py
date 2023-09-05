from app.backend.db.models import UserModel
from fastapi import HTTPException, Depends
from app.backend.auth.auth_user import pwd_context, get_user
from datetime import datetime, timedelta
from typing import Union
import os
from jose import jwt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class AuthenticationClass:
    def __init__(self, db):
        self.db = db

    def authenticate_user(self, rut, password):
        user = get_user(rut)
        if not user:
            raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

        if not self.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
        return user
        
    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_token(self, data: dict, time_expire: Union[datetime, None] = None):
        data_copy = data.copy()
        if time_expire is None:
            expires = datetime.utcnow() + timedelta(minutes=30)
        else:
            expires = datetime.utcnow() + time_expire

        data_copy.update({"exp": expires})
        token_jwt = jwt.encode(data_copy, os.environ['SECRET_KEY'], algorithm=os.environ['ALGORITHM'])

        return token_jwt
    
    def forgot(self, data):
        print(data.email)

        return 1
    
    def forgot(self, data):
        # Configurar los detalles del correo
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Recupreación de contraseña'
        msg['From'] = 'info@jisparking.com'
        msg['To'] = data.email

        # Crear las partes del mensaje (versión de texto plano y versión HTML)
        text = "Este correo requiere un cliente de correo que admita HTML."
        html = "<html><body><h1>¡Hola!</h1><p>Este es un ejemplo de correo con diseño HTML.</p></body></html>"

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Adjuntar las partes al mensaje
        msg.attach(part1)
        msg.attach(part2)

        sender_email = 'info@jisparking.com'

        # Enviar el correo utilizando el servidor SMTP
        with smtplib.SMTP('mail.jisparking.com', 465) as server:
            server.login(sender_email, 'Macana11!')
            server.sendmail(sender_email, data.email, msg.as_string())


