import os
class Config:
    SECRET_KEY = '1233'


class DevelomentConfig(Config):
    DEBUG = True
    # Configuración BD
    MYSQL_HOST = '127.0.0.1'
    MYSQL_USER = 'devpy'
    MYSQL_PASSWORD = 'P@s5word*123'
    MYSQL_DB = 'db_appxtrim'

    # Configuración del servidor de correo electrónico
    EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
    

class ProductionConfig(Config):
    DEBUG = True
    # Configuración BD
    MYSQL_HOST = '192.168.21.18'
    MYSQL_USER = 'usr_ecomerce'
    MYSQL_PASSWORD = 'usr_ecomerce'
    MYSQL_DB = 'ecomerce'

    # Configuración del servidor de correo electrónico
    EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

   
config = {
    'development' : DevelomentConfig,
    'prod' : ProductionConfig
}