from flask import Flask, render_template
import os
import logging
from flask import Flask, request


app = Flask(__name__)




# Configure logging to show messages in the terminal
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@app.before_request
def log_request():
    logging.info(f"Incoming request: {request.method} {request.path} from {request.remote_addr}")




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/profile/<username>')
def profile(username):
    return render_template('profile.html', username=username)


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
