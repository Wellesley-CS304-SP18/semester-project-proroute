
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, session, send_from_directory, jsonify, flash)

app = Flask(__name__)
app = Flask(__name__, static_url_path="/static")

import sys,os,random
import dbconn2
import helperFunctions
import MySQLdb

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

                #set sessions
                session['email']=email
                session['logged_in']=True

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
                print 'error is', typer(err), err
                flash('Missing inputs')
                error = True

@app.route('/logout/',methods=['GET'])
def logout():
    session.clear()
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
        if password!=confirm_password:
            flash("Passwords don't match. Please try again")
            return render_template('home/register.html')
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("SELECT * from user where email=%s;",[email])
        existing_email = curs.fetchone()
        if (existing_email != None):
            flash("This email address is already associated with an account."+
            "Please sign in")
            return render_template('home/register.html')
        else:
            curs.execute("insert into user (firstname,lastname,email,password)"+
            "values (%s, %s, %s,%s);", (firstName, lastName, email,password))


        print usertype;
        return render_template('home/updateProfile.html')

@app.route('/browseJobs/')
def browseJobs():
    return render_template('home/browseJobs.html')

@app.route('/browseMentors/')
def browseMentors():
    return render_template('home/browseMentors.html')

@app.route('/updateProfile/')
def profile():
    return render_template('home/updateProfile.html')

@app.route('/addJob/')
def addJob():
    return render_template('home/addJob.html')

@app.route('/addEducation/')
def addEducation():
    return render_template('home/addEducation.html')

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
