import os

MONGO_URL = "mongodb://localhost:27017/"
DB_NAME = "Task_manager_db"
JWT_SECRET = os.getenv("JWT_SECRET", "Some-secret_key")
JWT_ALG = "HS256"
JWT_EXPIRE_SECONDS = 3600  # 1 hour