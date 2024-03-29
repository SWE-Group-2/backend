"""Module for upload related routes."""
from io import BytesIO

from flask import Response, jsonify, make_response, request

from src.app.services.upload_service import UploadService
from src.app.upload import bp


@bp.route("/upload", methods=["OPTIONS", "PUT"])
def upload() -> Response:
    """Upload file to cloud."""
    if request.method == "OPTIONS":
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    file = request.files["file"]
    filename = request.form["filename"]
    file_content = file.read()

    try:
        UploadService.upload_file_to_aws(BytesIO(file_content), filename)
        return jsonify(
            {"message": "File uploaded successfully"}
        )  # Return success response

    except Exception:
        response = {"message": "Error uploading file"}
        return make_response(jsonify(response), 500)
