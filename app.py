'''
------------------------------

Tutor Center

Authors: Jason, Evan, Raghav, Amogh

------------------------------
'''



from flask import Flask, render_template, url_for, request, redirect, session, flash
import hashlib
import os
import random
import json
import requests
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

cluster = MongoClient("mongodb+srv://evan:ueWoDdHKcZ5E0Ln1@cluster0.cwhuk86.mongodb.net/?retryWrites=true&w=majority")
db = cluster["tutor-centre"]
users = db["users"]
tutors_db = db["tutors"]
reviews = db["reviews"]

# MongoDB
# USername: evan
# Password: ueWoDdHKcZ5E0Ln1
# mongodb+srv://evan:<password>@cluster0.cwhuk86.mongodb.net/?retryWrites=true&w=majority

'''
App config
------------------------------
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

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
    tutor = {"name": name, "email": f"{name.lower()}@fake_email.com", "phone_number": str(random.randint(1000000000, 9999999999)), "pay": random.randint(20, 40), "description": desc, "subject": subjects[random.randint(1, len(subjects)-1)], "grade": grades[random.randint(1, len(grades)-1)], "average_stars": 0, "image": imageURL, "num_stars": 0}
    tutors_db.insert_one(tutor)

@app.route('/index.html')
@app.route('/')
def index():
    return render_template('index.html', session=session, title="Home")

# @app.route('/start-up')
# def start_up():
#     return render_template('start-up.html')

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
            tutor = {
                "name": name,
                "email": email,
                "phone_number": phone_number,
                "pay": pay,
                "description": description,
                "subject": subject,
                "grade": grade,
                "average_stars": average_stars,
                "image": image,
                "num_stars": num_stars
            }

            tutors_db.insert_one(tutor)

            flash(f'You have now become a tutor! Go to grade {grade} {subject} to see yourself!', 'success')
            return redirect(url_for('tutors'))

    return render_template('create_tutor.html', title='Become Tutor', session=session)

@app.route('/tutors', methods=['GET', 'POST'])
def tutors():

    if not "user" in session:
        return redirect(url_for('index'))

    subject, grade = "All", "All"
    tutors_list = tutors_db.find().sort("average_stars", -1)

    if request.method == 'POST':
        subject = request.form["subject"]
        grade = request.form["grade"]

        if subject == "All" and grade == "All":
            tutors_list = tutors_db.find().sort("average_stars", -1)
        elif subject == "All" and grade != "All":
            tutors_list = tutors_db.find({"grade": grade}).sort("average_stars", -1)
        elif subject != "All" and grade == "All":
            tutors_list = tutors_db.find({"subject": subject}).sort("average_stars", -1)
        else:
            tutors_list = tutors_db.find({"subject": subject, "grade": grade}).sort("average_stars", -1)

    return render_template('tutors.html', tutors=tutors_list, subjects=subjects, grades=grades, grade_selected=grade, subject_selected=subject, session=session, title="Tutors")

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
        
        user = users.find_one({"email": session['user']})
        review = {
            "tutor_id": id,
            "title": title.strip(),
            "username": user['username'],
            "rating": starsSelected,
            "content": review.strip()
        }

        newObjectId = ObjectId(id)

        tutor = tutors_db.find_one(newObjectId)
        new_average_stars = round((tutor['num_stars'] * tutor['average_stars'] + starsSelected) / (tutor['num_stars'] + 1))
        new_num_stars = tutor['num_stars'] + 1

        tutors_db.find_one_and_update(
            {'_id': newObjectId}, 
            {
                '$set': {
                    'average_stars': new_average_stars,
                    'num_stars': new_num_stars
                }
            }
        )

        reviews.insert_one(review)
    
    newObjectId = ObjectId(id)
    tutor = tutors_db.find_one(newObjectId)

    if reviews.find_one({"tutor_id": id}):
        reviews_exist = True 
    else:
        reviews_exist = False
    reviews_list = reviews.find({"tutor_id": id})
    if not reviews_exist:
        reviews_list = None

    print(tutor['average_stars'])
    
    return render_template('specific_tutor.html', tutor=tutor, reviews=reviews_list, session=session, title=tutor['name'])

@app.route('/login', methods=['GET', 'POST'])
def login():

    if "user" in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form["email"]
        password = toHash(request.form["password"])

        if users.find_one({"email": email, "password": password}):
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

        if users.find_one({"username": username}):
            # Username already exists code here
            success = False
            flash('Username already exists. Please try with a different username.', 'danger')
        if users.find_one({"email": email}):
            # Email already exists code here
            success = False
            flash('Email already exists. Please try with a different email.', 'danger')

        # if success then flash success message and take to login page
        if success:
            hashPass = toHash(password)

            user = {
                "username": username, 
                "password": hashPass, 
                "email": email
            }

            users.insert_one(user)

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

    app.run(debug=True, host='0.0.0.0') # use in testing, uncomment next line in production
    # app.run(debug=False)
