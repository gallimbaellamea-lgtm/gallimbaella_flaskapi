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
