from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Student(UserMixin, db.Model):
    __tablename__ = 'STUDENT'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(80), index=True,  unique=True, nullable=False)
    fname = db.Column(db.String(80), index=False,  nullable=False)
    lname = db.Column(db.String(80), index=False,  nullable=False)
    classcode=db.Column(db.String(20), index=False,  nullable=False)
    password = db.Column(db.String(200), index=False,  unique=False, nullable=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)

