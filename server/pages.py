from flask import Flask, render_template, request
import requests
import json
from server.models import db
from uuid import uuid4

def init_pages(app):
    @app.route("/")
    def index():
        return render_template("pages/index.html", title="Home")

    @app.route("/images")
    def images():
        response = requests.get(request.url_root + '/api/images')
        images = response.json()
        return render_template("pages/images.html", title="Images", images=images['images'])

    @app.route("/image")
    def image():
        return "To Implement"

    @app.route("/characters")
    def kanji():
        response = requests.get(request.url_root + '/api/characters')
        characters = response.json()
        return render_template("pages/kanji.html", title="Characters", characters=characters['characters'])

    @app.route("/character")
    def character():
        return "To Implement"

    @app.route("/createdb")
    def create_db():
        db.create_all()
        # example
        #char = Character(id=str(uuid4()), character="Hello")
        #db.session.add(char)
        db.session.commit()
        return "Created!"