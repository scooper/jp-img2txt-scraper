from flask import Flask, render_template, request, redirect, url_for
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
        response = requests.get(request.url_root + 'api/images')
        images = response.json()
        return render_template("pages/images.html", title="Images", images=images['images'])

    @app.route("/image")
    def image():
        if 'id' not in request.args:
            return redirect(url_for('images'))

        image_id = request.args['id']
        response = requests.get(request.url_root + 'api/image?image_id=' + image_id)
        image = response.json()
        return render_template("pages/image.html", title="Image", image=image['image'])

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