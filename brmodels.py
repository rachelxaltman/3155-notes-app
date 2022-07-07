from database import db
import datetime

class BRtopic(db.Model):
    id = db.Column("id", db.Integer, primary_key = True)
    topic = db.Column("topic", db.String(50))

    def __init__(self, topic):
        self.topic = topic

class BRboard(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)

    #Game State Info 
    round = db.Column("round", db.Integer)

    winner = db.String("winner", db.Integer)

    lobby = db.Column("lobby", db.String(50))
    topic1 = db.Column("topic1", db.String(50))
    topic2 = db.Column("topic2", db.String(50))
    topic3 = db.Column("topic3", db.String(50))

    date = db.Column("date", db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    players = db.relationship("BRplayer", backref = "BRboard", lazy=True, cascade="all,delete")
    brnotes = db.relationship("BRnote", backref = "BRboard", lazy=True, cascade="all,delete")

    def __init__(self, user_id, lobby):
        self.user_id = user_id
        self.lobby = lobby
        self.round = 0
        self.date = datetime.date.today()


class BRplayer(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    fortnite = db.Column("fortnite", db.Boolean, default=True)

    brboard_id = db.Column(db.Integer, db.ForeignKey("b_rboard.id"), nullable=False)

    brnote = db.relationship("BRnote", backref=db.backref("BRnote", uselist=False), lazy=True)

    def __init__(self, name, brboard_id):
        self.name = name
        self.votes = 3
        self.brboard_id = brboard_id

class BRnote(db.Model):
    id = id = db.Column("id", db.Integer, primary_key=True)
    votes = db.Column("votes", db.Integer)
    ranking = db.Column("ranking", db.Integer)
    fortnite = db.Column("fortnite", db.Boolean, default=True)

    brboard_id = db.Column(db.Integer, db.ForeignKey("b_rboard.id"), nullable=False)

    player_id = db.Column(db.Integer, db.ForeignKey('b_rplayer.id'))
    player = db.relationship("BRplayer", backref = "BRplayer", lazy = True)

    title = db.Column("title", db.String(100))
    text1 = db.Column("text1", db.String(100))
    text2 = db.Column("text2", db.String(100))
    text3 = db.Column("text3", db.String(100))




    brcomments = db.relationship("BRcomment", backref = "BRnote", lazy=True, cascade="all,delete")

    def __init__(self, brboard_id, user_id):
        self.brboard_id = brboard_id
        self.player_id = user_id
        self.title = ""
        self.text1 = ""
        self.text2 = ""
        self.text3 = ""
        self.ranking = 0
        self.votes = 0
        

class BRcomment(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    text = db.Column("text1", db.String(100))
    brnote_id = db.Column(db.Integer, db.ForeignKey("b_rnote.id"), nullable=False)

    def __init__(self, text, brnote_id):
        self.text = text
        self.brnote_id = brnote_id


"""
DD:
    1. Starting matches
    2. Rounds
        a. Adding Notes stage
        b. Reading Stage
        c. Commenting/debating stage --> More integral, to give reason for slow voting. 
        d. Voting Stage.
        e. Completing Stage/submit
    3. Repeat Rounds, add new topic x3.
    4. Winner/results page --> Play again?

    5. View old matches, and delete.

    0
    123 phases
    456
    789
    10
    11

*:
- Ties all count for a single position, so any under that position gets tossed. 
- Ordering algo is gonna have to be kinda boss.

Rounds :bottom 25%, bottom 50%, top 3
Minimums: Round 2: 5, round 3: 3 obvs.
Ranking is always ordered, so that those who dropped in the bottom keep, and it just makes a smaller and smaller array or something.
Database will have to calculate and order the array accordingly. 
Get all as list, then order it, then apply values via for loop.


Tutorial details:
Add more details/instructions to make the game more playable, like subtitle instructions on jackbox games. Ex: "Phase: Reading and Commenting!" "Read through each of the notes, shout out suggest
-If time allows as well as sql, maybe could make versions of the pages with help=True for help.
Table under BattleRoyale.html with text, story, and etc. be "professional", "businessy" this time, lol.


"""


"""
Hot Takes Battle Royale, Note to self BR, 
Notes App Battle Royale.

Structure: 
- Players all get to post 3 or so hot takes, and then vote on them to decide which is the hottest.
- After a set time period, or everyone has voted, the tallies are displayed.
- most votes, second most votes, third most votes wins.
    BR?:
    - 3 round partitions. Top 50%, then top 25%, then winners. Minimum of 3 players per round. 


Local:
- Local version should be easily playable, like a board game. Might actually jsut do that.
- Database of topics then to have hot takes on? or just note to self.
- Add comments is most difficult part, but I think everyone should also just get one comment per note.

Even better, cascading topics, and then everyone gets to add to their note, but not take away.

A, B, C topic discussion.
"Squirrles that eat seals"
"politics that suck at family reunions"
or just 3 nouns, make a convincing note.

vote table, over the general like or unlike system. but can buttons, if want. Just *voting page*, and edit with dropboxes, or something.


Store winners at the end.
Everyone gets a comment each round.
Store versions?


---------------
Want database to store each match, with each note, and display ranking, feel free to delete.
new boards, old boards.


"""
