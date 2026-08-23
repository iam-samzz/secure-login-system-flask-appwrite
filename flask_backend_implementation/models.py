from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = "users"


    #user_id = db.Column(db.Text,primary_key=True,nullable=False)
    id = db.Column(db.String(40), primary_key=True,nullable=False)
    #user_id = db.Column(db.Text, unique=True,nullable=False)
    email = db.Column(db.Text,unique=True,nullable=False)
    password = db.Column(db.Text,nullable=False)

class Profiles(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer,primary_key = True)

    full_name = db.Column(db.Text,nullable=False)
    display_name = db.Column(db.Text,nullable=False)
    bio = db.Column(db.Text,nullable=False)
    created_at = db.Column(db.DateTime(timezone = False),default=db.func.now(), nullable=False)
    role = db.Column(db.String(20),nullable = False)

    #foreign key
    user_id = db.Column(db.String(40),db.ForeignKey("users.id"),nullable = False)

class Files(db.Model):
    __tablename__ = "files"

    id = db.Column(db.String(40),primary_key = True)
    file_name = db.Column(db.Text, nullable = False)
    mime_type = db.Column(db.Text, nullable = False)
    size_byte = db.Column(db.BigInteger,nullable = False)
    uploaded_at = db.Column(db.DateTime(timezone = False),
                            default = db.func.now(),
                             nullable = False)

    #foreign key
    owner_id = db.Column(db.String(40),db.ForeignKey("users.id"),nullable=False)

class AppSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seed_completed = db.Column(db.Boolean, default=False, nullable=False)