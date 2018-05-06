from flask import (Flask, render_template, flash, request, redirect, url_for, session)
#import temp
import os
import dbconn2
app= Flask(__name__)

app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.config['SECRET_KEY'] = "abcde"

DATABASE = 'jaguilar2_db' #this needs to be replaced with team database


#the inital page once at the website
@app.route('/', methods= ['GET','POST'])
def login():
    if request.method == "POST":

            #siging in without a database backing
        if 'email' not in session :
            session['email'] = request.form['l_email']
            email = session['email']
            print request.form['l_email']
            session['password'] = request.form['l_password']
            password = session['password']
            session['logged_in'] = True

        #redirect to the profile page that will be shown after logging in
        return render_template('profile.html', header = "Profile",email= session.get('email'))

    return render_template('login.html',  header ="Log In")



@app.route('/SignUp', methods = ['GET', 'POST'])
def signup():
    try:
        if request.method == 'POST':
            error = False
            user_firstName = ''
            user_lastName = ''
            user_userName = ''
            user_email = ''
            user_password = ''
            user_age = ''
            user_gender = ''
            #user_homeState = ''
            #user_homeCountry = ''
            #user_ethnicity = ''

            try:
                user_firstName = request.form['']
                user_lastName = request.form['']
                user_userName = request.form['']
                user_email = request.form['']

                #we will need to generate the user id on our end
                #however we might want to change this as we might use the user_email
                #as a primary key? as Scott suggested
                #user_userId= ''
                #user_password = request.form['']
                user_age = request.form['']
                user_gender = request.form['']
                #user_homeState = request.form['']
                #user_homeCountry = request.form['']
                #user_ethnicity = request.form['']
            except Exception as err:
                print 'error is', typer(err), err
                flash('Missing inputs')
                error = TRUE
    except Exception as err:
        print 'Unknown exception',error
        return '<p>failed due to an unknown error</p>'
    return ''
                #would need to add the rest of the error flash messages

#profile page that would appear once user is logged in
@app.route('/profile',methods = ['GET', 'POST'])
def profile():
    return render_template('/profile.html', header = "Profile", email = session['email'])

@app.route('/logout',methods = ['GET', 'POST'])
def logout():
    # removes the email/password/logged_in from the session logging out. No path yet
    session.clear() # What is the difference between clear and pop?
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', os.getuid())
