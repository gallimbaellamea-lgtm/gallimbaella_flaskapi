from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------------- Models ----------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    birthday = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    course = db.Column(db.String(20), nullable=False)
    section = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    hobby = db.Column(db.String(100))
    contact_number = db.Column(db.String(20))
    guardian_name = db.Column(db.String(100))
    guardian_contact = db.Column(db.String(20))

# ---------------- Routes ----------------
@app.route('/')
def home():
    return redirect(url_for('add_student'))  # First page shows the form

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    try:
        if request.method == 'POST':
            fullname = request.form.get('fullname', '').strip()
            address = request.form.get('address', '').strip()
            birthday = request.form.get('birthday', '').strip()

            # Safely calculate age
            try:
                birth_year = int(birthday.split("-")[0])
                today = date.today()
                age = today.year - birth_year
            except Exception:
                age = 0

            sex = request.form.get('sex', '').strip()
            course = request.form.get('course', '').strip()
            section = request.form.get('section', '').strip()
            email = request.form.get('email', '').strip()
            hobby = request.form.get('hobby', '').strip()
            contact_number = request.form.get('contact_number', '').strip()
            guardian_name = request.form.get('guardian_name', '').strip()
            guardian_contact = request.form.get('guardian_contact', '').strip()

            new_student = Student(
                fullname=fullname,
                address=address,
                birthday=birthday,
                age=age,
                sex=sex,
                course=course,
                section=section,
                email=email,
                hobby=hobby,
                contact_number=contact_number,
                guardian_name=guardian_name,
                guardian_contact=guardian_contact
            )
            db.session.add(new_student)
            db.session.commit()
            return redirect(url_for('dashboard'))

        return render_template('add_student.html')

    except Exception as e:
        print("Error adding student:", e)
        return "<h2>Failed to add student. Please check your input.</h2><a href='/add'>Back to form</a>"

@app.route('/dashboard')
def dashboard():
    search_query = request.args.get('search', '').strip()
    if search_query:
        students = Student.query.filter(Student.fullname.ilike(f'%{search_query}%')).all()
    else:
        students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.fullname = request.form.get('fullname', student.fullname)
        student.address = request.form.get('address', student.address)
        student.birthday = request.form.get('birthday', student.birthday)
        try:
            birth_year = int(student.birthday.split("-")[0])
            student.age = date.today().year - birth_year
        except:
            student.age = 0
        student.sex = request.form.get('sex', student.sex)
        student.course = request.form.get('course', student.course)
        student.section = request.form.get('section', student.section)
        student.email = request.form.get('email', student.email)
        student.hobby = request.form.get('hobby', student.hobby)
        student.contact_number = request.form.get('contact_number', student.contact_number)
        student.guardian_name = request.form.get('guardian_name', student.guardian_name)
        student.guardian_contact = request.form.get('guardian_contact', student.guardian_contact)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('edit_student.html', student=student)

@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('dashboard'))

# ---------------- Main ----------------
if __name__ == '__main__':
    if not os.path.exists('students.db'):
        db.create_all()  # Create DB if it doesn't exist
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
