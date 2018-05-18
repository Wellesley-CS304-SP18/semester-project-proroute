#ProRoute
#Isabel and Jess

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
    """Allows user to login to their account. Checks user credentials
    against information in the user database"""
    conn = dbconn2.connect(DSN)

    #check if the user's email is already in the session
    #if this is the case, redirect to the user's profile
    if 'email' in session:
        return redirect(url_for('viewProfile'))

    if request.method == "GET":
        return render_template('home/login.html')

    if request.method == "POST":

        try:
            # get userid and password from the form
            email=request.form['email']
            password= request.form['password']
            conn = dbconn2.connect(DSN)

            #check in the database to see if login is correct
            loginSuccess = helperFunctions.loginSuccess(conn, email, password)

            # if login credentials are verified, tell user they've logged in
            if loginSuccess == "success":
                flash("Login succeeded!")

                #get the newly created user id from the database(auto-incremented)
                userid=helperFunctions.getUID(conn,email)

                #set sessions for email,loggedin, visits, and userid
                session['email']=email
                session['logged_in']=True
                session['visits'] = 1
                session['userid']=userid

                return redirect(url_for('viewProfile'))

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
    """Logs out the user by redirecting to the login page and clearing
    all the sessions"""
    try:
        #clear sessions
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
    """Allows user to register for an account using the register.html formself.
    Inputs this data into the user database """
    conn = dbconn2.connect(DSN)
    if request.method == "GET":
        return render_template('home/register.html',message="")

    if request.method == 'POST':
        #get information from registration form
        usertype= request.form['usertype']
        firstName=request.form['firstName']
        lastName=request.form['lastName']
        email=request.form['myEmail']
        password=request.form['password']
        confirm_password=request.form["confirm_pass"]

        #require users to select an account type
        if usertype=="" or usertype=="None":
            flash("Please select Student or Mentor account")
            return render_template('home/register.html')

        #check to see if passwords match
        if password!=confirm_password:
            flash("Passwords don't match. Please try again")
            return render_template('home/register.html')

        #encode password add it to the user table of the database
        hashed=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        #check to see if a user already exists with this email. If so,
        #flash an error message and redirect to the login page
        exists = helperFunctions.findUser(conn,email)
        if (exists == True):
            flash("This email address is already associated with an account."+
            "Please sign in")
            return redirect(url_for('login'))
        else: # if email not already in use, register new user
            helperFunctions.registerUser(conn, usertype, firstName, lastName, email,hashed)

            userid=helperFunctions.getUID(conn,email)

            #set sessions for email,loggedin, visits, and userid
            session['email']=email
            session['logged_in']=True
            session['visits'] = 1
            session['userid']=userid

            return redirect(url_for('viewProfile'))


@app.route('/browseJobs/',methods=['GET','POST'])
def browseJobs():
    """Allows users to browse jobs submitted by mentors and filter these
    jobs according to specific fields """
    conn = dbconn2.connect(DSN)
    if request.method == "GET":
        jobinfo=helperFunctions.browseJobs(conn)
        return render_template('home/browseJobs.html',jobs=jobinfo)


    if request.method == 'POST':

        #get optional filter parameters from form
        searchform=request.form.get('searchform')
        jobtype=request.form.get('jobtype')
        tasks=request.form.get('tasks')
        minsalary=request.form.get('minsalary')
        workExperience= request.form.getlist('workExperience')
        educationExperience=request.form.getlist('educationExperience')


        #filter jobs shown on the page according to the filter paramaters
        jobinfo=helperFunctions.filterJobs(conn,searchform,jobtype,tasks,
        minsalary,workExperience,educationExperience)
        return render_template('home/browseJobs.html',jobs=jobinfo)

