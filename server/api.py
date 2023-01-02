from flask import Flask, request, redirect
from flask_restful import Resource, Api
import os
from server.models import Image
from server.models import Character

class ImageResource(Resource):
    def get(self, image_id):
        ()

    def put(self, image_id):
        ()
    

def init_api(app):

    @app.route("/upload-image", methods=["POST"])
    def upload_image():
        if request.method == "POST":
            if "file" not in request.files:
                return "No File Submitted\n"
            id = request.form["id"]
            file = request.files["file"]
            if file.filename == "":
                return "Filename Empty\n"
            file.save(app.root_path + os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return "Success\n"
        return "Method not supported\n"


    api = Api(app)
    api.add_resource(ImageResource, "/image/<string:image_id>")
