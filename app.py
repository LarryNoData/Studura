from flask import Flask, render_template
import os
from flask import Flask, request, redirect, url_for
import uuid 



app = Flask(__name__)

tasks_list = []

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
def home():
    return render_template('home.html')


@app.route('/home/createtask')
def createtask():
    return render_template('create_task.html')


@app.route('/home/tasks')
def tasks():
    return render_template('tasks.html', tasks=tasks_list)


@app.route('/home/createtask/create', methods=['GET', 'POST'])
def handle_task():
    global tasks_list

    if request.method == 'POST':
        name = request.form.get('name')
        task_type = 'type' in request.form
        subject = request.form.get('subject')
        describe = request.form.get('describe')

        tasks_list.append({
            'id': str(uuid.uuid4()),  # Generate a unique ID for the task
            'name': name,
            'type': 'Normal' if task_type else 'Other',
            'subject': subject,
            'describe': describe
        })

        return redirect('/home/tasks')

    return render_template('create.html')



@app.route('/home/tasks/delete/<task_id>', methods=['POST'])
def delete_task(task_id):
    global tasks_list
    tasks_list = [task for task in tasks_list if task['id'] != task_id]
    return redirect('/home/tasks')

@app.route('/profile/<username>')
def profile(username):
    return render_template('profile.html', username=username)


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
