from pydantic import BaseModel, validator
from app.Database import db

URL_DB = db.urls

class Question_Model(BaseModel):
    msg: str
