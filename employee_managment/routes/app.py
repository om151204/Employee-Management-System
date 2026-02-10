from employee_managment.database import create_tables, get_db, Employee
from fastapi import FastAPI, Depends, HTTPException, status
from employee_managment.routes.base_model import EmployeeModel, PatchEmployeeModel
from sqlalchemy.orm import Session

from employee_managment.routes.validation import check_email, check_contact, check_salary

app = FastAPI()

if not create_tables():
    create_tables()


@app.get("/", tags=["Welcome Page"], status_code=status.HTTP_200_OK)
def welcome_message():
    return {"message": "Welcome to Employee Managment"}


@app.get("/employees", tags=["Employees Data Retrival"], status_code=status.HTTP_200_OK)
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    if not employees:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return employees


@app.get("/employees/{employee_id}", tags=["Employees Data Retrival"], status_code=status.HTTP_200_OK)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee:
        return employee
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.post("/employees", tags=["Employees Data Insertion"], status_code=status.HTTP_201_CREATED)
def add_employee(request: EmployeeModel, db: Session = Depends(get_db)):
    if not check_email(request.email):
        return HTTPException(detail="Invalid email", status_code=status.HTTP_400_BAD_REQUEST)
    if not check_contact(request.phone_number):
        return HTTPException(detail="Invalid contact", status_code=status.HTTP_400_BAD_REQUEST)
    if not check_salary(request.salary):
        return HTTPException(detail="Invalid salary", status_code=status.HTTP_400_BAD_REQUEST)
    employee = Employee(name=request.name, email=request.email, department=request.department, salary=request.salary,
                        phone_number=request.phone_number, is_active=request.is_active)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


@app.put("/employees/{employee_id}", tags=["Employees PUT Request"], status_code=status.HTTP_200_OK)
def put_employees(request: EmployeeModel, employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee:
        employee.name = request.name
        employee.email = request.email
        employee.department = request.department
        employee.salary = request.salary
        employee.phone_number = request.phone_number
        employee.is_active = request.is_active
        db.commit()
        db.refresh(employee)
        return employee
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.delete("/employees/{employee_id}", tags=["Employees Patch Request"], status_code=status.HTTP_200_OK)
def delete_employees(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id)
    if employee:
        employee.delete()
        db.commit()
        return f"Employee {employee_id} has been deleted"
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.patch("/employees/{employee_id}", tags=["Employees Data Delection"], status_code=status.HTTP_200_OK)
def patch_employees(request: PatchEmployeeModel, employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee:
        employee.is_active = request.is_active
        db.commit()
        db.refresh(employee)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
