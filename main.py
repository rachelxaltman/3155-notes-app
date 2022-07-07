
import os                 
import random
from flask import Flask, request, render_template, redirect, url_for, session
from sqlalchemy.sql.expression import func, select
from database import db
from note import Note
from user import User
from comment import Comment
from hashing import Encryption
from brmodels import BRboard, BRplayer, BRnote, BRcomment, BRtopic

from ZAASK_forms import CommentForm, PlayerForm, TopicForm, BRNoteForm, BRCommForm

app = Flask(__name__)

#Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY'] = 'A31503G5DD33S'

#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)
# Setup models
with app.app_context():
    db.create_all()   # run under the app context

@app.route('/')
@app.route('/index')
def index():
    if session.get('user'):
        return render_template('index.html', user=session['user'])
    else:
        return redirect(url_for('sign_in'))


# TODO: This page should become a board (display multiple notes) and we need a board selection screen before it
@app.route('/notes')
def display_notes():
    if session.get('user'):
        #retrieve all notes
        _notes = db.session.query(Note).filter_by(user_id=session['user']).all()

        return render_template('notes.html', user=session['user'], notes=_notes)
    else:
        return redirect(url_for('sign_in'))


@app.route('/notes/<note_id>')
def get_note(note_id):
    if session.get('user'):

        #retrieve note
        my_note = db.session.query(Note).filter_by(id=note_id).one()

        form = CommentForm()

        return render_template('viewnote.html', note = my_note, user=session['user'], form=form)
    else:
        return render_template('signIn.html')

#New Notes
@app.route('/notes/new', methods=['GET', 'POST'])
def new_note():
    if session.get('user'):
        if request.method == 'POST':
            #get user
            user_id = session['user']
            #get form data
            title = request.form['title']
            text = request.form['noteText']
            isTaskBox = request.form.getlist('isTask') # Is the note a task?

            isTask = False
            if len(isTaskBox) > 0:
                isTask = True

            #create date stamp
            from datetime import date
            today = date.today()
            today = today.strftime("%m-%d-%Y")

            #create color
            color = "TEMP"

            new_record = Note(title, text, today, color, user_id, isTask)
            db.session.add(new_record)
            db.session.commit()

            return redirect(url_for('display_notes'))
        else:
            #GET request
            return render_template('newnote.html', user=session['user'])
    else:
        return render_template('signIn.html')

@app.route('/signIn', methods=['GET', 'POST'])
def sign_in():

    
    if request.method == 'POST':

        encryption = Encryption()

        # Get username and password
        user_username = request.form['username']
        user_encrypted_password = encryption.encrypt(request.form['password'])
        the_user = db.session.query(User).filter_by(name=user_username).one()

        if encryption.check_encrypted_password(user_encrypted_password, the_user.password):
            print("\n\nPassword and username correct\n")
            session['user'] = the_user.name
            session['user_id'] = the_user.id
        else:
            print("\nIncorrect password\n")

        return redirect(url_for('index'))
    return render_template('signIn.html')

@app.route('/createAccount', methods=['GET', 'POST'])
def new_account():
    new_user = {'name':'','email':''}

    # Get form data from creating account
    if request.method == 'POST':

        encryption = Encryption()

        # Check if passwords match
        if request.form['password'] == request.form['repeatPassword']:
            encrypted_password = encryption.encrypt(request.form['password'])
            new_user = User(request.form['username'], request.form['email'], encrypted_password)


            db.session.add(new_user)
            db.session.commit()

            the_user = db.session.query(User).filter_by(email=request.form['email']).one()

            session['user'] = the_user.name
            session['user_id'] = the_user.id
            
            # Return user to notes page
            return redirect(url_for("index"))

    return render_template('createAccount.html')

@app.route('/logout')
def logout():
    # check if a user is saved in session
    if session.get('user'):
        session.clear()

    return redirect(url_for('sign_in'))

# FIX ISSUE BELOW

