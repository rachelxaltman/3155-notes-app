from database import db
from note import Note
from comment import Comment
from brmodels import BRboard

class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column("password", db.String(100))
    notes = db.relationship("Note", backref="user", lazy=True)
    comments = db.relationship("Comment", backref="user", lazy=True)
    matches = db.relationship("BRboard", backref="user", lazy=True)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password