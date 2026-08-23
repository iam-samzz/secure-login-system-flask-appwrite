import json
# we need to load the json file
# since the given json file is small, we are using load
# if the file is big, then wwe can use bigjson/ijson package..

from datetime import datetime
from pass_hash import generate_password_hash
from models import db,Users,Profiles,Files

def seed_data_into_db():

    with open("seed-data.json","r") as file:
        
        data = json.load(file)


    for user in data["users"]:

        passwd = generate_password_hash(user["password"])
        if passwd["success"] == True:
            hash_pass = passwd.get("password")
        else:
            #skipping the user data if the password cannot hashed
            continue


        #inserting the user
        try:
            new_user = Users(
                id = user["id"],
                email = user["email"],
                password = hash_pass
                )
        
            db.session.add(new_user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            continue

        
        try:
            profile = user["profile"]

            new_prof = Profiles(
                full_name=profile.get("fullName"),
                display_name=profile.get("displayName"),
                bio=profile.get("bio"),
                created_at=profile.get("createdAt"),
                role=profile.get("role"),
                user_id=new_user.id
            )

            db.session.add(new_prof)
            db.session.commit()
        except Exception:
            db.session.rollback()

        #iterating files details
        for file in user["files"]:

            #each file is {...}
            # so for each loop, we are inserting a file data
            try:

                new_file = Files(
                    id = file["id"],
                    file_name = file.get("fileName"),
                    mime_type = file.get("mimeType"),
                    size_byte = file.get("sizeBytes"),
                    uploaded_at = file.get("uploadedAt"),
                    owner_id = new_user.id
                )
                db.session.add(new_file)
                db.session.commit()
            except Exception:
                db.session.rollback()
                continue

