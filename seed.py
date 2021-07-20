"""Seed file to make sample data for notes db."""

from models import User, Note, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Note.query.delete()

# Add users
users = [User(username="bobthebob", password="Björk", email="adw@adf.com", first_name="Bob", last_name ="Bobert"),
         User(username="bobthebob2", password="Björk", email="adc@adf.com", first_name = "Bob2", last_name = "Bobert2"),
         User(username="bobthebob3", password="Björk", email="ade@adf.com", first_name = "Bob3", last_name = "Bobert3"),
        ]

# Add notes
notes = [Note(title="Beethoven Works", content="Beethoven only", owner="bobthebob"),
        Note(title="Beethoven Works2", content="Beethoven only2", owner="bobthebob"),
        Note(title="Beethoven Works3", content="Beethoven only3", owner="bobthebob")
        ]

# Add new objects to session, so they'll persist
db.session.add_all(users)
db.session.add_all(notes)

# Commit--otherwise, this never gets saved!
db.session.commit()