from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    birthday = db.Column(db.String(20))
    age = db.Column(db.Integer)
    sex = db.Column(db.String(10))
    course = db.Column(db.String(10))
    section = db.Column(db.String(20))
    email = db.Column(db.String(100))
    hobby = db.Column(db.String(100))
    contact_number = db.Column(db.String(20))
    guardian_name = db.Column(db.String(100))
    guardian_contact = db.Column(db.String(20))

    def to_dict(self):
        return {
            "id": self.id,
            "fullname": self.fullname,
            "address": self.address,
            "birthday": self.birthday,
            "age": self.age,
            "sex": self.sex,
            "course": self.course,
            "section": self.section,
            "email": self.email,
            "hobby": self.hobby,
            "contact_number": self.contact_number,
            "guardian_name": self.guardian_name,
            "guardian_contact": self.guardian_contact
        }

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        data = request.form
        birthday = data['birthday']
        birth_year = int(birthday.split('-')[0])
        today = date.today()
        age = today.year - birth_year

        new_student = Student(
            fullname=data['fullname'],
            address=data['address'],
            birthday=birthday,
            age=age,
            sex=data['sex'],
            course=data['course'],
            section=data['section'],
            email=data['email'],
            hobby=data['hobby'],
            contact_number=data['contact_number'],
            guardian_name=data['guardian_name'],
            guardian_contact=data['guardian_contact']
        )
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', student=None)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        student.fullname = data['fullname']
        student.address = data['address']
        student.birthday = data['birthday']
        birth_year = int(student.birthday.split('-')[0])
        today = date.today()
        student.age = today.year - birth_year
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

@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/api/students', methods=['GET'])
def api_get_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students])

@app.route('/api/students/<int:id>', methods=['GET'])
def api_get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify(student.to_dict())

@app.route('/api/students', methods=['POST'])
def api_add_student():
    data = request.json
    birthday = data.get('birthday', '2000-01-01')
    birth_year = int(birthday.split('-')[0])
    today = date.today()
    age = today.year - birth_year

    new_student = Student(
        fullname=data['fullname'],
        address=data.get('address', ''),
        birthday=birthday,
        age=age,
        sex=data.get('sex',''),
        course=data.get('course',''),
        section=data.get('section',''),
        email=data.get('email',''),
        hobby=data.get('hobby',''),
        contact_number=data.get('contact_number',''),
        guardian_name=data.get('guardian_name',''),
        guardian_contact=data.get('guardian_contact','')
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify(new_student.to_dict()), 201

@app.route('/api/students/<int:id>', methods=['PUT'])
def api_update_student(id):
    student = Student.query.get_or_404(id)
    data = request.json
    student.fullname = data.get('fullname', student.fullname)
    student.address = data.get('address', student.address)
    student.birthday = data.get('birthday', student.birthday)
    birth_year = int(student.birthday.split('-')[0])
    today = date.today()
    student.age = today.year - birth_year
    student.sex = data.get('sex', student.sex)
    student.course = data.get('course', student.course)
    student.section = data.get('section', student.section)
    student.email = data.get('email', student.email)
    student.hobby = data.get('hobby', student.hobby)
    student.contact_number = data.get('contact_number', student.contact_number)
    student.guardian_name = data.get('guardian_name', student.guardian_name)
    student.guardian_contact = data.get('guardian_contact', student.guardian_contact)
    db.session.commit()
    return jsonify(student.to_dict())

@app.route('/api/students/<int:id>', methods=['DELETE'])
def api_delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message":"Student deleted successfully"})

if __name__ == '__main__':
    db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
