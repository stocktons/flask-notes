"""Notes app that allows users to write, save, and edit notes."""

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Note
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///notes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route("/")
def homepage():
    """Redirect to /register."""

    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user: produce form & handle form submission."""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, pwd, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        session["username"] = user.username

        # on successful login, redirect to secret page
        return redirect(f"/users/{username}")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(username, pwd)

        if user:
            session["username"] = user.username  # keep logged in
            return redirect(f"/users/{username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)


@app.route("/users/<username>")
def authorize(username):
    """Example hidden page for logged-in users only."""

    user = User.query.get_or_404(username)
    notes = user.notes

    if "username" not in session or username != session["username"]: # REALLY IMPORTANT
        flash("You must be logged in to view!")
        return redirect("/")

        # alternatively, can return HTTP Unauthorized status:
        #
        # from werkzeug.exceptions import Unauthorized
        # raise Unauthorized()

    else:

        return render_template("userinfo.html", user=user, notes=notes)

@app.route("/logout", methods = ["POST"])
def logout():
    """Logs user out and redirects to homepage."""

    # Remove "username" if present, but no errors if it wasn't
    session.pop("username", None)

    return redirect("/")

# @app.route("/users/<username>/notes/add", methods=["POST", "GET"])
# def add_user(username):
#     """Displays a form to add notes."""

#     user = User.query.get_or_404(username)
   


#     # db.session.add(note)
#     # db.session.commit()

#     return redirect(f"/users/{user.username}")

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Deletes user and all their posts from database."""

    if "username" not in session or username != session["username"]: # REALLY IMPORTANT
        flash("You can't delete someone else, you slimeball! (Or if you are really you, log in.)")
        return redirect("/")

        # alternatively, can return HTTP Unauthorized status:
        #
        # from werkzeug.exceptions import Unauthorized
        # raise Unauthorized()

    user = User.query.get_or_404(username)

    db.session.delete(user)
    db.session.commit()
    flash(f"User {username} deleted.")

    return redirect("/")

##################################################################
# Notes Routes
@app.route("/notes/<note_id>/delete", methods=["POST"])
def delete_note(note_id):
    """Deletes note from database."""

    note = Note.query.get_or_404(note_id)
    user = note.user
    
    db.session.delete(note)
    db.session.commit()

    return redirect(f"/users/{user.username}")