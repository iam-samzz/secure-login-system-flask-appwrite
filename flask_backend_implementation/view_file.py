from flask import session,jsonify

from models import db,Files


def send_user_file_detail():

    usr_id = session.get("id")
    auth_status = session.get("is_auth")
    
    
    if usr_id and auth_status:

        file_details = db.session.execute(
            db.select(
                Files.id,
                Files.owner_id,
                Files.file_name,
                Files.mime_type,
                Files.size_byte,
                Files.uploaded_at
            ).where(Files.owner_id == usr_id)
        ).mappings()

        file_list= []
        for row in file_details:

            uploaded_at_str = row["uploaded_at"].strftime("%Y-%m-%dT%H:%M:%SZ") if row["uploaded_at"] else None

            file_list.append({
                "id": row["id"],
                "ownerId": row["owner_id"],
                "fileName": row["file_name"],
                "mimeType": row["mime_type"],
                "sizeBytes": row["size_byte"],
                "uploadedAt": uploaded_at_str
            })

        file_d = {
            "files" : file_list
        }

        return jsonify(file_d),200
    else:
        return jsonify({"error":"Not authenticated"}),401



def send_sepcific_file_detail(file_id):

    usr_id = session.get("id")
    if not usr_id:
        print("no user id")
    if not session.get("is_auth"):
        print("no is auth")
    if not usr_id or (not session.get("is_auth")):

        return jsonify({"error":"Not authenticated"}),401

    #fetch the file data bases on file_id
    file_data = db.session.execute(
        db.select(Files).where(Files.id == file_id)
    ).mappings().first()

    #file existence check
    if file_data:
        print(file_data["Files"].owner_id)
        #checking if the owener id of the file  is session usr id
        if file_data["Files"].owner_id == usr_id:
            formatted_date = file_data["Files"].uploaded_at.strftime("%Y-%m-%dT%H:%M:%SZ")

            result = {
                "file" : {
                    "id":file_data["Files"].id,
                    "ownerId":file_data["Files"].owner_id,
                    "fileName":file_data["Files"].file_name,
                    "mimeType":file_data["Files"].mime_type,
                    "sizeBytes":int(file_data["Files"].size_byte),
                    "uploadedAt":formatted_date
                }
            }

            return jsonify(result),200
        
        return jsonify({"error":"You do not have access to this file"}),403
    return jsonify({"error":"File not found"}),404

            

