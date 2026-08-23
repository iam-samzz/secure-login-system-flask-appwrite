from flask import Flask,render_template,jsonify,request,session
from dotenv import load_dotenv
import os
import uuid
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS



#local modules
import pass_hash
from models import db,AppSettings,Users,Files
from seed import seed_data_into_db
from email_validation import check_email
from verify_login import check_acc
from about_user import send_user_personal_data
from view_file import send_user_file_detail,send_sepcific_file_detail
#------
#loading env
load_dotenv()


app = Flask(__name__)

CORS(app,supports_credentials=True)
#configuring the db address
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

#from sql alchemy object, we are initializing the app
#this initilize the db object with DATABASE URL
db.init_app(app)

with app.app_context():

    db.create_all()

    settings = db.session.get(AppSettings, 1)

    if settings is None:
        settings = AppSettings(
            id=1,
            seed_completed=False
        )

        db.session.add(settings)
        db.session.commit()

    if not settings.seed_completed:
        seed_data_into_db()

        settings.seed_completed = True
        db.session.commit()


limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[]
)


#-------------------------------

@app.route("/")

def func():
    return render_template("index.html")


#registration route
@app.route("/register",methods=['POST'])
def register():

    new_user_data = request.get_json()
    #print(new_user_data)

    if not new_user_data:
        return jsonify({
            "error": "Request body must contain JSON"
        }), 400


    email = new_user_data.get("email")
    password = new_user_data.get("password")

    if not email or not password:
        return jsonify({"error":"email and password are required"}), 400
    email_status = check_email(email)

    #checking email..
    if email_status == "VALID":
        # now, email is completely valid and not in the db
                
        hash_result = pass_hash.generate_password_hash(password)

        if "error" in hash_result:
            return jsonify({"error":hash_result["error"]}),500

        #validating..
        if ("success" in hash_result) and hash_result["success"] == True :

            # update password to to db
            
            hashed_actual_password = hash_result.get("password")
            new_user = Users(
                id = str(uuid.uuid4()),
                email = email,
                password = hashed_actual_password
            )
            try:
                db.session.add(new_user)
                db.session.commit()

            except Exception:
                db.session.rollback()

                return jsonify({
                    "error": "Internal server error"
                }), 500

            #add to table
            return jsonify({"id":new_user.id,"email":new_user.email}),200
        
    elif email_status == "EMAIL-EXISTS":
        #email format is valid, but already exists
        return jsonify({"error":"an account with this email already exists."}),409
    
    elif email_status == "INVALID-EMAIL-FORMAT":
        return jsonify({"error":"Unprocessable Content","message":"Validation failed"}),422,



@app.route("/login", methods=['POST'])
@limiter.limit("5 per 10 seconds", error_message="Too many attempts. Try again after 5 sec.")
def login():
    # get the credentils.
    credentials = request.get_json()
    

    session["login_failed"] = 0
    
    if not credentials:
        return jsonify({"error":"Invalid email or password"}),401

    email = credentials.get("email")
    password = credentials.get("password")

    login_status = check_acc(email,password)
    if login_status:
        user_detail = db.session.execute(
            db.select(
                Users.email,
                Users.id
            ).where(Users.email == email)
        ).first()

        #storing sessions
        session["email"] = email
        session["is_auth"] = True
        session["id"] = user_detail.id

        return jsonify({"id":f"{user_detail.id}", "email":f"{user_detail.email}"}),200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

#for reurning too many attempts
@app.errorhandler(429)
def l_handler(e):
    return jsonify({"error":"Too many attempts. Try again after 5 sec"}),429

@app.errorhandler(500)
def e_handler(e):
    return jsonify({"error":"Server Not Found"})




@app.route("/logout",methods=["POST"])
def logout():
    if not session:
        return jsonify({"message":"You are already logged out"}),200
    session.clear()
    return jsonify({"message":"Logged out"}),200


@app.route("/me",methods=["GET"])
def myself():
    #from about_user.py
    return send_user_personal_data()



@app.route("/files",methods = ["GET"])
def files():
    #we are  looking local session to see wheather the user is logged in or not.
    #..if yes, then we fetch data from db and show details of all the files

    #from view_file.py
    return send_user_file_detail()
    

@app.route("/files/<file_id>",methods=["GET"])
def show_file_by_id(file_id):
    #get file id
    #get the session's user id
    #find the file
    #if that file's owner id is session's id
        #then return file detail
    # if that file is user is someone else
        #return not auth
    #if that file dint exists, return 404

    #implemented in view_file.py
    return send_sepcific_file_detail(file_id)
from flask import Response, jsonify, session

@app.route('/files/<file_id>/download', methods=['GET'])
def download_file(file_id):
    usr_id = session.get("id")
    is_auth = session.get("is_auth")
    
    if not usr_id or not is_auth:
        return "Not authenticated", 401

    file_data = db.session.execute(
        db.select(Files).where(Files.id == file_id)
    ).mappings().first()

    if not file_data:
        return "File not found", 404

    f = file_data["Files"]

    if f.owner_id != usr_id:
        return "You do not have access to this file", 403

    #creting a mock text
    mock_text = f'This is a mock stand-in for "{f.file_name}" ({f.mime_type}, {f.size_byte} bytes).\nIn the real backend this endpoint would stream the actual file bytes.'

    #it sends the responce as file
    return Response(
        mock_text,
        mimetype=f.mime_type, 
        headers={'Content-Disposition': f'attachment; filename="{f.file_name}"'}
    )
if __name__ == "__main__":
    app.run(debug=False)


