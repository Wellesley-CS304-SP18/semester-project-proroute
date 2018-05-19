#ProRoute
#Isabel and Jess

from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, session, send_from_directory, jsonify, flash)
from werkzeug import secure_filename
app = Flask(__name__)
app = Flask(__name__, static_url_path="/static")

import sys,os,random,datetime
import dbconn2
import helperFunctions
import myhelperfunctions
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
    # conn = dbconn2.connect(DSN)

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

    if request.method == "GET":
        return render_template('home/register.html',message="")

    if request.method == 'POST':
        conn = dbconn2.connect(DSN)
        #get information from registration form
        usertype= request.form['usertype']
        firstName=request.form['firstName']
        lastName=request.form['lastName']
        email=request.form['myEmail']
        password=request.form['password']
        confirm_password=request.form["confirm_pass"]
        picture='dummy_user.png'

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
            helperFunctions.registerUser(conn, usertype, firstName, lastName, email,hashed,picture)

            userid=helperFunctions.getUID(conn,email)

            #set sessions for email,loggedin, visits, and userid
            session['email']=email
            session['logged_in']=True
            session['userid']=userid

            return redirect(url_for('viewProfile'))


@app.route('/browseJobs/',methods=['GET','POST'])
def browseJobs():
    """Allows users to browse jobs submitted by mentors and filter these
    jobs according to specific fields """
    conn = dbconn2.connect(DSN)
    if request.method == "GET":
        userid=session.get('userid')
        if not userid:
            return redirect(url_for('login'))

        #view job listings
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
        userid=session.get('userid')
        if not userid:
            return redirect(url_for('login'))
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
        #don't allow user to select a state if they choose a non-US country
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
        email= session.get('email')
        userid=session.get('userid')
        if email==None:
            return redirect(url_for('login'))
        else:
            conn = dbconn2.connect(DSN)

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

@app.route('/updateProfile/',methods=['GET','POST'])
def profile():
    """allows user to update basic profile information and inputs
    this information into the user databse"""
    conn = dbconn2.connect(DSN)
    if request.method == "GET":
        email= session.get('email')
        userid=session.get('userid')

        #check if user is signed in
        if not userid:
            return redirect(url_for('login'))
        info=helperFunctions.viewProfile(conn,email)

        #set default picture if none is provided
        filename=info['picture']
        if filename==None:
            filename='dummy_user.png'

        return render_template('home/updateProfile.html',header=session.get('email'),message="",
        info=info,filename=filename)

    if request.method == 'POST':

        #get intputs from the form
        email= session.get('email')
        info=helperFunctions.viewProfile(conn,email)

        """if blank/Null inputs are provided on the form, but these
        parameters were previously supplied by the user, these
        values are taken from the database and used to update
        the user's profile """
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
            filename = secure_filename('{}.{}'.format(email,mime_type))
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
    """allows user to update edit one of their education entries. This
    information is updated in the education table"""

    conn = dbconn2.connect(DSN)
    if request.method=='GET':
        userid=session.get('userid')

        #make sure user is logged in
        if not userid:
            return redirect(url_for('login'))

        #check to make sure the user has permission to edit this education
        #entry (it is one of their own )
        if helperFunctions.checkEducationPermissions(conn,eduid,userid)==True:

            #get education entry from the education table
            eduinfo=helperFunctions.viewEduInfo(conn,eduid)
            return render_template('home/editEducation.html',eduinfo=eduinfo)
        else:
            flash('You do not have permission to edit this entry')
            return redirect(url_for('viewProfile'))

    if request.method=='POST':
        #get education entry from the education table
        eduinfo=helperFunctions.viewEduInfo(conn,eduid)

        """Get new information from the editEducation form.
        If fields are left blank but this information was
        previously provided for the education entry,
        these values are taken from the database and used
        to update the entry
        """
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

        #update information in the education table
        helperFunctions.editEducation(conn,institution,state,country,major,
                                    secondmajor,degreetype,rating,review,eduid)

        return redirect(url_for('viewProfile'))

@app.route('/viewMentorProfile/<userid>',methods=['GET'])
def viewMentorProfile(userid):
    """Allows user to view the full profile of a mentor (accessed
    through the browseMentors page). This information includes
    basic profile information, jobs, and education (similar to the
    user's own viewProfile page but without edit/delete options)"""

    conn = dbconn2.connect(DSN)
    if request.method=='GET':

        #make sure the user is logged in
        personaluserid=session.get('userid')
        if not personaluserid:
            return redirect(url_for('login'))
        try:
            #get basic mentor information from the user table
            curs = conn.cursor(MySQLdb.cursors.DictCursor)
            curs.execute("select * from user join mentor using(userid) where "+
            "userid =%s;",[userid])
            mentorinfo=curs.fetchone()

            #get mentor's job information from the job table
            jobinfo=helperFunctions.viewJobs(conn,userid)

            #get mentor's education information from the education table
            eduinfo= helperFunctions.viewEducation(conn,userid)

            #display all of this information
            return render_template('home/viewMentorProfile.html',mentorinfo=mentorinfo,
            jobs=jobinfo,education=eduinfo)
        except MySQLdb.IntegrityError as err:
            return "Error"
    else:
        return redirect(url_for('browseMentors'))


