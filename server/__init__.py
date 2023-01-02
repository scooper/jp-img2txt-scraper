from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from server.pages import init_pages
from server.api import init_api
from server.models import db

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///server.db?charset=utf8"
    app.config["UPLOAD_FOLDER"] = "/upload"
    app.secret_key = 'big secret!!!'

    db.init_app(app)

    init_api(app)
    init_pages(app)
    
    return app