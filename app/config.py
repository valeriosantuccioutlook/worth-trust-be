import os

DB_URI = os.getenv("DB_URI")

if DB_URI is None:
    DB_URI = (
        DB_URI
    ) = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PSW')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