@app.route('/viewJobPosting/<jobid>',methods=['GET'])
def viewJobPosting(jobid):
    """Allows user to view a job entry (accessed
    through the browseJobs page)."""
    conn = dbconn2.connect(DSN)

    if request.method=='GET':
        #make sure user is logged in
        userid=session.get('userid')
        if not userid:
            return redirect(url_for('login'))
        try:
            curs = conn.cursor(MySQLdb.cursors.DictCursor)

            #get job information from the job database
            jobinfo=helperFunctions.viewJobInfo(conn,jobid)

            #display this information
            return render_template('home/viewJobPosting.html',job=jobinfo)
        except MySQLdb.IntegrityError as err:
            return "Error"
    else:
        return redirect(url_for('browseJobs'))

@app.route('/editJob/<jobid>',methods=['GET','POST'])
def editJob(jobid):
    """allows user to update/edit one of their job entries. This
    information is updated in the job table"""
    conn = dbconn2.connect(DSN)
    if request.method=='GET':

        #make sure user is logged in
        userid=session.get('userid')
        if not userid:
            return redirect(url_for('login'))

        #make sure user has permission to edit this job (it is one of their own)
        if helperFunctions.checkJobPermissions(conn,jobid,userid)==True:

            #get job information from the job table
            jobinfo=helperFunctions.viewJobInfo(conn,jobid)

            #get job type (for rendering pre-selected the radio buttons )
            jobtypes=['full time','part time']
            selected=jobinfo['type']
            return render_template('home/editJob.html',jobinfo=jobinfo,jobtypes=jobtypes,selected=selected)

        else:
            flash('You do not have permission to edit this job')
            return redirect(url_for('viewProfile'))

    if request.method=='POST':
        #get job information from the job table
        jobinfo=helperFunctions.viewJobInfo(conn,jobid)

        """Get new information from the editJob form.
        If fields are left blank but this information was
        previously provided for the job entry,
        these values are taken from the database and used
        to update the entry
        """

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
            #format date appropriately for storage in database
            startdate=startdate +'-00'

        enddate=request.form.get('enddate')
        if enddate=='':
            #format date appropriately for storage in database
            enddate=jobinfo['endDate'] + '-00'

        education=request.form.get('educationExperience')
        if education=='':
            education=jobinfo['education']

        #edit job entry in the job table
        helperFunctions.editJob(conn,jobid,title,company,description,jobtype,
        priorexperience,tags,favorite,leastfav,tasks,daily,skills,advice,
        salary,startdate,enddate,education)

        return redirect(url_for('viewProfile'))

@app.route('/addJob/',methods=['GET','POST'])
def addJob():
    """Allows user to add a job to their profile. Reads information
    input with the addJob.html form and inserts it into the
    job database"""

    if request.method == 'GET':
        userid=session.get('userid')
        if not userid:
            return redirect(url_for('login'))
        return render_template('home/addJob.html',message="")
    if request.method == 'POST':
        conn = dbconn2.connect(DSN)
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
        userid=session.get('userid')
        if not userid:
            return redirect(url_for('login'))
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


@app.route('/', methods=['GET', 'POST'])
def index():
    """Main page. Reroutes to the login page if no session is set.
    If a session is set, reroutes to the view profile page """
    userid=session.get('userid')
    if not userid:
        print 'no userid'
        return redirect(url_for('login'))
    else:
        return redirect(url_for('profile'))

@app.route('/forum/',methods = ['GET', 'POST'])
def forum():
    return render_template('home/forum.html', header = "Forum")

@app.route('/getQuestion/', methods = ['GET','POST'])
def getQuestion():
    print "getting to the getQuestion"
    try:
        connect = dbconn2.connect(DSN)
        if request.method == 'POST':
            print 'handling POST QUestion'
            userid=session['userid']


            quest = request.form.get('question')
            tags=request.form.get('tags')
            user = myhelperfunctions.getUID(connect, session['email'])
            date = datetime.datetime.now()

            if quest is not None :
                if helperFunctions.isStudent(connect,userid):
                    myhelperfunctions.add_question(connect, user, quest, tags, date)

        result = myhelperfunctions.show_questions(connect)

        print "end of GET_QUESTION"
        return jsonify(result)
    except Exception as err:
        return jsonify( [{'error': True, 'err': str(err) } ])

@app.route('/answer/<quest_identifier>',methods = ['GET', 'POST']) #<quest_id>
def answer(quest_identifier):
    #return quest_identifier + "THIS IS QUESTID for answer"
    #print str(request.args.get('quest_identifier')) + ("WOULD APPEAR HER FOR ANSWER!!!!!!")
    try:
        connect = dbconn2.connect(DSN)
        quid= myhelperfunctions.get_question(connect,str(quest_identifier))
        #return quest_identifier + "THIS IS QUESTID for answer"
        return render_template('home/answer.html', header = quid['questionText'] )#"Question ID: "+ quid['questionID']+quid['questionText'])
    except Exception as err:
        return err

@app.route('/getAnswer/<qid>', methods = ['GET','POST'])
def getAnswer(qid):
    print "getting to the getAnswer"
    try:
        connect = dbconn2.connect(DSN)
        if request.method == 'POST':
            print 'handling POST Answer'
            user = myhelperfunctions.getUID(connect, session['email'])
            print qid
            ans = request.form.get('answer')
            date = datetime.datetime.now()
            #print quest
            #print user
            #print date
            print 'answer'
            print ans
            if ans is not None :
                myhelperfunctions.add_answer(connect,user,qid, ans, date)
                print ans +"its not empty"

                print "this is where answer get would show up"

        result = myhelperfunctions.show_answers(connect, qid)

        print jsonify(result)

        return jsonify(result)
    except Exception as err:
        return jsonify( [{'error': True, 'err': str(err) } ])

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
