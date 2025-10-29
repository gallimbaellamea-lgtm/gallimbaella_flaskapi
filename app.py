from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    grade = db.Column(db.String(20), nullable=True)
    section = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    students = Student.query.order_by(Student.created_at.desc()).all()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        fname = request.form.get('first_name', '').strip()
        lname = request.form.get('last_name', '').strip()
        grade = request.form.get('grade', '').strip()
        section = request.form.get('section', '').strip()
        email = request.form.get('email', '').strip()

        if not fname or not lname:
            flash('First name and last name are required.', 'danger')
            return redirect(url_for('add_student'))

        student = Student(first_name=fname, last_name=lname, grade=grade, section=section, email=email)
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully.', 'success')
        return redirect(url_for('index'))

    return render_template('form.html')

@app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        student.first_name = request.form.get('first_name', student.first_name).strip()
        student.last_name = request.form.get('last_name', student.last_name).strip()
        student.grade = request.form.get('grade', student.grade).strip()
        student.section = request.form.get('section', student.section).strip()
        student.email = request.form.get('email', student.email).strip()

        if not student.first_name or not student.last_name:
            flash('First name and last name are required.', 'danger')
            return redirect(url_for('edit_student', student_id=student.id))

        db.session.commit()
        flash('Student updated successfully.', 'success')
        return redirect(url_for('index'))

    return render_template('edit.html', student=student)

@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
