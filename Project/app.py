from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import re
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import mysql.connector
from passlib.hash import bcrypt
import os

app = Flask(__name__,static_folder='static')  
app.secret_key = os.environ.get('SECRET_KEY')

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='login'
)

@app.route('/')
def home():
    return render_template('home.html')

app.secret_key = 'my_super_secret_key_1234'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username exists in the database
        cursor = db.cursor()
        cursor.execute("SELECT * FROM logintable WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            storedHashedPassword = user[2]

            # Verify the entered password
            if bcrypt.verify(password, storedHashedPassword):
                session['loggedin'] = True
                session['username'] = username

                print(session['loggedin'])
                print(session['username'])
                
                return redirect('/index')
            else:
                error = 'Invalid password.'
                return render_template('login.html', error=error)
        else:
            error = 'Invalid username.'
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['reg-username']
        password = request.form['reg-password']
        confirm_password = request.form['confirm-password']
        email = request.form['email']

        if password != confirm_password:
            return " Passwords do not match."
        
        # Check if the username already exists
        cursor = db.cursor()
        cursor.execute("SELECT * FROM logintable WHERE username = %s", (username,))
        if cursor.fetchone():
            return "Username already exists."

        # Insert the user data into the database
        hashed_password = bcrypt.hash(password)
        cursor.execute("INSERT INTO logintable (username, password, email) VALUES (%s, %s, %s)", (username, hashed_password, email))
        db.commit()
        cursor.close()

        return redirect(url_for('login'))

    return render_template('registration.html')

    
 
    

@app.route('/index')
def index():
    if 'loggedin' in session:
        return render_template('index.html')
    else:
        return redirect('/login')

with open('ensemble_model.pkl', 'rb') as file:
    ensemble_model = pickle.load(file)

with open('vectorizer.pkl', 'rb') as file:
    vectorizer = pickle.load(file)

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d', '', text)
    text = text.strip()
    return text

@app.route('/classify-review', methods=['POST'])
def classify_review():
    review = request.form.get('review')

    if not review:
        return jsonify({'result': 'Not submit'})

    preprocessed_review = preprocess_text(review)
    review_vectorized = vectorizer.transform([preprocessed_review]) 
    prediction = ensemble_model.predict(review_vectorized)
    print(prediction)

    result = 'fake' if prediction[0] == 'fake' else 'genuine'

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