@app.route('/browseMentors/',methods=['GET','POST'])
def browseMentors():
    """Allows users to browse the profiles of mentors, and filter the
    results shown according to specific parameters  """

    conn = dbconn2.connect(DSN)
    if request.method == "GET":
        #fetch mentor profile info from the databse
        mentorinfo=helperFunctions.viewMentors(conn)
        return render_template('home/browseMentors.html',mentors=mentorinfo)

    #filter parameters
    if request.method == 'POST':

        #gather filter parameters from the form
        searchform=request.form.get('searchform')
        profession_search= request.form.get('profession_search')
        minage= request.form.get('minage')
        maxage= request.form.get('maxage')
        gender=request.form.getlist('gender')
        country= request.form.get('country')
        state=request.form.get('state')
        if country!=None and country!='US':
            state=None


        #filter mentor profiles displayed on the page according to filter parameters
        mentorinfo=helperFunctions.filterMentors(conn,searchform,profession_search,minage,maxage,
        gender,country,state)
        return render_template('home/browseMentors.html',mentors=mentorinfo)

@app.route('/viewProfile/',methods=['GET','POST'])
def viewProfile():
    """Allows user to view their profile, including information in the user
    database, jobs, and educational steps entered into their profile.
    Also allows users to add/delete jobs and educational steps """


    if request.method == "GET":
        conn = dbconn2.connect(DSN)
        email= session.get('email')
        userid=session.get('userid')

        #view other profile details associated with the given email and uerid
        info=helperFunctions.viewProfile(conn,email)

        description=info['description']
        firstname=info['firstname']
        lastname=info['lastname']
        age=info['age']
        homeState=info['homeState']
        homeCountry=info['homeCountry']
        gender=info['gender']
        ethnicity=info['Ethnicity']
        filename=info['picture']

        #default photo to display if one is not uploaded
        if filename==None:
            print 'ITS NONE'
            filename='dummy_user.png'

        #fetch jobs submitted by the user from the jobs database,
        #nad display them on the user profile
        jobinfo=helperFunctions.viewJobs(conn,userid)

        #fetch education information submitted by the user from the
        #education database, and display them on the user profile
        eduinfo= helperFunctions.viewEducation(conn,userid)

        #add new information to the user's profile
        return render_template('home/viewProfile.html',firstname=firstname,
        lastname=lastname,description=description,age=age,gender=gender,
        race=ethnicity,country=homeCountry,state=homeState,profpic=filename,
        jobs=jobinfo,education=eduinfo)

    if request.method == 'POST':
        return redirect(url_for('profile'))

@app.route('/pic/<fname>')
def pic(fname):
    """Method to display a profile picture uploaded by the user on their
    profile page"""
    f = secure_filename(fname)
    val = send_from_directory('images',f)
    print val, type(val)
    return val



@app.route('/deleteJob/', methods=['POST'])
def delete_job():
    """Allows user to delete job by clicking a button on their profile page
    Deletes the appropriate job from the jobs database"""
    conn = dbconn2.connect(DSN)
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    userid=session.get('userid')
    jobid=request.form['job_to_delete']
    curs.execute("delete from job where userid=%s and jobID=%s;",[userid,jobid])
    return redirect(url_for('viewProfile'))

@app.route('/deleteEdu/', methods=['POST'])
def delete_education():
    """Allows user to delete an education entry by clicking a button on their
    profile page. Deletes the appropriate education entry from the
    education database"""
    conn = dbconn2.connect(DSN)
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    userid=session.get('userid')
    eduid=request.form['edu_to_delete']
    curs.execute("delete from education where userid=%s and eduID=%s;",[userid,eduid])
    return redirect(url_for('viewProfile'))

