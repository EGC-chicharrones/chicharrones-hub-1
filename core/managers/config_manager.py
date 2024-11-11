import os
import secrets


class ConfigManager:
    def __init__(self, app):
        self.app = app

    def load_config(self, config_name='development'):
        # If config_name is not provided, use the environment variable FLASK_ENV
        if config_name is None:
            config_name = os.getenv('FLASK_ENV', 'development')

        # Load configuration
        if config_name == 'testing':
            self.app.config.from_object(TestingConfig)
        elif config_name == 'production':
            self.app.config.from_object(ProductionConfig)
        else:
            self.app.config.from_object(DevelopmentConfig)


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_bytes())
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('MARIADB_USER', 'default_user')}:"
        f"{os.getenv('MARIADB_PASSWORD', 'default_password')}@"
        f"{os.getenv('MARIADB_HOSTNAME', 'localhost')}:"
        f"{os.getenv('MARIADB_PORT', '3306')}/"
        f"{os.getenv('MARIADB_DATABASE', 'default_db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Configuración de correo electrónico
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = os.getenv('MAIL_PORT', 587)
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'chicharroneshub@gmail.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'vofd qmkw ipld vrwo')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', MAIL_USERNAME)
    TIMEZONE = 'Europe/Madrid'
    TEMPLATES_AUTO_RELOAD = True
    UPLOAD_FOLDER = 'uploads'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('MARIADB_USER', 'default_user')}:"
        f"{os.getenv('MARIADB_PASSWORD', 'default_password')}@"
        f"{os.getenv('MARIADB_HOSTNAME', 'localhost')}:"
        f"{os.getenv('MARIADB_PORT', '3306')}/"
        f"{os.getenv('MARIADB_TEST_DATABASE', 'default_db')}"
    )
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
