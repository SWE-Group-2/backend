import os
import typing

import pytest
from flask import Flask
from flask.testing import FlaskClient

from src.app import create_app
from src.app.extensions import db

basedir = os.path.abspath(os.path.dirname(__file__))


class TestConfig:
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URI"
    ) or "sqlite:///" + os.path.join(basedir, "test.db")


@pytest.fixture(scope="session")
def app() -> typing.Generator[Flask, None, None]:
    app = create_app(config=TestConfig)
    with app.app_context():
        yield app


@pytest.fixture(scope="function")
def test_client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture(scope="session")
def test_db(app: Flask, request: pytest.FixtureRequest) -> db:
    """Session-wide test database."""

    def teardown():
        db.drop_all()

    db.app = app
    db.create_all()
    request.addfinalizer(teardown)
    return db


@pytest.fixture(scope="function")
def session(test_db: db, request: pytest.FixtureRequest) -> db.session:
    db.session.begin_nested()

    def commit():
        db.session.flush()
        # patch commit method

    old_commit = db.session.commit
    db.session.commit = commit

    def teardown():
        db.session.rollback()
        db.session.close()
        db.session.commit = old_commit

    request.addfinalizer(teardown)
    return db.session