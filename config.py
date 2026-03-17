import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("postgresql://oop_db_7dol_user:bVjSnbt6rLaSqA1VO98M7vKjrsjyyIA3@dpg-d6sfg375gffc738in6sg-a/oop_db_7dol")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your_secret_key"

    # //postgresql://oop_db_7dol_user:bVjSnbt6rLaSqA1VO98M7vKjrsjyyIA3@dpg-d6sfg375gffc738in6sg-a/oop_db_7dol