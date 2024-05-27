from pydantic import BaseModel

class Trainer(BaseModel):
    name: str
    town: str

    class Config:
        orm_mode = True  # If using ORMs, enable orm_mode to treat ORM models as dictionaries