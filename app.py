from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "supersecretkey"
db = SQLAlchemy(app)

# ----------------- Model -----------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    birthday = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    course = db.Column(db.String(20), nullable=False)
    section = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    hobby = db.Column(db.String(100))
    contact_number = db.Column(db.String(20))
    guardian_name = db.Column(db.String(100))
    guardian_contact = db.Column(db.String(20))

# ----------------- Routes -----------------
@app.route('/')
def dashboard():
    search_query = request.args.get('search')
    if search_query:
        students = Student.query.filter(Student.fullname.ilike(f"%{search_query}%")).all()
    else:
        students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        try:
            fullname = request.form['fullname']
            address = request.form['address']
            birthday = request.form['birthday']
            birth_date = datetime.strptime(birthday, "%Y-%m-%d").date()
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            sex = request.form['sex']
            course = request.form['course']
            section = request.form['section']
            email = request.form['email']
            hobby = request.form.get('hobby', '')
            contact_number = request.form.get('contact_number', '')
            guardian_name = request.form.get('guardian_name', '')
            guardian_contact = request.form.get('guardian_contact', '')

            student = Student(
                fullname=fullname, address=address, birthday=birthday, age=age,
                sex=sex, course=course, section=section, email=email,
                hobby=hobby, contact_number=contact_number,
                guardian_name=guardian_name, guardian_contact=guardian_contact
            )
            db.session.add(student)
            db.session.commit()
            flash("Student added successfully!", "success")
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            print("Error:", e)
            flash("Failed to add student. Please check your input.", "danger")
            return redirect(url_for('add_student'))
    return render_template('add_student.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        try:
            student.fullname = request.form['fullname']
            student.address = request.form['address']
            student.birthday = request.form['birthday']
            birth_date = datetime.strptime(student.birthday, "%Y-%m-%d").date()
            today = date.today()
            student.age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            student.sex = request.form['sex']
            student.course = request.form['course']
            student.section = request.form['section']
            student.email = request.form['email']
            student.hobby = request.form.get('hobby', '')
            student.contact_number = request.form.get('contact_number', '')
            student.guardian_name = request.form.get('guardian_name', '')
            student.guardian_contact = request.form.get('guardian_contact', '')

            db.session.commit()
            flash("Student updated successfully!", "success")
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            print("Error:", e)
            flash("Failed to update student. Please check your input.", "danger")
            return render_template('edit_student.html', student=student)
    return render_template('edit_student.html', student=student)

@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    try:
        db.session.delete(student)
        db.session.commit()
        flash("Student deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        print("Error:", e)
        flash("Failed to delete student.", "danger")
    return redirect(url_for('dashboard'))

# ----------------- Initialize DB -----------------
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
