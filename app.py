'''
------------------------------

Tutor Center

Authors: Jason, Evan, Raghav, Amogh

------------------------------
'''



from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
import hashlib
import os
import random
import json
import requests



'''
App config
------------------------------
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

'''
------------------------------
'''

def toHash(value:str):
    '''
    Hashes string
    
    Parameters: string to hash
    Return: hashed string
    '''
    hash_obj = hashlib.sha256(bytes(value, 'utf8'))
    return hash_obj.hexdigest()

# Database models

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))

class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    phone_number = db.Column(db.String(10))
    pay = db.Column(db.Integer)
    description = db.Column(db.String(10000))
    subject = db.Column(db.String(100))
    grade = db.Column(db.Integer)
    average_stars = db.Column(db.Integer)
    image = db.Column(db.String(5000))
    num_stars = db.Column(db.Integer)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer)
    title = db.Column(db.String(250))
    username = db.Column(db.String(64))
    rating = db.Column(db.Integer)
    content = db.Column(db.String(10000))

subjects = ["All", "Math", "English", "Physics", "French", "Science", "Spanish", "Computer Science"]
grades = ["All", "5", "6", "7", "8", "9", "10", "11", "12"]

def generateRandomTutor():
    '''
    Generates fake tutors and inserts into database
    For demonstration purposes
    '''
    with open('tutorRandomJSON/tutornames.json') as f:
        json_file = json.load(f)
        name = json_file[random.randint(0, 4945)]
    with open('tutorRandomJSON/tutorimages.json') as f:
        json_file = json.load(f)
        imageURL = json_file[random.randint(0, 13)]
    with open('tutorRandomJSON/tutordescriptions.json') as f:
        json_file = json.load(f)
        desc = json_file[random.randint(0, 4)]
    title = Tutor(name=name, email=f"{name.lower()}@fake_email.com", phone_number=str(random.randint(1000000000, 9999999999)), pay=random.randint(20, 40), description=desc, subject=subjects[random.randint(1, len(subjects)-1)], grade=grades[random.randint(1, len(grades)-1)], average_stars=0, image=imageURL, num_stars=0)
    db.session.add(title)
    db.session.commit()

@app.route('/index.html')
@app.route('/')
def index():
    return render_template('index.html', session=session, title="Home")

@app.route('/start-up')
def start_up():
    return render_template('start-up.html')

@app.route('/become-tutor', methods=['GET', 'POST'])
def become_tutor():

    if not "user" in session:
        return redirect(url_for('index'))

    if request.method == 'POST':

        name = request.form["name"]
        email = session["user"]
        phone_number = request.form["phone-number"]
        pay = request.form["pay"]
        description = request.form["description"]
        subject = request.form["subject"]
        grade = request.form["grade"]
        average_stars = 0
        image = request.form["image"]
        num_stars = 0

        success = True

        try: 
            if int(pay) > 40:
                success = False
                flash('Rate must be under $40', 'danger')
            int(grade)
        except:
            success = False
            flash("Invalid rate or grade.", 'danger')

        if not name:
            flash('Please enter a name.', 'danger')
            success = False
        if not phone_number:
            flash('Please enter a phone number.', 'danger')
            success = False
        if not pay:
            flash('Please enter a rate.', 'danger')
            success = False
        if not description:
            flash('Please enter a description.', 'danger')
            success = False
        if not subject:
            flash('Please enter a subject.', 'danger')
            success = False
        if not grade:
            flash('Please enter a grade.', 'danger')
            success = False
        if image:
            # check if image exists
            image_formats = ("image/png", "image/jpeg", "image/jpg")
            try:
                img = requests.head(image)
                if not img.headers["content-type"] in image_formats:
                    flash('Invalid image url.', 'danger')
                    success = False
            except:
                flash('Invalid image url.', 'danger')
                success = False

        if success:
            tutor = Tutor(name=name, email=email, phone_number=phone_number, pay=pay, description=description, subject=subject, grade=grade, average_stars=average_stars, image=image, num_stars=num_stars)
            db.session.add(tutor)
            db.session.commit()

            flash(f'You have now become a tutor! Go to grade {grade} {subject} to see yourself!', 'success')
            return redirect(url_for('tutors'))

    return render_template('create_tutor.html', title='Become Tutor', session=session)

@app.route('/tutors', methods=['GET', 'POST'])
def tutors():

    if not "user" in session:
        return redirect(url_for('index'))

    tutors = []

    subject, grade = "All", "All"
    tutors = Tutor.query.order_by(Tutor.average_stars).all()

    if request.method == 'POST':
        subject = request.form["subject"]
        grade = request.form["grade"]

        if subject == "All" and grade == "All":
            tutors = Tutor.query.all()
        elif subject == "All" and grade != "All":
            tutors = Tutor.query.filter_by(grade=grade).order_by(Tutor.average_stars).all()
        elif subject != "All" and grade == "All":
            tutors = Tutor.query.filter_by(subject=subject).order_by(Tutor.average_stars).all()
        else:
            tutors = Tutor.query.filter_by(subject=subject, grade=grade).order_by(Tutor.average_stars).all()

    tutors.reverse()
    return render_template('tutors.html', tutors=tutors, subjects=subjects, grades=grades, grade_selected=grade, subject_selected=subject, session=session, title="Tutors")

@app.route('/tutors/<id>', methods=['GET', 'POST'])
def tutorName(id):

    if not "user" in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form['title']
        review = request.form['review']
        starsSelected = 0

        if title.strip() == '' or review.strip() == '': flash('Please enter a title or description.', 'danger')

        for i in range(1, 7):
            if f'star-{i}' in request.form: starsSelected = i
        
        user = User.query.filter_by(email=session['user']).first()
        review = Review(tutor_id=id, title=title.strip(), username=user.username, rating=starsSelected, content=review.strip())

        tutor = Tutor.query.filter_by(id=id).first()
        tutor.average_stars = round((tutor.num_stars * tutor.average_stars + starsSelected) / (tutor.num_stars + 1))
        tutor.num_stars += 1

        db.session.add(review)
        db.session.commit()
    

    tutor = Tutor.query.filter_by(id=id).first()
    reviews = Review.query.filter_by(tutor_id=id).all()
    return render_template('specific_tutor.html', tutor=tutor, reviews=reviews, session=session, title=tutor.name)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if "user" in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form["email"]
        password = toHash(request.form["password"])

        if User.query.filter_by(email=email, password=password).first():
            # if username and password correct
            session["user"] = email
            flash('You are logged in!', 'success')
            return redirect(url_for('index'))

        else:
            flash('Incorrect email or password', 'danger')

    return render_template('login.html', session=session, title="Login")

@app.route('/register', methods=['GET', 'POST'])
def register():

    # if user already logged in redirect to home page
    if ("user" in session):
        return redirect(url_for('index'))

    # if registering
    if request.method == 'POST':
        req = request.form
        success = True

        # get data from form
        username = req.get("username").strip()
        email = req.get("email").strip()
        password = req.get("password")
        confirm_password = req.get("confirm-password")

        # if passwords don't match return error
        if password != confirm_password:
            success = False
            flash("Passwords Don't match. Please try again.", 'danger')

        # if equals nothing return error
        if not username:
            success = False
            flash("Please enter a username.", 'danger')
        if not email:
            success = False
            flash("Please enter an email.", 'danger') 
        if not password:
            success = False
            flash("Please enter a password.", 'danger')
        
        # if info isn't under required length return error
        if len(username) > 64:
            success = False
            flash('Username must be under 64 characters.', 'danger')
        if len(email) > 64:
            success = False
            flash('Email must be under 64 characters.', 'danger')
        if len(password) > 64:
            success = False
            flash('Password must be under 64 characters.', 'danger')

        # if type of data isn't string return error
        try:
            if not type(username) == str:
                success = False
                flash('Invalid username.', 'danger')
            if not type(email) == str:
                success = False
                flash('Invalid email.', 'danger') 
            if not type(password) == str or not type(confirm_password) == str:
                success = False
                flash('Invalid password.', 'danger')
        except:
            success = False
            flash('Invalid registration. Please try again.', 'danger')

        if User.query.filter_by(username=username).first():
            # Username already exists code here
            success = False
            flash('Username already exists. Please try with a different username.', 'danger')
        if User.query.filter_by(email=email).first():
            # Email already exists code here
            success = False
            flash('Email already exists. Please try with a different email.', 'danger')

        # if success then flash success message and take to login page
        if success:
            hashPass = toHash(password)

            user = User(username=username, password=hashPass, email=email)
            db.session.add(user)
            db.session.commit()

            flash('Your account has been created.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', session=session, title="Register")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    '''
    Logout page
    '''
    # if user not logged in send to login page
    if not "user" in session:
        return redirect(url_for('login'))

    # Remove data from session
    session.pop("user", None)
    # Redirect to homepage
    return redirect(url_for('index'))



if __name__ == '__main__':

    #app.run(debug=True, host='0.0.0.0') # use in testing, uncomment next line in production
    app.run(debug=False)
