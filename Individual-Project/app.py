from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import random


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here


config = {
  
  'apiKey': "AIzaSyDEAvsWYW4hL_HsQfPCQMn3XNlcdtmbc4Y",
  "authDomain": "quote-of-the-day-5694b.firebaseapp.com",
  "projectId": "quote-of-the-day-5694b",
  'storageBucket': "quote-of-the-day-5694b.appspot.com",
  "messagingSenderId": "522608685007",
  "appId": "1:522608685007:web:ff37c3ba7f27bd60a6ecba",
  "databaseURL": "https://quote-of-the-day-5694b-default-rtdb.europe-west1.firebasedatabase.app/"
}


firebase = pyrebase.initialize_app(config)
auth= firebase.auth()
db = firebase.database()



mylist = ["If you’re going through hell, keep going.", "Don’t let yesterday take up too much of today.", "Nothing is impossible. The word itself says “I’m possible!","Everything has beauty, but not everyone sees it","Whatever you are, be a good one","You do not find the happy life. You make it"]
random_choice = random.choice(mylist)


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        error = ""
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('see_quote'))
        except Exception as e:
            print('SIGN IN ERROR:', e)
            error = "Authenication Error"
            print(error)
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        full_name= request.form['full_name']
        username = request.form['username']     
      

        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"email":email, "fullname":full_name ,"username" :username , }
            UID = login_session['user']['localId']
            db.child("Users").child(UID).set(user)
            return redirect(url_for('see_quote'))
        except Exception as e:
            print("SIGN UP ERROR:", e) 
            error = "Authenication Error"
            return redirect(url_for('signup'))
    return render_template("signup.html")




@app.route('/see_quote', methods=['GET', 'POST'])
def see_quote():
    return render_template('random_quote.html', choice = random_choice)



@app.route('/add_quote', methods=['GET', 'POST'])
def add_qot():
    if request.method == 'POST':
        uid = login_session['user']['localId']
        title = request.form['title']
        text = request.form['text']
        saved= {'quote': title, 'experience': text, 'uid': uid}
        db.child('All').push(saved)
        return redirect(url_for('allquotes'))

    return render_template("add_quote.html")


@app.route("/all_quote")
def allquotes():
    saved = db.child("All").get().val()
    return render_template("all_qoute.html", saved = saved)

#Code goes above here

if __name__ == '__main__':
    app.run(debug=True, port=5002)