@app.route('/notes/edit/<note_id>', methods=['GET', 'POST'])
def update_note(note_id):
     if request.method == 'POST':
       title = request.form['title']
       text = request.form['noteText']
       note = db.session.query(Note).filter_by(id=note_id).one()
       note.title = title
       note.text = text
       pinned = request.form.getlist('pin') # Pin note?
       if len(pinned) > 0:
           note.pinned = True
       else:
           note.pinned = False

       taskFinished = request.form.getlist('taskFinished') # Pin note?
       if len(taskFinished) > 0:
           note.taskFinished = True
       else:
           note.taskFinished = False

       print("\n\n", pinned)
       db.session.add(note)
       db.session.commit()

       return redirect(url_for('display_notes'))
     else:
        
      a_user = session['user']
      my_note = db.session.query(Note).filter_by(id=note_id).one()
      return render_template("newnote.html", note=my_note, user=a_user)

@app.route('/notes/delete/<note_id>', methods=['POST'])
def delete_note(note_id):
    my_note = db.session.query(Note).filter_by(id=note_id).one()
    db.session.delete(my_note)
    db.session.commit()

    return redirect((url_for('display_notes')))

@app.route('/notes/<note_id>/comment', methods=['POST'])
def add_comment(note_id):
    if session.get('user'):
        comment_form = CommentForm()
        # validate_on_submit only validates using POST
        if comment_form.validate_on_submit():
            # get comment data
            comment_text = request.form['comment']
            new_record = Comment(comment_text, int(note_id), session['user_id'])
            db.session.add(new_record)
            db.session.commit()

        return redirect(url_for('get_note', note_id=note_id))

    else:
        return redirect(url_for('sign_in'))

@app.route('/notes/<comment_id>/UpdateComment', methods=['GET', 'POST'])
def update_comment(comment_id):

    if request.method == 'POST':

        text = request.form['commText']
        comm = db.session.query(Comment).filter_by(id=comment_id).one()
        comm.text = text
            
        db.session.add(comm)
        db.session.commit()

        return redirect(url_for('display_notes'))
    else:
      a_user = session['user']
      comm = db.session.query(Comment).filter_by(id=comment_id).one()
      return render_template("editComment.html", comment=comm, user=a_user)

@app.route('/notes/<comment_id>/delete', methods=['POST'])
def delete_comment(comment_id):
    my_cm = db.session.query(Comment).filter_by(id=comment_id).one()
    db.session.delete(my_cm)
    db.session.commit()

    return redirect((url_for('display_notes')))

@app.route('/my_account')
def my_account():
    if session.get('user'):
        the_user = db.session.query(User).filter_by(name=session['user']).one()
        _notes = db.session.query(Note).filter_by(user_id=session['user']).all()
        return render_template('myaccount.html', user=session['user'], email=the_user.email, numNotes=len(_notes))
    else:
        return redirect(url_for('sign_in'))


@app.route('/note/<note_id>/Check')
def check_task(note_id):
    if session.get('user'):
        my_task = db.session.query(Note).filter_by(id=note_id).one()
        if my_task.isTask:
            my_task.taskFinished = not my_task.taskFinished

        db.session.add(my_task)
        db.session.commit()

        return redirect(url_for('display_notes'))
    else:
        return redirect(url_for('sign_in'))



#<-----------------------------------------------------------------------BR ROUTES-------------------------------------------------------------->


#BR Matches page
@app.route('/battle_mode')
def match_overview():
    if session.get('user'):

        _matches = db.session.query(BRboard).filter_by(user_id=session['user']).all()

        return render_template('br-home.html', user=session['user'], matches=_matches)
    else:
        return redirect(url_for('sign_in'))

#Delete Matches
@app.route('/matches/<match_id>/delete', methods=['POST'])
def delete_match(match_id):

    my_mt = db.session.query(BRboard).filter_by(id=match_id).one()
    db.session.delete(my_mt)
    db.session.commit()

    return redirect(url_for('match_overview'))

#Create Match
@app.route('/battle_mode/new', methods=['GET', 'POST'])
def new_match():
    if session.get('user'):

        if request.method == 'POST':

             #get user
            user_id = session['user']
            #get form data
            lobby = request.form['title']
            
            new_match = BRboard(user_id, lobby)
            db.session.add(new_match)
            db.session.commit()


            return redirect(url_for('new_players', board_id=new_match.id))

        else:
            return render_template('br-new-match.html', user=session['user'])
    else:
        return redirect(url_for('sign_in'))
