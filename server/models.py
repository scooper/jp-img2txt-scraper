from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)

Base = declarative_base(metadata=metadata)

association_table = db.Table(
    "img_char_association",
    db.Column("char_id", db.ForeignKey("characters.id"), primary_key=True),
    db.Column("img_id", db.ForeignKey("images.id"), primary_key=True)
)

class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.String, primary_key=True)
    filepath = db.Column(db.String)
    ocr_result = db.Column(db.String)
    ocr_result_machine_translated = db.Column(db.String)
    characters = db.relationship("Character", secondary=association_table, back_populates="images")
    time_created = db.Column(db.DateTime(timezone=True), default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

class Character(db.Model):
    __tablename__ = "characters"
    id = db.Column(db.String, primary_key=True)
    character = db.Column(db.String)
    jisho_link = db.Column(db.String)
    images = db.relationship("Image", secondary=association_table, back_populates="characters")
    time_created = db.Column(db.DateTime(timezone=True), default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())