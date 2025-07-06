from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Task, Exam
import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from insights import generate_study_insights
from datetime import datetime, timezone, timedelta
import json
from month_calendar import generate_month_data
from week_calendar import generate_week_data
from calendar import monthrange




print("App loaded and Flask-Migrate initialized.")



app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")


load_dotenv()


raw_url = os.getenv("DATABASE_URL")
if raw_url:
    if raw_url.startswith("postgres://"):
        raw_url = raw_url.replace("postgres://", "postgresql+psycopg://")
    elif raw_url.startswith("postgresql://"):
        raw_url = raw_url.replace("postgresql://", "postgresql+psycopg://")

    app.config["SQLALCHEMY_DATABASE_URI"] = raw_url

    #Now it's safe to print
    print("Resolved DB URI:", app.config["SQLALCHEMY_DATABASE_URI"])
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///planner.db"
    print("Using fallback SQLite DB")


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
    user_tasks = Task.query.filter_by(user_id=current_user.id).all()
    insights = generate_study_insights(user_tasks)
    today = datetime.today().date()

    tasks_due_today = Task.query.filter(
        Task.user_id == current_user.id,
        db.func.date(Task.due_date) == today,
        Task.completed_at == None
    ).all()
    
    overdue_tasks = Task.query.filter(
    Task.user_id == current_user.id,
    Task.due_date != None,
    db.func.date(Task.due_date) < today,
    Task.completed_at == None
    ).all()



    return render_template('home.html',insights=insights,tasks_due_today=tasks_due_today,overdue_tasks=overdue_tasks)

@app.route('/home/tasks')
@login_required
def tasks():
    user_tasks = Task.query.filter_by(owner=current_user).all()
    return render_template('tasks.html', tasks=user_tasks)

@app.route('/home/tasks/create', methods=['GET', 'POST'])
@login_required
def create_task():
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


        due_date = request.form.get("due_date")
        if due_date:
            new_task.due_date = datetime.strptime(due_date, "%Y-%m-%d")
                                     
        db.session.add(new_task)
        db.session.commit()

        return redirect('/home/tasks')

    origin = request.args.get('origin')
    return render_template('create.html',show_return_home=(origin == 'home'))

@app.route('/task/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        flash("You can't edit someone else's task!", "danger")
        return redirect(url_for('home'))

    if request.method == 'POST':
        task.name = request.form['name']
        task.type = request.form['type']
        task.subject = request.form['subject']
        task.describe = request.form['describe']
        date_input = request.form['due_date']
        task.due_date = datetime.strptime(date_input, '%Y-%m-%d') if date_input else None

        db.session.commit()
        flash("Task updated successfully!", "success")
        return redirect(url_for('tasks'))

    return render_template('edit_task.html', task=task)


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

@app.route('/home/tasks/complete/<int:task_id>', methods=['POST'])
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner != current_user:
        flash("You can't complete someone else's task.")
        return redirect('/home/tasks')
    
    #origin = request.form.get('origin')
    task.completed_at = datetime.now(timezone.utc)
    db.session.commit()

    #redirect_map = {
    #"/home/calendar/week": "/home/calendar/week",
    #"/home/calendar/month": "/home/calendar/month",
    #"/home/tasks": "/home/tasks/view"
    #}

    #if origin not in redirect_map:
         #Show an error message, log it, or just return a default page
    #    return "Unknown origin", 400

    #return redirect(f"{redirect_map[origin]}?origin={origin}")
    next_page = request.form.get('next')
    origin = request.form.get('origin')

    # Redirect with origin info preserved
    if next_page:
        if origin:
            return redirect(f"{next_page}?origin={origin}")
        return redirect(next_page)
    return redirect(url_for('tasks'))


    #return redirect('/home/tasks')





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

        due_date = request.form.get("due_date")
        if date:
            new_exam.date = datetime.strptime(date, "%Y-%m-%d")
        
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

@app.route('/home/exams/edit/<int:exam_id>', methods=['GET', 'POST'])
@login_required
def edit_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)

    if request.method == 'POST':
        exam.name = request.form['name']
        exam.type = request.form['type']
        exam.subject = request.form['subject']
        exam.revision = request.form['revision']
        exam.room = request.form['room']
        exam.date = datetime.strptime(request.form['date'], '%Y-%m-%d') if request.form['date'] else None

        db.session.commit()
        return redirect(url_for('view_exams', exam_id=exam.id, origin='week'))

    return render_template('edit_exam.html', exam=exam)


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


#@app.route('/home/calendar')
#@login_required
#def calendar_view():
#    tasks = Task.query.filter_by(user_id=current_user.id).all()
#    events = []
#    for task in tasks:
#        if task.due_date:
#            events.append({
#                'title': task.name,
#                'start': task.due_date.strftime('%Y-%m-%d'),
#                'color': '#007bff' if not task.completed_at else '#00b3ff'
#            })

 #   exams = Exam.query.filter_by(owner_id=current_user.id).all()
  #  for exam in exams:
   #     if exam.date:
    #        events.append({
     #           'title': exam.name,
      #          'start': exam.date.strftime('%Y-%m-%d'),
       #         'color': '#007bff' if not exam.completed_at_exam else '#00b3ff'
        #    })
   # return render_template("calendar.html", calendar_tasks=json.dumps(events))


@app.route('/home/calendar/month')
@login_required
def calendar_month():
    # Get current month/year or use query
    month = request.args.get('month', datetime.today().month, type=int)
    year = request.args.get('year', datetime.today().year, type=int)

    # Calculate previous/next month
    prev_month = month - 1 or 12
    prev_year = year - 1 if month == 1 else year
    next_month = month + 1 if month < 12 else 1
    next_year = year + 1 if month == 12 else year

    # Create a display date for header
    display_date = datetime(year, month, 1)

    # Query data
    tasks = Task.query.filter_by(owner=current_user).all()
    exams = Exam.query.filter_by(owner=current_user).all()
    calendar_days = generate_month_data(year, month, tasks, exams)

    return render_template(
        'calendar_month.html',
        calendar_days=calendar_days,
        display_date=display_date,
        month=month, year=year,
        prev_month=prev_month, prev_year=prev_year,
        next_month=next_month, next_year=next_year
    )



@app.route('/home/calendar/week')
@login_required
def calendar_week():
    ref_date_str = request.args.get('date')
    ref_date = datetime.strptime(ref_date_str, '%Y-%m-%d') if ref_date_str else datetime.today()

    # Calculate previous and next week
    prev_date = ref_date - timedelta(days=7)
    next_date = ref_date + timedelta(days=7)

    tasks = Task.query.filter_by(owner=current_user).all()
    exams = Exam.query.filter_by(owner=current_user).all()
    week_days = generate_week_data(ref_date, tasks, exams)

    return render_template(
        'calendar_week.html',
        week_days=week_days,
        today=ref_date,
        prev_date=prev_date.strftime('%Y-%m-%d'),
        next_date=next_date.strftime('%Y-%m-%d')
    )


@app.route('/home/tasks/view/<int:task_id>')
@login_required
def view_task(task_id):
    task = Task.query.get_or_404(task_id)
    origin = request.args.get('origin')
    return render_template('tasks.html', single_task=task, origin=origin)


@app.route('/home/exams/view/<int:exam_id>')
@login_required
def view_exam_from_calendar(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    origin = request.args.get('origin')
    return render_template('exams.html', single_exam=exam, origin=origin)




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