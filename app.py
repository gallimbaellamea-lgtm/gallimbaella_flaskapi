from flask import Flask, render_template, redirect, url_for, request
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

# Create + Read
@app.route('/', methods=['GET', 'POST'])
def index():
    form = StudentForm()
    if form.validate_on_submit():
        new_student = Student(
            full_name=form.full_name.data,
            birthday=form.birthday.data,
            course=form.course.data,
            section=form.section.data,
            sex=form.sex.data,
            email=form.email.data,
            address=form.address.data,
            hobby=form.hobby.data
        )
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('index.html', form=form)

# Read Dashboard
@app.route('/dashboard')
def dashboard():
    students = Student.query.all()
    return render_template('dashboard.html', students=students)

# Update
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.full_name = form.full_name.data
        student.birthday = form.birthday.data
        student.course = form.course.data
        student.section = form.section.data
        student.sex = form.sex.data
        student.email = form.email.data
        student.address = form.address.data
        student.hobby = form.hobby.data
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('index.html', form=form, edit=True)

# Delete
@app.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
