"""Module for upload related routes."""
import os
from io import BytesIO

from botocore.exceptions import BotoCoreError, ClientError
from flask import Response, jsonify, make_response, request

from src.app.services.upload_service import UploadService
from src.app.upload import bp


@bp.route("/upload_profilepic", methods=["OPTIONS", "PUT"])
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

    filename = "profilepic_" + request.form["user_id"] + file_extension
    file_content = file.read()

    try:
        UploadService.upload_file_to_aws(
            BytesIO(file_content), filename, "AWS_BUCKET_NAME_PROFILEPICS"
        )
        return jsonify(
            {"message": "File uploaded successfully"}
        )  # Return success response
    except (BotoCoreError, ClientError) as e:
        response = {"message": "Error uploading file: {}".format(str(e))}
        return make_response(jsonify(response), 500)


@bp.route("/upload_companypic", methods=["OPTIONS", "PUT"])
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

    filename = "companypic_" + request.form["internship_id"] + file_extension

    file_content = file.read()

    try:
        UploadService.upload_file_to_aws(
            BytesIO(file_content), filename, "AWS_BUCKET_NAME_COMPANYPICS"
        )
        return jsonify(
            {"message": "File uploaded successfully"}
        )  # Return success response
    except (BotoCoreError, ClientError) as e:
        response = {"message": "Error uploading file: {}".format(str(e))}
        return make_response(jsonify(response), 500)


@bp.route("/upload_cv", methods=["OPTIONS", "PUT"])
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

    filename = "cv_" + request.form["user_id"] + file_extension
    file_content = file.read()

    try:
        UploadService.upload_file_to_aws(
            BytesIO(file_content), filename, "AWS_BUCKET_NAME_CVS"
        )
        return jsonify({"message": "File uploaded successfully"})
    except (BotoCoreError, ClientError) as e:
        response = {"message": "Error uploading file: {}".format(str(e))}
        return make_response(jsonify(response), 500)


@bp.route("/delete_profilepic", methods=["OPTIONS", "DELETE"])
def delete_profilepic() -> Response:
    """Delete profile pic from cloud container."""
    if request.method == "OPTIONS":
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    filename = "profilepic_" + request.form["user_id"]

    try:
        UploadService.delete_file_from_aws(filename, "AWS_BUCKET_NAME_PROFILEPICS")
        return jsonify({"message": "File deleted successfully"})
    except (BotoCoreError, ClientError) as e:
        response = {"message": "Error deleting file: {}".format(str(e))}
        return make_response(jsonify(response), 500)


@bp.route("/delete_companypic", methods=["OPTIONS", "DELETE"])
def delete_companypic() -> Response:
    """Delete company pic from cloud container."""
    if request.method == "OPTIONS":
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    filename = "companypic_" + request.form["internship_id"]

    try:
        UploadService.delete_file_from_aws(filename, "AWS_BUCKET_NAME_COMPANYPICS")
        return jsonify({"message": "File deleted successfully"})
    except (BotoCoreError, ClientError) as e:
        response = {"message": "Error deleting file: {}".format(str(e))}
        return make_response(jsonify(response), 500)


@bp.route("/delete_cv", methods=["OPTIONS", "DELETE"])
def delete_cv() -> Response:
    """Delete cv from cloud container."""
    if request.method == "OPTIONS":
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    filename = "cv_" + request.form["user_id"]

    try:
        UploadService.delete_file_from_aws(filename, "AWS_BUCKET_NAME_CVS")
        return jsonify({"message": "File deleted successfully"})
    except (BotoCoreError, ClientError) as e:
        response = {"message": "Error deleting file: {}".format(str(e))}
        return make_response(jsonify(response), 500)
