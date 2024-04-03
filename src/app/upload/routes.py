"""Module for upload related routes."""
import os
from io import BytesIO

from botocore.exceptions import BotoCoreError, ClientError
from flask import Response, jsonify, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.app.services.upload_service import UploadService
from src.app.services.user_service import UserService
from src.app.upload import bp


@bp.route("/upload_profilepic", methods=["OPTIONS", "PUT"])
@jwt_required()
def upload_profilepic() -> Response:
    """Upload profile picture file to cloud container."""
    if request.method == "OPTIONS":
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    file = request.files["file"]
    allowed_extensions = {"png", "jpg", "jpeg", "gif"}
    filename, file_extension = os.path.splitext(file.filename)

    if file_extension[1:] not in allowed_extensions:
        return jsonify({"error": "Invalid file format. Only image files are allowed."})

    filename = f"profilepic_{get_jwt_identity()}{file_extension}"
    file_content = file.read()

    try:
        UploadService.upload_file_to_aws(
            BytesIO(file_content), filename, "AWS_BUCKET_NAME_PROFILEPICS", "image/png"
        )
        return jsonify(
            {"message": "File uploaded successfully"}
        )  # Return success response
    except (BotoCoreError, ClientError) as e:
        response = {"message": "Error uploading file: {}".format(str(e))}
        return make_response(jsonify(response), 500)


@bp.route("/upload_companypic", methods=["OPTIONS", "PUT"])
@jwt_required()
def upload_companypic() -> Response:
    """Upload company picture file to cloud container."""
    if request.method == "OPTIONS":
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    file = request.files["file"]
    allowed_extensions = {"png", "jpg", "jpeg", "gif"}
    filename, file_extension = os.path.splitext(file.filename)

    if file_extension[1:] not in allowed_extensions:
        return jsonify({"error": "Invalid file format. Only image files are allowed."})

    filename = f"companypic_{request.form['internship_id']}{file_extension}"

    file_content = file.read()

    try:
        UploadService.upload_file_to_aws(
            BytesIO(file_content), filename, "AWS_BUCKET_NAME_COMPANYPICS", "image/png"
        )
        return jsonify(
            {"message": "File uploaded successfully"}
        )  # Return success response
    except (BotoCoreError, ClientError) as e:
        response = {"message": "Error uploading file: {}".format(str(e))}
        return make_response(jsonify(response), 500)


@bp.route("/upload_cv", methods=["OPTIONS", "PUT"])
@jwt_required()
def upload_cv() -> Response:
    """Upload cv file to cloud container."""
    if request.method == "OPTIONS":
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    file = request.files["file"]
    allowed_extensions = {"pdf", "docx"}
    filename, file_extension = os.path.splitext(file.filename)

    if file_extension[1:] not in allowed_extensions:
        return jsonify(
            {"error": "Invalid file format. Only pdf or docx files are allowed."}
        )

    filename = f"cv_{get_jwt_identity()}{file_extension}"
    file_content = file.read()

    try:
        UploadService.upload_file_to_aws(
            BytesIO(file_content), filename, "AWS_BUCKET_NAME_CVS", "application/pdf"
        )
        return jsonify({"message": "File uploaded successfully"})
    except (BotoCoreError, ClientError) as e:
        response = {"message": "Error uploading file: {}".format(str(e))}
        return make_response(jsonify(response), 500)


@bp.route("/delete_profilepic", methods=["OPTIONS", "DELETE"])
@jwt_required()
def delete_profilepic() -> Response:
    """Delete profile pic from cloud container."""
    if request.method == "OPTIONS":
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    filename = f"profilepic_{get_jwt_identity()}"

    try:
        UploadService.delete_file_from_aws(filename, "AWS_BUCKET_NAME_PROFILEPICS")
        UserService.clear_profile_picture(user_id=get_jwt_identity())
        return jsonify({"message": "File deleted successfully"})
    except (BotoCoreError, ClientError) as e:
        response = {"message": "Error deleting file: {}".format(str(e))}
        return make_response(jsonify(response), 500)


@bp.route("/delete_companypic", methods=["OPTIONS", "DELETE"])
@jwt_required()
def delete_companypic() -> Response:
    """Delete company pic from cloud container."""
    if request.method == "OPTIONS":
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    filename = f"companypic_{request.form['internship_id']}"

    try:
        UploadService.delete_file_from_aws(filename, "AWS_BUCKET_NAME_COMPANYPICS")
        return jsonify({"message": "File deleted successfully"})
    except (BotoCoreError, ClientError) as e:
        response = {"message": "Error deleting file: {}".format(str(e))}
        return make_response(jsonify(response), 500)


@bp.route("/delete_cv", methods=["OPTIONS", "DELETE"])
@jwt_required()
def delete_cv() -> Response:
    """Delete cv from cloud container."""
    if request.method == "OPTIONS":
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    filename = f"cv_{get_jwt_identity()}"

    try:
        UploadService.delete_file_from_aws(filename, "AWS_BUCKET_NAME_CVS")
        UserService.clear_cv(user_id=get_jwt_identity())
        return jsonify({"message": "File deleted successfully"})
    except (BotoCoreError, ClientError) as e:
        response = {"message": "Error deleting file: {}".format(str(e))}
        return make_response(jsonify(response), 500)
