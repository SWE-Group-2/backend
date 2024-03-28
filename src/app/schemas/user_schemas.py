"""Marshmallow schemas for user related data."""
from marshmallow import Schema, fields, validate


class UserRegisterSchema(Schema):
    """Schema for user registration."""

    username = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    password = fields.Str(required=True, validate=validate.Length(min=8, max=255))


class UserLoginSchema(Schema):
    """Schema for user login."""

    username = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    password = fields.Str(required=True, validate=validate.Length(min=8, max=255))


class UserEditSchema(Schema):
    """Schema for editing user data."""

    first_name = fields.Str(validate=validate.Length(min=1, max=255))
    last_name = fields.Str(validate=validate.Length(min=1, max=255))
    gpa = fields.Float(required=True)
    academic_year = fields.Str(required=True)
    github_link = fields.Str(required=True)
    linkedin_link = fields.Str(required=True)
    website_link = fields.Str(required=True)
    profile_picture_link = fields.Str(required=True)
    email = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    description = fields.Str(required=True)
    internship_time_period_id = fields.Int(required=True)


class UserSchema(Schema):
    """Schema for user data."""

    id = fields.Int()
    username = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    gpa = fields.Float()
    academic_year = fields.Str()
    github_link = fields.Str()
    linkedin_link = fields.Str()
    website_link = fields.Str()
    profile_picture_link = fields.Str()
    email = fields.Str()
    phone_number = fields.Str()
    description = fields.Str()
    role_id = fields.Int()
    internship_time_period_id = fields.Int()
