
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, session, send_from_directory, jsonify, flash)
from werkzeug import secure_filename
app = Flask(__name__)
app = Flask(__name__, static_url_path="/static")

import sys,os,random
import dbconn2
import helperFunctions
import MySQLdb
import bcrypt
import imghdr

app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.config['SECRET_KEY'] = 'something very secret'



# Route for logging in
@app.route('/login/', methods=['GET', 'POST'])
def login():
    conn = dbconn2.connect(DSN)
    # check if there's a useridCookie in the browser already
    # useridCookie = request.cookies.get('useridCookie')
    if 'email' in session:
        return render_template('home/updateProfile.html')

    if request.method == "GET":
        return render_template('home/login.html')

    if request.method == "POST":
        # get userid and password from the form
        try:
            email=request.form['email']
            password= request.form['password']
            conn = dbconn2.connect(DSN)
            # userid=assignUID(conn)
            # returns true or false
            loginSuccess = helperFunctions.loginSuccess(conn, email, password)
            print loginSuccess
            # if login credentials are verified, tell user they've logged in
            # and set their userid as a cookie
            if loginSuccess == "success":
                flash("Login succeeded!")

                userid=helperFunctions.getUID(conn,email)

                #set sessions
                session['email']=email
                session['logged_in']=True
                session['visits'] = 1
                session['userid']=userid

                # resp = make_response(render_template('home/updateProfile.html',
                #                                      allCookies=request.cookies))
                # resp.set_cookie('useridCookie',value=email)
                return render_template('home/updateProfile.html',header=session.get('email'))
            # if login is unsuccessful because user provides wrong password
            # or no userid, prompt them to re-attempt to login
            else:
                flash("Email or password are incorrect. Please try again")
                return render_template('home/login.html')
        except Exception as err:
                print 'error is', type(err), err
                flash('Missing inputs')
                error = True
                return render_template('home/login.html')

