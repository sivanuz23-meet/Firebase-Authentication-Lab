from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {

  "apiKey": "AIzaSyBflH-j9YSw2K9GnHA5TxvvceVw2lR0l00",

  "authDomain": "database-lab-3fb7c.firebaseapp.com",

  "projectId": "database-lab-3fb7c",

  "storageBucket": "database-lab-3fb7c.appspot.com",

  "messagingSenderId": "862144256115",

  "appId": "1:862144256115:web:77442267a9078423d2b206",

  "measurementId": "G-QHEETK0LS6", "databaseURL": ""

}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


@app.route('/', methods=['GET', 'POST'])
def signin():
	if request.method == 'POST':
		try:
			login_session['email'] = request.form['email']
			login_session['password'] = request.form['password']
			return redirect(url_for('add_tweet'))
		except:
			print("Authentication Failed")
			return render_template("signin.html")
	return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		try:
			login_session['email'] = request.form['email']
			login_session['password'] = request.form['password']
			return redirect(url_for('add_tweet'))
		except:
			print("Authentication Failed")
			return render_template("signup.html")
	return render_template("signup.html")

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)