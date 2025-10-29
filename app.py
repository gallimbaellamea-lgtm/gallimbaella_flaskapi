from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------------- Models ----------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    birthday = db.Column(db.String(20))
    age = db.Column(db.Integer)
    sex = db.Column(db.String(10))
    course = db.Column(db.String(50))
    section = db.Column(db.String(50))
    email = db.Column(db.String(100))
    hobby = db.Column(db.String(200))
    contact_number = db.Column(db.String(50))
    guardian_name = db.Column(db.String(100))
    guardian_contact = db.Column(db.String(50))

# ---------------- Initialize DB ----------------
with app.app_context():
    db.create_all()  # <- ensures the table exists

# ---------------- Routes ----------------

# Index / Dashboard
@app.route('/')
def index():
    search = request.args.get('search', '')
    if search:
        students = Student.query.filter(Student.fullname.contains(search)).all()
    else:
        students = Student.query.all()
    return render_template('index.html', students=students)

# Add Student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        fullname = request.form['fullname']
        address = request.form['address']
        birthday = request.form['birthday']
        age = calculate_age(birthday)
        sex = request.form['sex']
        course = request.form['course']
        section = request.form['section']
        email = request.form['email']
        hobby = request.form['hobby']
        contact_number = request.form['contact_number']
        guardian_name = request.form['guardian_name']
        guardian_contact = request.form['guardian_contact']

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
        return redirect(url_for('index'))
    return render_template('form.html', student=None)

# Edit Student
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.fullname = request.form['fullname']
        student.address = request.form['address']
        student.birthday = request.form['birthday']
        student.age = calculate_age(student.birthday)
        student.sex = request.form['sex']
        student.course = request.form['course']
        student.section = request.form['section']
        student.email = request.form['email']
        student.hobby = request.form['hobby']
        student.contact_number = request.form['contact_number']
        student.guardian_name = request.form['guardian_name']
        student.guardian_contact = request.form['guardian_contact']

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', student=student)

# Delete Student
@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

# ---------------- Utility ----------------
def calculate_age(birthday_str):
    try:
        birth_date = datetime.strptime(birthday_str, "%Y-%m-%d").date()
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    except:
        return 0

# ---------------- Run ----------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
