from database import db
import datetime

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column("text", db.String(100))
    date = db.Column("date", db.String(50))
    note_id = db.Column(db.Integer, db.ForeignKey("note.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, text, note_id, user_id):
        self.text = text
        self.date = datetime.date.today()
        self.note_id = note_id
        self.user_id = user_id


    # This will be used later to create the note in the database, it's useless for now
    @staticmethod
    def create_comment(text, note_id, user_id):
        return Comment(text, note_id, user_id)