@app.route('/updateProfile/',methods=['GET', 'POST'])
def profile():
    """allows user to update basic profile information and inputs
    this information into the user databse"""
    conn = dbconn2.connect(DSN)
    if request.method == "GET":
        email= session.get('email')
        userid=session.get('userid')
        info=helperFunctions.viewProfile(conn,email)

        filename=info['picture']
        if filename==None:
            filename='dummy_user.png'

        return render_template('home/updateProfile.html',header=session.get('email'),message="",
        info=info,filename=filename)

    if request.method == 'POST':

        #get intputs from the form
        email= session.get('email')
        info=helperFunctions.viewProfile(conn,email)

        description= request.form.get('description')
        if description=='':
            description=info['description']
        age=request.form.get('age')
        if age=='':
            age= info['age']
        gender=request.form.get('gender')
        if gender==None:
            gender=info['gender']
        race=request.form.get('race')
        if race=='':
            race=info['Ethnicity']
        country= request.form.get('country')
        if country==None:
            country=info['homeCountry']
        state= request.form.get('state')
        if state==None:
            state=info['homeState']
        if country!=None and country!='US':
            state=None
        email= session.get('email')
        profpic= request.files.get('profpic')

        #store profile picture in filesystem
        try:
            mime_type = imghdr.what(profpic.stream)
            if mime_type != 'jpeg' and mime_type != 'png' and mime_type!="JPG":
                raise Exception(' ')
            newemail=email.strip(".")
            filename = secure_filename('{}.{}'.format(newemail,mime_type))
            pathname= "images/"+filename
            profpic.save(pathname)

        except Exception as err:
            filename=None
            print ('Upload failed {why}'.format(why=err))

        if filename==None:
            filename=info['picture']


        #update the database with new information
        helperFunctions.updateProfile(conn,email,description,age,gender,race,country,state,filename)
        return redirect(url_for('viewProfile'))

@app.route('/editEducation/<eduid>',methods=['GET','POST'])
def editEducation(eduid):
    conn = dbconn2.connect(DSN)
    if request.method=='GET':
        userid=session.get('userid')
        if helperFunctions.checkEducationPermissions(conn,eduid,userid)==True:

            eduinfo=helperFunctions.viewEduInfo(conn,eduid)
            return render_template('home/editEducation.html',eduinfo=eduinfo)
        else:
            flash('You do not have permission to edit this entry')
            return redirect(url_for('viewProfile'))
    if request.method=='POST':
        eduinfo=helperFunctions.viewEduInfo(conn,eduid)

        institution= request.form.get('institution')
        if institution=='':
            title=eduinfo['institution']

        major=request.form.get('major')
        if major=='':
            major=eduinfo['major']

        secondmajor=request.form.get('secondmajor')
        if secondmajor=='':
            secondmajor=eduinfo['major2']

        degreetype=request.form.get('degreetype')
        if degreetype==None:
            degreetype=eduinfo['degreetype']

        rating=request.form.get('rating')
        if rating==None:
            rating=eduinfo['overallRating']

        review=request.form.get('review')
        if review==None:
            review=eduinfo['review']

        country=request.form.get('country')
        if country==None:
            country=eduinfo['instCountry']

        state=request.form.get('state')
        if state==None:
            state=eduinfo['instState']
        if country!=None and country!='US':
            state=None

        helperFunctions.editEducation(conn,institution,state,country,major,
                                    secondmajor,degreetype,rating,review,eduid)

        return redirect(url_for('viewProfile'))

