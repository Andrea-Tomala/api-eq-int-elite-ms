from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_openapi3 import OpenAPI, Info, Tag, Parameter, RequestBody
from pydantic import BaseModel, Field


#Instancia swagger
info = Info(title="api-eqintelite-ms", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


# Inicializar Firebase Admin SDK
cred = credentials.Certificate("credentials/equipo-interno-elite-firebase-adminsdk-kxpzn-3f9b63f3f6.json")  # Cambia por la ruta de tu archivo JSON de credenciales
firebase_admin.initialize_app(cred)



class RegisterBody(BaseModel):
    email: str
    nombre: str
    contrasena: str

class RegisterResponse(BaseModel):
    code: int = Field(0, description="Código de estado")
    message: str = Field("OK", description="Mensaje de respuesta")

class SessionBody(BaseModel):
    email: str
    contrasena: str

class SessionResponse(BaseModel):
    code: int = Field(0, description="Código de estado")
    message: str = Field("OK", description="Mensaje de respuesta")

@app.route('/')

def Index():
    return 'Bienvenido a Equipo Interno Élite api'

# Función para registrar un nuevo usuario con Firebase Authentication
def registrar_usuario(email, contrasena):
    try:
        # Crear el usuario en Firebase Authentication
        usuario = auth.create_user(
            email=email,
            password=contrasena,
            email_verified=False  # Indicar que el correo electrónico no está verificado inicialmente
        )
        # Enviar correo electrónico de verificación
        #auth.send_email_verification(usuario.email)
        #auth.generate_email_verification_link(usuario.email)
        print("Usuario registrado exitosamente. Se ha enviado un correo de verificación a", usuario.email)
        return True
    except auth.UserNotFoundError:
        # No se encontró un usuario existente con este correo electrónico
        return False
    except Exception as e:
        # Otras excepciones
        raise e
    

reg_tag = Tag(name="Registro de usuario", description="Creación de Usuarios por Firebase")

# Ruta para registro de usuario
@app.post("/registro", summary="Registro de usuarios desde la app", tags=[reg_tag],
         responses = {
            200: RegisterResponse,
            422: None       
         })
def registro(body: RegisterBody):
    email = body.email
    nombre = body.nombre
    contrasena = body.contrasena

    try:
        # Verificar que se proporcionen datos válidos
        if not nombre or not email or not contrasena:
            return jsonify({'code': 400, 'message': 'Se requieren correo electrónico y contraseña para registrarse'}), 400
        # Crear usuario en Firebase Authentication
        if not registrar_usuario(email, contrasena):
            return jsonify({'code': 400, 'message': 'El correo electrónico ya está registrado.'}), 400
        return jsonify({'code': 200, 'message': 'Usuario registrado exitosamente.'}), 200

    except Exception as e:
        return jsonify({'code': 500, 'message': 'Error al registrar usuario: ' + str(e)}), 500


# Ruta para inicio de sesión
session_tag = Tag(name="Inicio de sesión de usuarios", description="Acceso de usuarios registrados")
# Ruta para registro de usuario
@app.post("/login", summary="Acceso de usuarios registrados en la app", tags=[session_tag],
         responses = {
            200: SessionResponse,
            422: None       
         })
def login(body: SessionBody):
    email = body.email
    contrasena = body.contrasena

    try:
        # Verificar que se proporcionen datos válidos
        if not email or not contrasena:
            return jsonify({'code': 400, 'message': 'Se requieren correo electrónico y contraseña para iniciar sesión'}), 400

        # Verificar si el correo electrónico está registrado en Firebase Authentication
        try:
            usuario = auth.get_user_by_email(email)
        except auth.UserNotFoundError:
            return jsonify({'code': 400, 'message': 'El correo electrónico no está registrado'}), 400
        
        # Autenticar al usuario con Firebase Authentication
        try:
            auth.sign_in_with_email_and_password(email, contrasena)
            return jsonify({'mensaje': 'Inicio de sesión exitoso.'}), 200
        except Exception as e:
            # Capturar cualquier excepción genérica y manejarla
            error_message = str(e)
            if 'INVALID_PASSWORD' in error_message:
                return jsonify({'code': 400, 'message': 'Contraseña incorrecta'}), 400
            else:
                return jsonify({'mensaje': 'Error al iniciar sesión: ' + error_message}), 400

    except Exception as e:
        return jsonify({'mensaje': 'Error al iniciar sesión: ' + str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
