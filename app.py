from flask import Flask, render_template, redirect, url_for, request, jsonify
from models import db, Student
from forms import StudentForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

# ---------- HTML Form Routes ----------
@app.route('/', methods=['GET', 'POST'])
def index():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(
            full_name=form.full_name.data,
            birthday=form.birthday.data,
            sex=form.sex.data,
            course=form.course.data,
            section=form.section.data,
            email=form.email.data,
            address=form.address.data,
            hobby=form.hobby.data,
            contact_number=form.contact_number.data,
            guardian_name=form.guardian_name.data,
            guardian_contact=form.guardian_contact.data
        )
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('index.html', form=form)

@app.route('/dashboard')
def dashboard():
    students = Student.query.all()
    return render_template('dashboard.html', students=students)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        form.populate_obj(student)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('index.html', form=form, edit=True)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('dashboard'))

# ---------- API Routes ----------
@app.route('/api/students', methods=['GET'])
def api_students():
    students = Student.query.all()
    return jsonify([{
        "id": s.id,
        "full_name": s.full_name,
        "age": s.age,
        "birthday": s.birthday.strftime("%Y-%m-%d"),
        "sex": s.sex,
        "course": s.course,
        "section": s.section,
        "email": s.email,
        "address": s.address,
        "hobby": s.hobby,
        "contact_number": s.contact_number,
        "guardian_name": s.guardian_name,
        "guardian_contact": s.guardian_contact
    } for s in students])

@app.route('/api/student/<int:id>', methods=['GET'])
def api_student(id):
    s = Student.query.get_or_404(id)
    return jsonify({
        "id": s.id,
        "full_name": s.full_name,
        "age": s.age,
        "birthday": s.birthday.strftime("%Y-%m-%d"),
        "sex": s.sex,
        "course": s.course,
        "section": s.section,
        "email": s.email,
        "address": s.address,
        "hobby": s.hobby,
        "contact_number": s.contact_number,
        "guardian_name": s.guardian_name,
        "guardian_contact": s.guardian_contact
    })

if __name__ == '__main__':
    app.run(debug=True)
