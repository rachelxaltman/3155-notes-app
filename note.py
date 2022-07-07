from database import db
from comment import Comment

class Note(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(200))
    text = db.Column("text", db.String(100))
    date = db.Column("date", db.String(50))
    color = db.Column("color", db.String(6))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    comments = db.relationship("Comment", backref="note", cascade="all, delete-orphan", lazy=True)
    pinned = db.Column("pinned", db.Boolean)
    isTask = db.Column("isTask", db.Boolean)
    taskFinished = db.Column("taskFinished", db.Boolean)

    def __init__(self, title, text, date, color, user_id, isTask):
        self.title = title
        self.text = text
        self.date = date
        self.color = color
        self.user_id = user_id
        self.isTask = isTask


    # This will be used later to create the note in the database, it's useless for now
    @staticmethod
    def create_note(title, text, date, color, user_id, isTask):
        return Note(title, text, date, color, user_id, isTask)