from flask import Flask, request, redirect
from flask_restful import Resource, Api, reqparse
import os
import uuid
from server.models import Image, Character, db
from urllib.parse import quote_plus

parser = reqparse.RequestParser()
parser.add_argument("ocr_txt", type=str)
parser.add_argument("character", type=str)
parser.add_argument("character_id", type=str)
parser.add_argument("image_id", type=str)

class CharactersRes(Resource):
    def get(self):
        # all characters
        query_result = Character.query.all()
        # map
        characters = [{"id": c.id, "character": c.character, "jisho": c.jisho_link, "images": [{"image_id": i.id} for i in c.images]} for c in query_result]
        return {"characters": characters}, 200

class CharacterRes(Resource):
    def get(self):
        character_id = request.args['character_id']

        if character_id is None or character_id == "":
            return "Not Found", 404

        query_result = Character.query.get(character_id)

        return {"id": query_result.id, "character": query_result.character, "images": [{"image_id": i.id} for i in query_result.images]}

    def put(self):
        args = parser.parse_args()

        image_id = args['image_id']
        image = Image.query.get(image_id)

        if image is None:
            return "Not Found", 404

        character = args['character']
        character_id = str(uuid.uuid4())

        character_db = Character.query.filter_by(character = character).first()
        if character_db is None:
            character_db = Character()
            character_db.id = character_id
            character_db.character = character
            character_db.jisho_link = 'https://jisho.org/search/' + quote_plus(character) + '%20%23kanji'
        
        character_db.images.append(image)

        db.session.add(character_db)
        db.session.commit()

        # receive character and image reference, 
        return "Success", 201

class ImagesRes(Resource):
    def get(self):
        # all images
        query_result = Image.query.all()
        # map
        images = [{"id": i.id, "text": i.ocr_result, "machine_text": i.ocr_result_machine_translated, "characters": [{"character_id": c.id} for c in i.characters]} for i in query_result]
        return {"images": images}, 200

class ImageRes(Resource):
    def get(self):
        image_id = request.args['image_id']

        if image_id is None or image_id == "":
            return "Not Found", 404

        query_result = Image.query.get(image_id)
        payload = {"id": query_result.id, "text": query_result.ocr_result, "machine_text": query_result.ocr_result_machine_translated, "characters": [{"character_id": c.id, "character": c.character} for c in query_result.characters]}
        return {"image": payload}, 200
        

    def put(self):
        args = parser.parse_args()
        image_id = args['image_id']
        ocr_txt = args['ocr_txt']

        image_db = Image()
        image_db.id = image_id
        image_db.ocr_result = ocr_txt
        image_db.ocr_result_machine_translated = 'https://www.deepl.com/translator#ja/en/' + quote_plus(ocr_txt)
        image_db.filepath = "" # reduntant
        image_db.characters = []

        db.session.add(image_db)
        db.session.commit()

        return "Success", 201
    

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
    api.add_resource(ImageRes, "/api/image")
    api.add_resource(ImagesRes, "/api/images")
    api.add_resource(CharacterRes, "/api/character")
    api.add_resource(CharactersRes, "/api/characters")
