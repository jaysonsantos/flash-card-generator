import pytest
from flask import Flask
from flask.testing import Client

from learning.clients.web import create_app


@pytest.yield_fixture()
def app():
    app_: Flask = create_app()
    app_.config["SERVER_NAME"] = "testserver"
    app_.testing = True
    ctx = app_.app_context()
    ctx.push()
    yield app_
    ctx.pop()


@pytest.yield_fixture()
def test_client(app):
    yield app.test_client()