@app.route('/editJob/<jobid>',methods=['GET','POST'])
def editJob(jobid):
    conn = dbconn2.connect(DSN)
    if request.method=='GET':

        userid=session.get('userid')
        if helperFunctions.checkJobPermissions(conn,jobid,userid)==True:

            jobinfo=helperFunctions.viewJobInfo(conn,jobid)



            print 'my startdate'
            print jobinfo['startDate']
            print 'jobid'
            print jobinfo['jobID']
            jobtypes=['full time','part time']
            selected=jobinfo['type']
            return render_template('home/editJob.html',jobinfo=jobinfo,jobtypes=jobtypes,selected=selected)

        else:
            flash('You do not have permission to edit this job')
            return redirect(url_for('viewProfile'))

    if request.method=='POST':
        jobinfo=helperFunctions.viewJobInfo(conn,jobid)

        title= request.form.get('title')
        if title=='':
            title=jobinfo['title']

        company= request.form.get('company')
        if company=='':
            company=jobinfo['company']

        description= request.form.get('description')
        if description=='':
            description=jobinfo['description']

        jobtype=request.form.get('type')
        if jobtype==None:
            jobtype=jobinfo['type']

        priorexperience= request.form.get('priorexperience')
        if priorexperience=='':
            priorexperience=jobinfo['experience']

        tags=request.form.get('tags')
        if tags=='':
            tags=jobinfo['professionTag']

        favorite=request.form.get('favorite')
        if favorite=='':
            favorite=jobinfo['favoritePart']

        leastfav=request.form.get('leastfav')
        if leastfav=='':
            leastfav=jobinfo['leastFavoritePart']

        tasks= request.form.get('tasks')
        if tasks=='':
            tasks=jobinfo['task']

        daily=request.form.get('daily')
        if daily=='':
            daily=jobinfo['dailylife']

        skills=request.form.get('skills')
        if skills=='':
            skills=jobinfo['skill']

        advice=request.form.get('advice')
        if advice=='':
            advice=jobinfo['advice']

        salary=request.form.get('salary')
        if salary=='':
            salary=jobinfo['annualSalary']

        startdate=request.form.get('startdate')
        if startdate=='':
            startdate=jobinfo['startDate']
        else:
            startdate=startdate+'-00'

        enddate=request.form.get('enddate')
        if enddate=='':
            enddate=jobinfo['endDate']

        education=request.form.get('educationExperience')
        if education=='':
            education=jobinfo['education']

        helperFunctions.editJob(conn,jobid,title,company,description,jobtype,
        priorexperience,tags,favorite,leastfav,tasks,daily,skills,advice,
        salary,startdate,enddate,education)

        return redirect(url_for('viewProfile'))

@app.route('/addJob/',methods=['GET','POST'])
def addJob():
    """Allows user to add a job to their profile. Reads information
    input with the addJob.html form and inserts it into the
    job database"""
    conn = dbconn2.connect(DSN)
    if request.method == 'GET':
        return render_template('home/addJob.html',message="")
    if request.method == 'POST':

        #get information from html form
        title= request.form.get('title')
        company= request.form.get('company')
        description= request.form.get('description')
        jobtype=request.form.get('type')
        priorexperience= request.form.get('priorexperience')
        educationExperience=request.form.get('educationExperience')
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

        #add job to the jobs table of the database
        mymessage=helperFunctions.addJob(conn,userid,title,company,description,jobtype,
        priorexperience,tags,favorite,leastfav,tasks,daily,skills,advice,
        salary,startdate,enddate,educationExperience)

        return render_template('home/addJob.html',header="",message=mymessage)


@app.route('/addEducation/',methods=['GET','POST'])
def addEducation():
    """Allows user to add an education entry to their profile. Reads information
    input with the addEducation.html form and inserts it into the
    job database"""

    conn = dbconn2.connect(DSN)
    if request.method == 'GET':
        return render_template('home/addEducation.html')
    if request.method == 'POST':

        #get data from form
        institution=request.form.get('institution')
        major=request.form.get('major')
        secondmajor=request.form.get('secondmajor')
        degreetype=request.form.get('degreetype')
        rating=request.form.get('rating')
        review=request.form.get('review')
        country=request.form.get('country')
        state=request.form.get('state')
        if country!=None and country!='US':
            state=None

        userid=session.get('userid')

        #add education to the education database, associated with user via
        #userid
        mymessage=helperFunctions.addEducation(conn,userid,institution,major,
        secondmajor,degreetype,rating,review,country,state)

        return render_template('home/addEducation.html',message=mymessage)

@app.route('/addProfession/')
def addProfession():
    """Allows user to add profession ratings to a profession and updates
    this information in the professions table"""
    return render_template('home/addProfession.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main page. Reroutes to the login page if no session is set.
    If a session is set, reroutes to the view profile page """
    conn = dbconn2.connect(DSN)
    userid=session.get('userid')
    if not userid:
        print 'no userid'
        return redirect(url_for('login'))
    else:
        return redirect(url_for('profile'))


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
