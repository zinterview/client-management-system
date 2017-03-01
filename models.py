"""Models."""
import hashlib
import enum

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(99), unique=True)
    password = db.Column(db.String(32))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.set_password(password)

    def __repr__(self):
        return '<User %s>' % self.email

    def set_password(self, password):
        self.password = hashlib.md5(password.encode()).hexdigest()

    def compare_password(self, password):
        hashed = hashlib.md5(password.encode()).hexdigest()
        if hashed == self.password:
            return True
        return False


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Client %s>' % self.email


class AccountType(enum.Enum):
    SAVINGS = "savings"
    CURRENT = "current"


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acc_no = db.Column(db.Integer, unique=True)
    acc_name = db.Column(db.String(40))
    acc_type = db.Column(db.Enum(AccountType))
    client1 = db.Column(db.Integer, db.ForeignKey(Client.id))
    client2 = db.Column(db.Integer, db.ForeignKey(Client.id), nullable=True)

    def __init__(self, acc_no, acc_name, acc_type, client1, client2=None):
        self.acc_no = acc_no
        self.acc_name = acc_name
        self.acc_type = acc_type
        self.client1 = client1
        self.client2 = client2

    def __repr__(self):
        return '<Account %d>' % self.acc_no