#create players
@app.route('/battle_mode/<board_id>/players', methods=['GET', 'POST'])
def new_players(board_id):
    if session.get('user'):
        _match = db.session.query(BRboard).filter_by(id=board_id).one()
        if _match.round == 0:

            
            player_form = PlayerForm()

            if request.method == 'POST':

                # validate_on_submit only validates using POST
                if player_form.validate_on_submit():
                    #Add player
                    pname = request.form['player']
                    new_play = BRplayer(pname, board_id)
                    db.session.add(new_play)
                    db.session.commit()

                    #also add new note for each player
                    new_note = BRnote(board_id, new_play.id)
                    db.session.add(new_note)
                    db.session.commit()


                return redirect(url_for('new_players', board_id = board_id))
            else:
                return render_template('br-new-players.html', user=session['user'], match=_match, form=player_form)
        else:
            return redirect(url_for('match_overview'))
    else:
        return redirect(url_for('sign_in'))
#create topics
@app.route('/battle_mode/<board_id>/topics', methods=['GET', 'POST'])
def new_topics(board_id):
    if session.get('user'):
        _match = db.session.query(BRboard).filter_by(id=board_id).one()

        if _match.round <= 0:
            

            if request.method == 'POST':
                text1 = request.form['text1']
                text2 = request.form['text2']
                text3 = request.form['text3']

                if text1 != "":
                    _match.topic1 = text1
                else:
                    _sl = db.session.query(BRtopic).order_by(func.random()).first()
                    _match.topic1 = _sl.topic

                if text2 != "":
                    _match.topic2 = text2
                else:
                    _sl = db.session.query(BRtopic).order_by(func.random()).first()
                    _match.topic2 = _sl.topic

                if text3 != "":
                    _match.topic3 = text3
                else:
                    _sl = db.session.query(BRtopic).order_by(func.random()).first()
                    _match.topic3 = _sl.topic
                
                #set starting round
                _match.round = 0

                db.session.add(_match)
                db.session.commit()

                return redirect(url_for('view_match', match_id=board_id))

            else:
                return render_template('br-new-Topics.html', user=session['user'], match =_match)
        else:
            return redirect(url_for('match_overview'))
    else:
        return redirect(url_for('sign_in'))


#Match Page
@app.route('/battle_mode/<match_id>', methods=['GET', 'POST'])
def view_match(match_id):
    if session.get('user'):
        _match = db.session.query(BRboard).filter_by(id=match_id).one()
        _notes = db.session.query(BRnote).filter_by(brboard_id=match_id).all()


        #Randomize notes
        _procnotes = _notes
        #_procnotes.pop('_sa_instance_state', None)
        random.shuffle(_procnotes)

        #Sort order
        sortable = []
        for note in _procnotes:
            notevote = (note, note.votes)
            sortable.append(notevote)
        sortable.sort(key = lambda x: x[1], reverse=True)
        #replace
        _procnotes = []
        for note in sortable:
            _procnotes.append(note[0])
        

        if request.method == 'POST': #ROUND PROCESSING
            #next round timer
            if _match.round < 10:
                _match.round = _match.round + 1   #NOTE!!! NEED GAME TO START ON ROUND 1, NOT 0

                db.session.add(_match)
                db.session.commit()
            
            return redirect(url_for('view_match', match_id = _match.id))
        else:
            return render_template('br-match.html', user=session['user'], match=_match, procnotes=_procnotes)
    else:
        return redirect(url_for('sign_in'))
    #Display/calculate the topic
    #Display Ranking
        #END ROUND button
    #Display Stages (3)
    #Display winner,
    #Then version to display old/won games.

@app.route('/battle_mode/<match_id>/add', methods=['GET', 'POST'])
def match_add_notes(match_id):
    if session.get('user'):
        _match = db.session.query(BRboard).filter_by(id=match_id).one()
        if _match.round <= 9:
            
            _players = db.session.query(BRplayer).filter_by(brboard_id=match_id).all()
            _notes = db.session.query(BRnote).filter_by(brboard_id=match_id).all()

            brnoteform = BRNoteForm()

            return render_template('br-edit-notes.html', user=session['user'], match=_match, procplayers = _players, form=brnoteform, notes=_notes)
        
        else:
            return redirect(url_for('view_match', match_id=match_id))
    else:
        return redirect(url_for('sign_in'))
