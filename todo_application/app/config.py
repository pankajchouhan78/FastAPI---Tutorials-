import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database URL
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    # Secret key for JWT token generation
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Azure AD Configuration
    AZURE_TENANT_ID = os.getenv('AZURE_TENANT_ID')
    AZURE_CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
    AZURE_CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')
    
    # JWT token settings
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
