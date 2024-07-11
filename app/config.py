import os

class Config:
    # SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    SQLALCHEMY_DATABASE_URI = f"postgresql://postgres.mnnjqlkqfsilirxfiphz:{os.getenv('DB_PASS')}@aws-0-sa-east-1.pooler.supabase.com:6543/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET')