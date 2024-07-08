# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define a model for the student table
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enrollment_number = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    course = db.Column(db.String(50), nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)
    grade = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Student {self.name}>'

# Flask-WTF form for student creation
class StudentForm(FlaskForm):
    enrollment_number = StringField('Enrollment Number', validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    age = IntegerField('Age', validators=[InputRequired(), NumberRange(min=0, max=150)])
    address = StringField('Address', validators=[InputRequired()])
    course = StringField('Course', validators=[InputRequired()])
    branch = StringField('Branch', validators=[InputRequired()])
    mobile_number = StringField('Mobile Number', validators=[InputRequired()])
    grade = StringField('Grade', validators=[InputRequired()])
    submit = SubmitField('Submit')

# Create the database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        new_student = Student(
            enrollment_number=form.enrollment_number.data,
            name=form.name.data,
            age=form.age.data,
            address=form.address.data,
            course=form.course.data,
            branch=form.branch.data,
            mobile_number=form.mobile_number.data,
            grade=form.grade.data
        )
        db.session.add(new_student)
        db.session.commit()
        flash('Student added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_student.html', form=form)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.enrollment_number = form.enrollment_number.data
        student.name = form.name.data
        student.age = form.age.data
        student.address = form.address.data
        student.course = form.course.data
        student.branch = form.branch.data
        student.mobile_number = form.mobile_number.data
        student.grade = form.grade.data
        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_student.html', form=form)


if __name__ == '__main__':
    app.run(port=8000)
    app.run(debug=True)