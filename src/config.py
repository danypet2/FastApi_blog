from dotenv import load_dotenv
import os


load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')

REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_HOST = os.environ.get('REDIS_HOST')

SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = os.environ.get('SMTP_PORT')

SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

SECRET_KEY = os.environ.get('SECRET_KEY')
