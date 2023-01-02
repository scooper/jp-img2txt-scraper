from flask import Flask
from flask_restful import Resource, Api
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
        ()

    api = Api(app)
    api.add_resource(ImageResource, "/image/<string:image_id>")
