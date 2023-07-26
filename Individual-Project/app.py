from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase














config = {"apiKey": "AIzaSyDHHJF-ONEvENl2sU5DnMfoHFvF3WRZb5M",
  "authDomain": "csproject-e0061.firebaseapp.com",
  "databaseURL": "https://csproject-e0061-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "csproject-e0061",
  "storageBucket": "csproject-e0061.appspot.com",
  "messagingSenderId": "775744400663",
  "appId": "1:775744400663:web:ee825397f3c2e0e5fe1b52",
  "databaseURL":"https://csproject-e0061-default-rtdb.europe-west1.firebasedatabase.app/"}












firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()







app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here

@app.route('/', methods=['GET', 'POST'])
def signin():
    error=""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user']=auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('add_tweet'))
        except:
            error =" authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        username = request.form['username']
        bio = request.form['bio']

        try:
            login_session['user'] = auth.create_user_with_email_and_password(email,password)
            UID = login_session['user']['localId']
            user = {"email": email,"name":name,"username":username,"bio":bio}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('add_tweet'))
        except Exception as e:
            error = "authentecation failed"
            print("Exception in sign up:", e)
    return render_template("signup.html")



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        title= request.form['title']
        text = request.form['text']
        try:
            tweet = {"title": title,"text": text}
            db.child("Tweets").push(tweet)
            return redirect(url_for('all_tweets'))
        except:
            print("Couldn't add tweet")
    name=db.child("Users").child(login_session['user']['localId']).get().val()
    print(name)
    return render_template("add_tweet.html",name = name)


@app.route('/signout')
def signout():
    auth_current_user = None
    login_session['user'] = None
    return redirect(url_for('signin'))

@app.route('/all_tweets')
def all_tweets():
    tweets = db.child("Tweets").get().val()
    return render_template("all_tweets.html", tweets=tweets)


#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)