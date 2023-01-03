from flask import Flask, request, redirect
from flask_restful import Resource, Api
import os
from server.models import Image
from server.models import Character

class CharacterResource(Resource):
    def get(self):
        # all characters
        return

    def put(self):
        # receive character and image reference, 
        return

class ImageResource(Resource):
    def get(self, image_id):
        if image_id == None or image_id == "":
            # get all
            return
        return

    def put(self):
        return
    

def init_api(app):

    @app.route("/upload-image", methods=["POST"])
    def upload_image():
        if request.method == "POST":
            if "file" not in request.files:
                return "No File Submitted\n"
            #id = request.form["id"]
            file = request.files["file"]
            if file.filename == "":
                return "Filename Empty\n"
            file.save(app.root_path + os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return "Success\n"
        return "Method not supported\n"


    api = Api(app)
    api.add_resource(ImageResource, "/api/images/<string:image_id>")
    api.add_resource(CharacterResource, "/api/characters")
