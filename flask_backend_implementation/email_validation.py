#validating email
from email_validator import validate_email, EmailNotValidError
from models import db,Users

def check_email(email):
    #...we need to check if the email is valid and the email is valid and the email is existing in the db
    try:
        validate_email(email,check_deliverability=False)
        
        #TODO: return TRUE if the already exising in the db
        #TODO: return "EMAIL-EXISTS"

        #checking in db
        user = db.session.execute(
            db.select(Users).where(Users.email == email)
        ).scalar_one_or_none()

        if user:
            return "EMAIL-EXISTS"

        return "VALID"
    except EmailNotValidError:
        #print(e)
        return "INVALID-EMAIL-FORMAT"

