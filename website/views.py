"""
Store routes for our website. Home page, anything not related to authentication information.
"""

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

"""
Defining route for our home page
"""


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if not note or len(note) < 1:
            flash('Note is too short!', category='error')
        else:  # create new note for this user, add to db, let them know created.
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    # else simple get request just show them the html template, pass in the current user so we can grab their note
    # information and display dynamically using the home.html template which loops through a user's notes.
    return render_template("home.html", user=current_user)


"""
Used as our endpoint for deleteNote function in index.js defined for onClick event handler for the button that user
clicks "x" to delete a note. 
"""


@views.route('/delete-note', methods=['POST'])
def delete_note():
    # put json from request into dict.
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    # if we found the note, and as a check the id mapped to it is indeed the same as the currently logged in user,
    # then remove it out of our db.
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
