from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Task, Exam
import os
from dotenv import load_dotenv
from flask_migrate import Migrate


print("App loaded and Flask-Migrate initialized.")



app = Flask(__name__)

load_dotenv()


raw_url = os.getenv("DATABASE_URL")
if raw_url:
    # Adjust prefix if Render gives 'postgres://'
    if raw_url.startswith("postgres://"):
        raw_url = raw_url.replace("postgres://", "postgresql+psycopg://")
    app.config["SQLALCHEMY_DATABASE_URI"] = raw_url
    print("📡 Resolved DB URI:", app.config["SQLALCHEMY_DATABASE_URI"]) 
else:
    # Default to a local SQLite file
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///planner.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Initialize DB
db.init_app(app)

#makemigrations
migrate = Migrate()
migrate.init_app(app, db)


# Setup Login Manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/home/createtask')
@login_required
def createtask():
    return render_template('create_task.html')

@app.route('/home/tasks')
@login_required
def tasks():
    user_tasks = Task.query.filter_by(owner=current_user).all()
    return render_template('tasks.html', tasks=user_tasks)

@app.route('/home/createtask/create', methods=['GET', 'POST'])
@login_required
def handle_task():
    if request.method == 'POST':
        name = request.form.get('name')
        task_type = 'Normal' if 'type' in request.form else 'Other'
        subject = request.form.get('subject')
        describe = request.form.get('describe')

        new_task = Task(
            name=name,
            type=task_type,
            subject=subject,
            describe=describe,
            owner=current_user
        )
        db.session.add(new_task)
        db.session.commit()

        return redirect('/home/tasks')

    return render_template('create.html')

@app.route('/home/tasks/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    if task.owner != current_user:
        flash("You can't delete someone else's task.")
        return redirect('/home/tasks')

    db.session.delete(task)
    db.session.commit()
    return redirect('/home/tasks')




@app.route('/home/create/exam', methods=['GET', 'POST'])
@login_required
def create_exam():
    if request.method == 'POST':
        name = request.form.get('exam')
        type = 'Normal' if 'type' in request.form else 'Other'
        subject = request.form.get('subject')
        revision = request.form.get('revision')
        room = request.form.get('room')
        date = request.form.get('date')

        new_exam = Exam(
            name=name,
            type=type,
            subject=subject,
            revision=revision,
            date=date,
            room=room,
            owner=current_user
        )
        db.session.add(new_exam)
        db.session.commit()

        return redirect('/home/exams')

    return render_template('create_exam.html')



@app.route('/home/exams')
@login_required
def view_exams():
    user_exams = Exam.query.filter_by(owner=current_user).all()
    return render_template('exams.html', exams=user_exams)


@app.route('/home/exams/delete/<int:exam_id>', methods=['POST'])
@login_required
def delete_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)

    if exam.owner != current_user:
        flash("You can't delete someone else's exam.")
        return redirect('/home/exams')

    db.session.delete(exam)
    db.session.commit()
    return redirect('/home/exams')



@app.route('/home/profile/')
@login_required
def profile():
    return render_template('profile.html', username = current_user.username)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect('/register')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect('/home')
        flash('Invalid credentials.')
    return render_template('login.html')

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current = request.form['current_password']
        new = request.form['new_password']
        confirm = request.form['confirm_new_password']

        if not check_password_hash(current_user.password, current):
            flash('Current password is incorrect.')
        elif new != confirm:
            flash('New passwords do not match.')
        else:
            current_user.password = generate_password_hash(new)
            db.session.commit()
            flash('Password updated successfully!')

    return render_template('change_password.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)