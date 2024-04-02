# api-eq-int-elite-ms
Código Fuente backend-middleware creación los usuarios con Firebase para prueba técnica

Configuración del Entorno

Para configurar el entorno de desarrollo, sigue estos pasos:
1. Crear un Entorno Virtual

python -m venv venv

2. Activar el Entorno Virtual

venv\Scripts\activate

3. Instalar las Dependencias

pip install -r requirements.txt

Ejecutar el Servidor de Desarrollo

flask run

Al ejecutar flask run se ejecuta directamente en puerto 5000, funcional en web:
http://127.0.0.1:5000/

Acceder swagger:
http://127.0.0.1:5000/openapi/swagger#/

# APK
Instale https://ngrok.com/download
Descomprime el archivo y ejecuta ngrok.exe
Accede con tu cuenta y genera un authotoken, luego en el cmd donde se ejecutó ngrok.exe, configura:
ngrok config add-authtoken TU-TOKEN (reemplaza TU-TOKEN por el Authtoken)

Ejecuta en el mismo puerto que flask se encuentra: 
ngrok http 5000

En la sección de Forwarding se encuentra url https segura, ejemplo:
https://4c9b-2800-bf0-82ab-149-8d3a-88e3-f54e-4818.ngrok-free.app

Esta ruta se reemplaza en las url del archvio environment.prod.ts del front, ejemplo:
apiUrlRegisterUser: 'https://4c9b-2800-bf0-82ab-149-8d3a-88e3-f54e-4818.ngrok-free.app/register',
apiUrlLoginUser: 'https://4c9b-2800-bf0-82ab-149-8d3a-88e3-f54e-4818.ngrok-free.app/login',