@app.route('/logout/',methods=['GET'])
def logout():
    try:
        if 'email' in session:
            email = session['email']
            session.pop('email')
            session.pop('logged_in')
            session.pop('userid')
            flash('You are logged out')
            return redirect(url_for('login'))
        else:
            flash('you are not logged in. Please login or join')
            return redirect(url_for('login'))
    except Exception as err:
        flash('some kind of error '+str(err))
        return redirect(url_for('login'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    conn = dbconn2.connect(DSN)
    if request.method == "GET":
        return render_template('home/register.html',message="")
    # form = RegisterForm(request.form)
    if request.method == 'POST':
        usertype= request.form['usertype']
        firstName=request.form['firstName']
        lastName=request.form['lastName']
        email=request.form['myEmail']
        password=request.form['password']
        confirm_password=request.form["confirm_pass"]

        if usertype=="" or usertype=="None":
            flash("Please select Student or Mentor account")
            return render_template('home/register.html')

        if password!=confirm_password:
            flash("Passwords don't match. Please try again")
            return render_template('home/register.html')
        hashed=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


        exists = helperFunctions.findUser(conn,email)
        if (exists == True):
            flash("This email address is already associated with an account."+
            "Please sign in")
            return redirect(url_for('login'))
        else: # if email not already in use, register new user
            helperFunctions.registerUser(conn, usertype, firstName, lastName, email,hashed)
            return render_template('home/updateProfile.html')

@app.route('/browseJobs/')
def browseJobs():
    return render_template('home/browseJobs.html')

@app.route('/browseMentors/')
def browseMentors():
    return render_template('home/browseMentors.html')

@app.route('/viewProfile/',methods=['GET','POST'])
def viewProfile():
    if request.method == "GET":
        conn = dbconn2.connect(DSN)
        email= session.get('email')
        info=helperFunctions.viewProfile(conn,email)
        description=info['description']
        firstname=info['firstname']
        lastname=info['lastname']
        age=info['age']
        homeState=info['homeState']
        homeCountry=info['homeCountry']
        gender=info['gender']
        ethnicity=info['Ethnicity']
        filename='../../../images/'+info['picture']
        return render_template('home/viewProfile.html',firstname=firstname,
        lastname=lastname,description=description,age=age,gender=gender,
        race=ethnicity,country=homeCountry,state=homeState,profpic=filename)
    if request.method == 'POST':
        return redirect(url_for('profile'))


@app.route('/updateProfile/',methods=['GET', 'POST'])
def profile():
    conn = dbconn2.connect(DSN)
    if request.method == "GET":
        return render_template('home/updateProfile.html',header=session.get('email'),message="")
    # form = RegisterForm(request.form)
    if request.method == 'POST':

        description= request.form.get('description')
        age=request.form.get('age')
        gender=request.form.get('gender')
        race=request.form.get('race')
        country= request.form.get('country')
        state= request.form.get('state')
        email= session.get('email')
        profpic= request.files.get('profpic')

        print profpic


        mime_type = imghdr.what(profpic.stream)
        if mime_type != 'jpeg' and mime_type != 'png':
            raise Exception('Not a JPEG or a PNG')
        email=email.strip(".")
        filename = secure_filename('{}.{}'.format(email,mime_type))
        pathname = 'images/'+filename
        profpic.save(pathname)
        flash('Upload successful')

        #description= request.form['description']
        #profpic= request.files['profpic']
        # age=request.form['age']
        # gender=request.form['gender']
        # race=request.form['race']
        # country= request.form ['country']
        # state= request.form ['state']
        # email= session.get('email')


        helperFunctions.updateProfile(conn,email,description,age,gender,race,country,state,filename)
        return render_template('home/updateProfile.html',header="",message="successfully updated profile")

@app.route('/addJob/',methods=['GET','POST'])
def addJob():
    conn = dbconn2.connect(DSN)
    if request.method == 'GET':
        return render_template('home/addJob.html',message="")
    if request.method == 'POST':
        title= request.form.get('title')
        company= request.form.get('company')
        description= request.form.get('description')
        jobtype=request.form.get('type')
        priorexperience= request.form.get('priorexperience')
        tags=request.form.get('tags')
        favorite=request.form.get('favorite')
        leastfav= request.form.get('leastfav')
        tasks= request.form.get('tasks')
        daily=request.form.get('daily')
        skills=request.form.get('skills')
        advice=request.form.get('advice')
        salary=request.form.get('salary')
        startdate=request.form.get('startdate')
        enddate=request.form.get('enddate')

        userid=session.get('userid')


        mymessage=helperFunctions.addJob(conn,userid,title,company,description,jobtype,
        priorexperience,tags,favorite,leastfav,tasks,daily,skills,advice,
        salary,startdate,enddate)

        return render_template('home/addJob.html',header="",message=mymessage)


@app.route('/addEducation/',methods=['GET','POST'])
def addEducation():
    conn = dbconn2.connect(DSN)
    if request.method == 'GET':
        return render_template('home/addEducation.html')
    if request.method == 'POST':
        institution=request.form.get('institution')
        major=request.form.get('major')
        secondmajor=request.form.get('secondmajor')
        degreetype=request.form.get('degreetype')
        rating=request.form.get('rating')
        review=request.form.get('review')
        country=request.form.get('country')
        state=request.form.get('state')

        userid=session.get('userid')

        mymessage=helperFunctions.addEducation(conn,userid,institution,major,
        secondmajor,degreetype,rating,review,country,state)

        return render_template('home/addEducation.html',message=mymessage)

@app.route('/addProfession/')
def addProfession():
    return render_template('home/addProfession.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = dbconn2.connect(DSN)
    userid = request.cookies.get('useridCookie')
    if not userid:
        print 'no userid'
        return redirect(url_for('login'))
    else:
        return render_template('home/updateProfile.html')
    # return redirect(url_for('login'))
    # return render_template('home/login.html')

# use the main function to connect the webpage to the database
if __name__ == '__main__':

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()

    DSN = dbconn2.read_cnf()
    DSN['db'] = 'idalessa_db'
    app.debug = True
    # app.run()
    app.run('cs.wellesley.edu',port)
