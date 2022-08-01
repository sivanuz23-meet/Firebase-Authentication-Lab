from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
from datetime import date
from datetime import datetime

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {

  "apiKey": "AIzaSyBflH-j9YSw2K9GnHA5TxvvceVw2lR0l00",

  "authDomain": "database-lab-3fb7c.firebaseapp.com",

  "projectId": "database-lab-3fb7c",

  "storageBucket": "database-lab-3fb7c.appspot.com",

  "messagingSenderId": "862144256115",

  "appId": "1:862144256115:web:77442267a9078423d2b206",

  "measurementId": "G-QHEETK0LS6", "databaseURL": "https://database-lab-3fb7c-default-rtdb.europe-west1.firebasedatabase.app/"

}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
today = date.today()
now = datetime.now()



@app.route('/signin', methods=['GET', 'POST'])
def signin():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('add_tweet'))
		except:
			print("Authentication Failed")
	return render_template("signin.html")

@app.route('/', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		try:
			email = request.form['email']
			password = request.form['password']
			user = {"email": email, "password": password, "full_name": request.form['full_name'], "username": request.form['username'], "bio": request.form['bio']}
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			db.child("Users").child(login_session['user']['localId']).set(user)
			return redirect(url_for('add_tweet'))
		except:
			print("error")
	return render_template("signup.html")

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
	if request.method == "POST":
		ts = now.strftime("%d/%m/%Y %H:%M:%S")
		tweet = {"title": request.form['title'], "text": request.form['text'], "uid": login_session['user']['localId'], "timestamp": ts }
		db.child("Tweets").push(tweet)
		return redirect(url_for('all_tweets'))
	return render_template("add_tweet.html")
	
@app.route('/all_tweets', methods=['GET', 'POST'])
def all_tweets():
	return render_template("all_tweets.html", tweets=db.child("Tweets").get().val())


if __name__ == '__main__':
	app.run(debug=True)