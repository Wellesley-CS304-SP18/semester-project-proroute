from flask import Flask, render_template, flash, request, redirect, url_for, sessions
import temp
import os

app= Flask(__name__)
app.secret_key = "abcde"

DATABASE = 'jaguilar2_db' #this needs to be replaced with team database

#this is the front end template/file that would be rendered
@app.route('/ProRoute/home')
    def home():
        return render_template('')

@app.route('/ProRoute/LogIn')
    def login():
        return render_template('')

@app.route('/ProRoute/SignUp', methods = ['GET', 'POST'])
def signup():
    try:
        if request.method == 'POST':
            error = False
            user_firstName = ''
            user_lastName = ''
            user_userName = ''
            user_email = ''
            user_userId= ''
            user_password = ''
            user_age = ''
            user_gender = ''
            user_homeState = ''
            user_homeCountry = ''
            user_ethnicity = ''

            try:
                user_firstName = request.form['']
                user_lastName = request.form['']
                user_userName = request.form['']
                user_email = request.form['']

                #we will need to generate the user id on our end
                #however we might want to change this as we might use the user_email
                #as a primary key? as Scott suggested
                user_userId= ''
                user_password = request.form['']
                user_age = request.form['']
                user_gender = request.form['']
                user_homeState = request.form['']
                user_homeCountry = request.form['']
                user_ethnicity = request.form['']
            except Exception as err:
                print 'error is', typer(err), err
                flash('Missing inputs')
                error = True

                #would need to add the rest of the error flash messages

'''once signed up/logged they would be able to access the profile page
where they could see the current information and be redirected to another
page if they wanted to update or finish filling out their profile
'''
@app.route('/profile',method= ['GET', 'POST'])
def profile():
    return ''

@app.route('/logout',method= ['GET', 'POST'])
def logout():
    return ''

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', os.getuid())
