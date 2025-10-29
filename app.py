from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------------- Models ----------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    birthday = db.Column(db.Date)
    age = db.Column(db.Integer)
    sex = db.Column(db.String(10))
    course = db.Column(db.String(50))
    section = db.Column(db.String(50))
    email = db.Column(db.String(100))
    hobby = db.Column(db.String(100))
    contact_number = db.Column(db.String(20))
    guardian_name = db.Column(db.String(100))
    guardian_contact = db.Column(db.String(20))

# ---------------- Routes ----------------
@app.route('/', methods=['GET'])
def index():
    search_query = request.args.get('search', '')
    if search_query:
        students = Student.query.filter(Student.fullname.ilike(f"%{search_query}%")).all()
    else:
        students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        birthday = request.form['birthday']
        birth_date = date.fromisoformat(birthday)
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        student = Student(
            fullname=request.form['fullname'],
            address=request.form['address'],
            birthday=birth_date,
            age=age,
            sex=request.form['sex'],
            course=request.form['course'],
            section=request.form['section'],
            email=request.form['email'],
            hobby=request.form['hobby'],
            contact_number=request.form['contact_number'],
            guardian_name=request.form['guardian_name'],
            guardian_contact=request.form['guardian_contact']
        )
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', student=None)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        birthday = request.form['birthday']
        birth_date = date.fromisoformat(birthday)
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        student.fullname = request.form['fullname']
        student.address = request.form['address']
        student.birthday = birth_date
        student.age = age
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

@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
