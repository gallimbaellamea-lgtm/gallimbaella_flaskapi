student_management/
│
├── app.py
├── models.py
├── forms.py
├── requirements.txt
├── templates/
│   ├── index.html
│   └── dashboard.html
└── static/
    └── style.css

---

# Complete GitHub-ready ZIP Project
# You can compress the folder 'student_management/' and upload directly to GitHub.

---

# requirements.txt
Flask==2.3.4
Flask-SQLAlchemy==3.0.5
Flask-WTF==1.1.1
email-validator==2.1.3
gunicorn==21.2.0

---

# models.py
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

---

# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

class StudentForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    birthday = DateField('Birthday', validators=[DataRequired()], format='%Y-%m-%d')
    course = SelectField('Course', choices=[('BSIT','BSIT'), ('BSOA','BSOA'), ('BSED','BSED'), ('BSAG','BSAG')], validators=[DataRequired()])
    section = StringField('Section', validators=[DataRequired()])
    sex = SelectField('Sex', choices=[('Male','Male'), ('Female','Female')], validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    hobby = TextAreaField('Hobby')
    submit = SubmitField('Submit')

---

# templates/index.html
<!DOCTYPE html>
<html>
<head>
    <title>Student Form - San Enrique ISUFST</title>
</head>
<body>
    <h1>{% if edit %}Edit{% else %}Add{% endif %} Student</h1>
    <form method="POST">
        {{ form.hidden_tag() }}
        {{ form.full_name.label }} {{ form.full_name() }}<br>
        {{ form.birthday.label }} {{ form.birthday() }}<br>
        {{ form.course.label }} {{ form.course() }}<br>
        {{ form.section.label }} {{ form.section() }}<br>
        {{ form.sex.label }} {{ form.sex() }}<br>
        {{ form.email.label }} {{ form.email() }}<br>
        {{ form.address.label }} {{ form.address() }}<br>
        {{ form.hobby.label }} {{ form.hobby() }}<br>
        {{ form.submit() }}
    </form>
    <a href="{{ url_for('dashboard') }}">Go to Dashboard</a>
</body>
</html>
