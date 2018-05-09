from flask import (Flask, render_template, flash, request, redirect, url_for, session)
import temp
import os
import dbconn2
import MySQLdb
app= Flask(__name__)

app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.config['SECRET_KEY'] = "abcde"

DSN = None
DATABASE = 'jaguilar2_db' #this needs to be replaced with team database


#the inital page once at the website
@app.route('/', methods= ['GET','POST'])
def login():
    conn = dbconn2.connect(DSN)

    #will enter form if the form is submitted
    if request.method == "POST":
        print 'making it to post'

        #get the entries from the fields
        l_email = request.form['l_email']
        print l_email
        l_password = request.form['l_password']
        print l_password


        #get in contact with file temp and make sure the email is in the database
        loginSuccess = temp.login_user(conn, l_email, l_password)
        print loginSuccess

        #once logged
        if loginSuccess == "success" :
            print 'getting to loging success'
            flash("Login succeeded")


            #SET THE SESSIONS
            session['email'] = l_email
            session['password'] = l_password
            session['logged_in'] = True

            #redirect user to profile page
            return render_template('profile.html', header = "Profile",email= l_email)
        else:
            flash("email or password is incorrect")

    #once the user is logged in (in session) they will no longer reach the login page
    #unless they sign out
    if 'email' in session:
        print 'in session'
        return render_template('profile.html', header = "Profile",email= session.get('email'))

    #return the template and flash message if login was Unsuccessful
    return render_template('login.html',  header = "Login")



@app.route('/register', methods = ['GET', 'POST'])
def signup():
    #try:
    conn = dbconn2.connect(DSN)
    if request.method == 'GET':
        return render_template('register.html', header = "Sign Up")

    if request.method == 'POST':
        user_account_type = request.form['s_account_type']
        print user_account_type
        user_firstName = request.form['s_firstName']
        print user_firstName
        user_lastName = request.form['s_lastName']
        print user_lastName
        user_email = request.form['s_email']
        print user_email
        user_password = request.form['s_password']
        print user_password
        user_confrim_pass = request.form['s_conf_password']#we're going to need to compare passwords
        print user_confrim_pass
        #try:
        '''
        this is where we will put the databse querie
        '''
        if temp.find_user(conn, user_email):
            temp.register_user(conn, user_account_type , user_firstName, user_lastName, user_email, user_password)
            session['email'] = user_email
            session['password'] = user_password
            session['logged_in'] = True
            return redirect(url_for('profile'))

        #except Exception as error:
        ##    print 'error is', typer(err), err
            #flash('Missing inputs')

    #except Exception as error:
        #print 'Unknown exception',error
        #return '<p>failed due to an unknown error</p>'
    return render_template('register.html', header = "Sign Up")
                #would need to add the rest of the error flash messages

#profile page that would appear once user is logged in
@app.route('/profile',methods = ['GET', 'POST'])
def profile():
    return render_template('/profile.html', header = "Profile", email = session['email'])

@app.route('/job', methods= ['GET','POST'])
def job():
    return render_template('/job.html', header = "JOB")

@app.route('/logout',methods = ['GET', 'POST'])
def logout():
    # removes the email/password/logged_in from the session logging out. No path yet
    session.clear() # What is the difference between clear and pop?
    return redirect(url_for('login'))


if __name__ == '__main__':
    DSN = dbconn2.read_cnf()
    DSN['db']= 'jaguilar2_db'
    app.debug = True
    app.run('0.0.0.0', os.getuid())
