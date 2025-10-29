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
    address = db.Column(db.String(200), nullable=False)
    birthday = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer)
    sex = db.Column(db.String(10))
    course = db.Column(db.String(10))
    section = db.Column(db.String(10))
    email = db.Column(db.String(100))
    hobby = db.Column(db.String(100))
    contact_number = db.Column(db.String(20))
    guardian_name = db.Column(db.String(100))
    guardian_contact = db.Column(db.String(20))

    def __repr__(self):
        return f"<Student {self.fullname}>"

# ---------------- Initialize Database ----------------
with app.app_context():
    db.create_all()

# ---------------- Routes ----------------
@app.route('/', methods=['GET'])
def index():
    search_query = request.args.get('search', '')
    if search_query:
        students = Student.query.filter(Student.fullname.contains(search_query)).all()
    else:
        students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        birthday_str = request.form['birthday']
        birth_date = datetime.strptime(birthday_str, '%Y-%m-%d')
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        new_student = Student(
            fullname=request.form['fullname'],
            address=request.form['address'],
            birthday=birthday_str,
            age=age,
            sex=request.form['sex'],
            course=request.form['course'],
            section=request.form['section'],
            email=request.form['email'],
            hobby=request.form.get('hobby',''),
            contact_number=request.form['contact_number'],
            guardian_name=request.form['guardian_name'],
            guardian_contact=request.form['guardian_contact']
        )
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', student=None)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        birthday_str = request.form['birthday']
        birth_date = datetime.strptime(birthday_str, '%Y-%m-%d')
        today = date.today()
        student.age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        student.fullname = request.form['fullname']
        student.address = request.form['address']
        student.birthday = birthday_str
        student.sex = request.form['sex']
        student.course = request.form['course']
        student.section = request.form['section']
        student.email = request.form['email']
        student.hobby = request.form.get('hobby','')
        student.contact_number = request.form['contact_number']
        student.guardian_name = request.form['guardian_name']
        student.guardian_contact = request.form['guardian_contact']

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', student=student)

@app.route('/delete/<int:id>', methods=['GET'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

# ---------------- Run App ----------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