@app.route('/battle_mode/<match_id>/add/<user_id>', methods=['GET', 'POST'])
def match_add_notes_spec(match_id, user_id):
    if session.get('user'):
        _match = db.session.query(BRboard).filter_by(id=match_id).one()

        if _match.round <= 9:

            
            _players = db.session.query(BRplayer).filter_by(brboard_id=match_id).all()
            _notes = db.session.query(BRnote).filter_by(brboard_id=match_id).all()

            _spec = db.session.query(BRplayer).filter_by(id=user_id).one()
            

            brnoteform = BRNoteForm()

            if request.method == 'POST':
                
                _brnote = db.session.query(BRnote).filter_by(player_id=_spec.id, brboard_id = _match.id).one()

                #HTML doesn't seem to like the nested values

                addtext=request.form['note']
                if _match.round == 0:
                    _brnote.title = addtext
                elif _match.round < 3:
                    _brnote.text1 = addtext
                elif _match.round < 6:
                    _brnote.text2 = addtext
                elif _match.round < 9:
                    _brnote.text3 = addtext

                
                db.session.add(_brnote)
                db.session.commit()
                
                
                return redirect(url_for('match_add_notes', match_id=match_id))
            else:

                return render_template('br-edit-notes.html', user=session['user'], match=_match, procplayers = _players, notes=_notes, play = _spec, form=brnoteform)
        
        else:
            return redirect(url_for('view_match', match_id=match_id))
    else:
        return redirect(url_for('sign_in'))
        
#Round Start page:
    #Display all the notes/players, and let people add them.
    #display topic.



#<BRnote single pages>:

#voting page:
@app.route('/battle_mode/<match_id>/vote', methods=['GET', 'POST'])
def brnote_vote(match_id):
    if session.get('user'):
        _match = db.session.query(BRboard).filter_by(id=match_id).one()
        if _match.round <= 9:
            _notes = db.session.query(BRnote).filter_by(brboard_id=match_id)
            _notes = _notes.filter_by(fortnite=True).all()

            if request.method == 'POST':

                votes = {}
                for notes in _notes:
                    votes.update({str(notes.id): notes.votes})

                for play in _match.players:
                    reqst1 = play.name + 'v1'
                    reqst2 = play.name + 'v2'
                    reqst3 = play.name + 'v3'
                    
                    vote1 = request.form[reqst1]
                    vote2 = request.form[reqst2]
                    vote3 = request.form[reqst3]
                    votes[vote1] +=1
                    votes[vote2] +=1
                    votes[vote3] +=1


                for key in votes:
                    _candid = db.session.query(BRnote).filter_by(id=key).one()
                    _candid.votes = votes[key]
                    db.session.add(_candid)
                    db.session.commit()



                return redirect(url_for('brnote_vote_results', match_id=match_id))
            else:
                return render_template('br-voting.html', user=session['user'], match=_match, procnotes=_notes)
        else:
            return redirect(url_for('view_match', match_id=match_id))
    else:
        return redirect(url_for('sign_in'))
