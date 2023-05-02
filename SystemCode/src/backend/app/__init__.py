import logging
from os import environ
from dotenv import load_dotenv

from flask import Flask, request as req
from flask_restful import Api
from flask_cors import CORS, cross_origin

from app.config import config as app_config
from app.routes import initialize_routes

from app.errors import errors
from app.db import db

from flask_seeder import FlaskSeeder


def register_extensions(app):
    db.init_app(app)\
        # Seed DB
    seeder = FlaskSeeder()
    seeder.init_app(app, db)


def create_app():
    load_dotenv()
    APPLICATION_ENV = get_environment()
    app = Flask(app_config[APPLICATION_ENV].APP_NAME)
    app.config.from_object(app_config[APPLICATION_ENV])

    register_extensions(app)

    # CORS
    CORS(app, allow_headers=[
        "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
        supports_credentials=True)
    app.config['CORS_HEADERS'] = 'Content-Type'

    api = Api(app, errors=errors)
    initialize_routes(api)

    app.logger.setLevel(logging.NOTSET)

    return app


def get_environment():
    return environ.get('APPLICATION_ENV') or 'development'
