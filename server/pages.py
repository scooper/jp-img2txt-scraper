from flask import Flask, render_template
from server.models import db, Character
from uuid import uuid4

def init_pages(app):
    @app.route("/")
    def index():
        return render_template("pages/index.html", title="Home")

    @app.route("/createdb")
    def create_db():
        db.create_all()
        # example
        #char = Character(id=str(uuid4()), character="Hello")
        #db.session.add(char)
        db.session.commit()
        return "Created!"