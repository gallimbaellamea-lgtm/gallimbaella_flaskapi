from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    course = db.Column(db.String(10), nullable=False)
    section = db.Column(db.String(10), nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    hobby = db.Column(db.String(200))

    @property
    def age(self):
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
