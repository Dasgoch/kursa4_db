import logging
from app import login_manager
from flask_login import UserMixin
from main import *

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.set_username()

    def set_username(self):
        cur.execute("SELECT username FROM username")
        username = cur.fetchone()
        self.username = username[0]

