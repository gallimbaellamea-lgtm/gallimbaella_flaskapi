from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date

# ---------------- Flask Setup ----------------
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
    course = db.Column(db.String(10))
    section = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    hobby = db.Column(db.String(100))
    contact_number = db.Column(db.String(20))
    guardian_name = db.Column(db.String(100))
    guardian_contact = db.Column(db.String(20))

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

with app.app_context():
    db.create_all()

# ---------------- Routes ----------------

# First page: Add student if none exist, else dashboard
@app.route('/')
def first_student_form():
    if Student.query.count() == 0:
        return redirect(url_for('add_student'))
    else:
        return redirect(url_for('index'))

# Dashboard
@app.route('/index')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

# Search
@app.route('/search', methods=['GET'])
def search_student():
    query = request.args.get('q', '')
    students = Student.query.filter(Student.fullname.ilike(f'%{query}%')).all()
    return render_template('index.html', students=students, search_query=query)

# Add student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        data = request.form
        birthday = data['birthday']
        age = date.today().year - int(birthday.split('-')[0])
        new_student = Student(
            fullname=data['fullname'], address=data['address'], birthday=birthday,
            age=age, sex=data['sex'], course=data['course'], section=data['section'],
            email=data['email'], hobby=data['hobby'], contact_number=data['contact_number'],
            guardian_name=data['guardian_name'], guardian_contact=data['guardian_contact']
        )
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', student=None)

# Edit student
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        student.fullname = data['fullname']
        student.address = data['address']
        student.birthday = data['birthday']
        student.age = date.today().year - int(student.birthday.split('-')[0])
        student.sex = data['sex']
        student.course = data['course']
        student.section = data['section']
        student.email = data['email']
        student.hobby = data['hobby']
        student.contact_number = data['contact_number']
        student.guardian_name = data['guardian_name']
        student.guardian_contact = data['guardian_contact']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', student=student)

# Delete student
@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

# ---------------- API Endpoints ----------------
@app.route('/api/students', methods=['GET'])
def api_get_students():
    return jsonify([s.to_dict() for s in Student.query.all()])

@app.route('/api/students/<int:id>', methods=['GET'])
def api_get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify(student.to_dict())

# ---------------- Run App ----------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
