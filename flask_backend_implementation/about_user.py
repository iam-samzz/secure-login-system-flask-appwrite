from flask import jsonify,session

#local package
from models import Users,db,Profiles

def send_user_personal_data():
    #id's session data
    s1 = session.get("id")
    #is_auth session data
    s2 = session.get("is_auth")
    
    if s1 and s2:
        usr_id = session["id"]

        about_me = {}
        #usr's detail
        user_detail = db.session.execute(
            db.select(
                Users.id,
                Users.email
            ).where(Users.id == usr_id)).mappings().first()
        

        if user_detail:
            about_me["id"] = user_detail["id"]
            about_me["email"] = user_detail["email"]
        else:
            return jsonify({"error":"User not found"}),404

        profile_detail = db.session.execute(
            db.select(
                Profiles.full_name,
                Profiles.display_name,
                Profiles.bio,
                Profiles.created_at,
                Profiles.role
            ).where(Profiles.user_id == user_detail.id)
            ).mappings().first()

        if profile_detail:
            about_me["profile"] = {
                "fullname": profile_detail["full_name"],
                "displayName" : profile_detail["display_name"],
                "bio" : profile_detail["bio"],
                "createdAt" : profile_detail["created_at"],
                "role": profile_detail["role"]
            }
        return jsonify(about_me),200
    else:
        return jsonify({"error":"Not authenticated"}),401