#results
@app.route('/battle_mode/<match_id>/vote/results')
def brnote_vote_results(match_id):
    if session.get('user'):
        _match = db.session.query(BRboard).filter_by(id=match_id).one()
        if _match.round <= 9:

            _notes = db.session.query(BRnote).filter_by(brboard_id=match_id).all()
            _players = db.session.query(BRplayer).filter_by(brboard_id=match_id).all()

            #Randomize notes
            _procnotes = _notes
            #_procnotes.pop('_sa_instance_state', None)
            random.shuffle(_procnotes)
            #Sort order
            sortable = []
            unsort =[]
            for note in _procnotes:
                if note.fortnite:
                    notevote = (note, note.votes)
                    sortable.append(notevote)
                else:
                    unsort.append(note)
            sortable.sort(key = lambda x: x[1], reverse=True)
        
            #calc and replace
            fortnight = int(len(sortable) * .75) - 1
            if fortnight < 1:
                fortnight = 1

            for num in range(0, len(sortable)):

                if num <= fortnight:
                    sortable[num][0].fortnite = True

                    db.session.add(sortable[num][0])
                    db.session.commit()
                    
                else:

                    sortable[num][0].fortnite = False
                    db.session.add(sortable[num][0])
                    db.session.commit()

                    _play = db.session.query(BRplayer).filter_by(id = sortable[num][0].player_id).one()
                    _play.fortnite = False
                    db.session.add(_play)
                    db.session.commit()

            _procnotes = []
            for note in sortable:
                _procnotes.append(note[0])
            for note in unsort:
                _procnotes.append(note)

            for num in range(0, len(_procnotes)):
                _procnotes[num].ranking = str(num + 1)
                db.session.add(_procnotes[num])
                db.session.commit()
            
            if _match.round >= 9:
                _match.winner = _procnotes[0].title
                db.session.add(_match)
                db.session.commit()
                

            return render_template('br-voting-results.html', user=session['user'], match=_match, procnotes=_notes, players=_players)
        else:
            return redirect(url_for('view_match', match_id=match_id))
    else:
        return redirect(url_for('sign_in'))
    

#comment page:
@app.route('/battle_mode/<brnote_id>/<match_id>/comment', methods=['GET', 'POST'])
def brnote_comment(match_id, brnote_id):
    if session.get('user'):
        _match = db.session.query(BRboard).filter_by(id=match_id).one()  
        _note = db.session.query(BRnote).filter_by(id=brnote_id).one()
        _proccomm = db.session.query(BRcomment).filter_by(brnote_id=brnote_id).all()
        print(_proccomm)
        comm_form = BRCommForm()

        # Comments, one for each person, and submit. (Play over discord.)
        # auto load and edit the comments

        if request.method == 'POST':
            
            # get comment data
            comment_text = request.form['comm']
            new_record = BRcomment(comment_text, brnote_id)
            db.session.add(new_record)
            db.session.commit()


            return redirect(url_for('brnote_comment', match_id=match_id, brnote_id=brnote_id))
    
        else:        
            return render_template('br-comments.html', user=session['user'], match=_match, note=_note, proccomments=_proccomm, form=comm_form)

    else:
        return redirect(url_for('sign_in'))
@app.route('/battle_mode/<brnote_id>/<match_id>/comment/delete/<brcomm_id>', methods=['POST'])
def brnote_comment_delete(match_id, brnote_id, brcomm_id):
    if session.get('user'):
        _match = db.session.query(BRboard).filter_by(id=match_id).one()

        if _match.round <= 9:
            my_cm = db.session.query(BRcomment).filter_by(id=brcomm_id).one()
            db.session.delete(my_cm)
            db.session.commit()
            return redirect(url_for('brnote_comment', match_id=match_id, brnote_id=brnote_id))
        else:
            return redirect(url_for('brnote_comment', match_id=match_id, brnote_id=brnote_id))

    else:
        return redirect(url_for('sign_in'))
        
#OR, replace with first 10 comments by ref/favorites? That way it's more collab, and more fun to read along!
#"Shout it out! battle royale." 
#hard part is limiting it, html and list count? maybe the value is built into list though. 

#Have it so you cycle quick from comments, then to next note. high stakes time stuff!



#add topic suggestions
@app.route('/battle_mode/suggestions', methods=['GET', 'POST'])
def suggest_topics():
    if session.get('user'):

        topic_form = TopicForm()
        topics = db.session.query(BRtopic)

        if request.method == 'POST':

            # validate_on_submit only validates using POST
            if topic_form.validate_on_submit():
                #Add player
                _topic = request.form['topic']
                new_topic = BRtopic(_topic)
                db.session.add(new_topic)
                db.session.commit()

            return redirect(url_for('suggest_topics'))
        else:
            return render_template('br-suggest-topics.html', user=session['user'],topics = topics, form=topic_form)
    else:
        return redirect(url_for('sign_in'))
#delete topic
@app.route('/battle_mode/sgdelete/<topic_id>', methods=['POST'])
def delete_topic(topic_id):
    my_cm = db.session.query(BRtopic).filter_by(id=topic_id).one()
    db.session.delete(my_cm)
    db.session.commit()

    return redirect((url_for('suggest_topics')))




app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)
