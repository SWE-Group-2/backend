"""Wrappers for request body validation and response serialization (courtesy of copilot)."""
from functools import wraps

from flask import jsonify, make_response, request
from marshmallow import ValidationError


def handle_validation(schema):  # noqa: ANN001, ANN201
    """Make decorator to handle request body validation."""

    def decorator(f):  # noqa: ANN001, ANN201
        @wraps(f)  # noqa: ANN201
        def wrapper(*args, **kwargs):  # noqa: ANN001, ANN201
            try:
                data = schema.load(request.json)
            except ValidationError as error:
                response = {"message": "Invalid request body", "errors": error.messages}
                return make_response(jsonify(response), 400)
            return f(data, *args, **kwargs)

        return wrapper

    return decorator
