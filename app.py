from flask import Flask, render_template
import os
from flask import Flask, request, redirect, url_for



app = Flask(__name__)



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
    return render_template('tasks.html')


@app.route('/home/createtask/create', methods=['GET', 'POST'])
def handle_task():
    if request.method == 'POST':
        # process form data
        name = request.form.get('name')
        task_type = 'type' in request.form  # checkbox returns key if checked
        subject = request.form.get('subject')
        describe = request.form.get('describe')
        # do something with the data...
        return redirect('/home/createtask')  # or wherever you want to go next
    return render_template('tasks.html')  # or your form page


@app.route('/profile/<username>')
def profile(username):
    return render_template('profile.html', username=username)


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
