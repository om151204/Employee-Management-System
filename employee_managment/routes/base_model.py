from pydantic import BaseModel, EmailStr, StrictStr, StrictInt, StrictFloat, StrictBool
from typing import Optional
class EmployeeModel(BaseModel):
    name: str
    email: EmailStr
    department: str
    salary: float
    phone_number: str
    is_active: bool

class PatchEmployeeModel(EmployeeModel):
    name : Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    salary: Optional[float] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = False

    class Config:
        orm_mode = True             ## To access the database