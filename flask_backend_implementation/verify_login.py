from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

#local module
from models import Users,db
ph = PasswordHasher()

def check_acc(input_email,input_passwd):

    #check for email in the db
    email_status = db.session.execute(
        db.select(Users).where(Users.email == input_email)
    ).scalar_one_or_none()

    if not email_status:
        return False

    password = db.session.execute(
        db.select(Users.password).where(Users.email == input_email)
    ).scalar_one_or_none()
    try:
        ph.verify(password,input_passwd)
        return True
    except VerifyMismatchError:
        return False
    
