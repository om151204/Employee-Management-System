import re

def check_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.fullmatch(pattern, email):
        return True
    return False

def check_contact(phone_number):
    pattern = r"/^(?:\+91|91|0)?[6-9]\d{9}$/"

    if re.fullmatch(pattern, phone_number):
        return True
    return False

def check_salary(salary):
    if float(salary)<0:
        return False
    return True