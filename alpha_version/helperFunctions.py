# CS 304 Homework 7
# April 12, 2018
# Authors: Katy Ma and Isabel D'Alessandro

import sys
import MySQLdb
import dbconn2
import bcrypt
import imghdr
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, session, send_from_directory, jsonify, flash)

temporaryPassword = '123'


def findUser(conn, email):
    """checks if a user with the given email already exists in the
    user table. If such a user does exist, returns True, otherwise
    returns False """
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)

        curs.execute("SELECT * from user where email=%s;",[email])
        existing_email = curs.fetchone()
        if (existing_email != None):
            return True
        else:
            return False
    except MySQLdb.IntegrityError as err:
        return "error"

# def assignUID(conn):
#     """"""
#     try:
#         curs = conn.cursor(MySQLdb.cursors.DictCursor)
#         curs.execute("SELECT max(userid) from user")
#         uid=curs.fetchone()['max(userid)'] + 1
#         return uid
#     except MySQLdb.IntegrityError as err:
#         return "error"

def registerUser(conn, account_type, firstName, lastName,email, password):
    """Adds a new user to the user table given the information provided
    on the registration form. Also adds the userid to the appropriate
    table (student or mentor)"""
    try:

        curs = conn.cursor(MySQLdb.cursors.DictCursor)

        #insert information into the user database
        curs.execute("insert into user (firstname,lastname,email,password)"+
        "values (%s, %s, %s,%s);", (firstName,lastName, email,password))

        #find the userid assigned to this user in the user table
        curs.execute("SELECT userid from user where email=%s;",[email])
        userid=curs.fetchone()['userid']

        #if it is a mentor account, add the user's userid to the mentor
        #table. Otherwise, if it is a student account, add the user's userid
        #to the student table
        if account_type == "mentor":
            curs.execute("INSERT into mentor (userid) values (%s);",[userid])
        elif account_type== "student":
            curs.execute("INSERT into student (userid) values (%s);",[userid])
        return "registered"
    except MySQLdb.IntegrityError as err:
        return ("Unsuccessful registration")

def getUID(conn,email):
    """Returns the userid assigned to a user with a given email"""
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('SELECT userid FROM user WHERE email = %s;',
                     [email])
        row= curs.fetchone()
        return row['userid']
    except MySQLdb.IntegrityError as err:
        return "error"

def loginSuccess(conn, email, passwd):
    """Checks the credentials provided by the user on the login form.
    If the password and email match those in the database, returns
     'success' """
    try:

        #fetch encrypted password for the matching email in the database
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('SELECT password FROM user WHERE email = %s;',
                     [email])
        row= curs.fetchone()

        #no user with this email address exists in the database
        if row is None:
            # Same response as wrong password, so no information about what went wrong
            flash('login incorrect. Try again or join')
            return False

        #if such a user does exist, check if the hashed password in the database and the
        #encrypted form input match
        hashed = row['password']
        if bcrypt.hashpw(passwd.encode('utf-8'),hashed.encode('utf-8')) == hashed:
            flash('successfully logged in')
            return "success"
        else:
            return False

    except MySQLdb.IntegrityError as err:
        return "Login unsuccessful"

def viewProfile(conn,email):
    """Returns information from the user table for a given user with the
    given email address """
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("select firstname,lastname,description,age,gender,Ethnicity"+
        ",homeState,homeCountry,picture from user where email=%s;",[email])
        info=curs.fetchone()
        return info
    except MySQLdb.IntegrityError as err:
        return "Error"

def viewJobs(conn,userid):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("select title,jobID,company,description,type,experience,"+
        "favoritePart,leastFavoritePart,annualSalary,task,dailylife,skill,"+
        "advice,professionTag,startDate,endDate from job where userid=%s;",
        [userid])
        jobinfo=curs.fetchall()
        return jobinfo
    except MySQLdb.IntegrityError as err:
        return "Error"

def viewEducation(conn,userid):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("select institution,instState,instCountry,major,major2,"+
        "degreetype,overallRating,review from education where userid=%s;",
        [userid])
        eduinfo=curs.fetchall()
        return eduinfo

    except MySQLdb.IntegrityError as err:
        return "Error"


def updateProfile(conn,email,description,age,gender,race,country,state,profpic):
    """Updates the information in the user table for the user with the
    given email address with the information provdied on the
    updateProfile form"""
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)

        curs.execute("update user set description=%s"+
        ",age=%s,gender=%s,Ethnicity=%s, homeCountry=%s, homeState=%s, picture=%s where email=%s",
        [description,age,gender,race,country,state,profpic,email])
        return "successfully updated profile"
    except MySQLdb.IntegrityError as err:
        return "Error"

def addJob(conn,userid,title,company,description,jobtype,
        priorexperience,tags,favorite,leastfav,tasks,daily,skills,advice,
        salary,startdate,enddate):
    """Adds or updates an entry in the job table for a user with the
    given userid """
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)

        curs.execute("select jobID from job where title=%s and userid=%s;",[title,userid])

        #check to see if a job with that title has already been added for that user
        jobexists=curs.fetchone()
        if jobexists!=None:#if a job with the title has been added, update it
            jobid=jobexists['jobID']
            curs.execute("update job set title=%s"+
            ",company=%s,description=%s,type=%s, experience=%s, favoritePart=%s,"+
            "leastFavoritePart=%s, annualSalary=%s, task=%s, dailylife=%s,"+
            "skill=%s, advice=%s, professionTag=%s, startDate=%s,"+
            "endDate=%s where userid=%s and jobID=%s;",
            [title,company,description,jobtype,priorexperience,favorite,leastfav,
            salary,tasks,daily,skills,advice,tags,startdate,enddate,userid,jobid])
            return "A job with this title was already added to your profile.Updating this job"

        #if no job with that title has been added for that user, insert new job
        elif jobexists==None:
            curs.execute("insert into job (title,company,description,type,"+
            "experience,favoritePart,leastFavoritePart,annualSalary,task,"+
            "dailylife,skill,advice,professionTag,startDate,endDate,userid)"+
            "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
            [title,company,description,jobtype,priorexperience,favorite,leastfav,
            salary,tasks,daily,skills,advice,tags,startdate,enddate,userid])
            return "successfully added job"


    except MySQLdb.IntegrityError as err:
        return "Error"


def addEducation(conn,userid,institution,major,secondmajor,degreetype,rating,
                review,country,state):
    """Adds or updates an entry in the education table for a user with the
    given userid """
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)

        curs.execute("select eduID from education where institution=%s and "+
        "degreetype=%s and major=%s and userid=%s;",[institution,degreetype,
        major,userid])

        educationExists=curs.fetchone()
        #check to see if an educational step with matching parameters(institution
        #degree type, major)
        if educationExists!=None: #if such an educational entry has been added, update it

            eduid=educationExists['eduID']
            curs.execute("update education set institution=%s"+
            ",instState=%s,instCountry=%s,major=%s,major2=%s,degreetype=%s,"+
            "overallRating=%s,review=%s where userid=%s and eduID=%s;",
            [institution,state,country,major,secondmajor,degreetype,rating,
            review,userid,eduid])
            return ("You already have an entry with this institution name, degree"+
            "type, and major. Updating this entry")

        #if no such educational entry has already been added, add it to
        #the database
        elif educationExists==None:
            curs.execute("insert into education (userid,institution,"+
            "instState,instCountry,major,major2,degreetype,overallRating,"+
            "review)"+
            "values (%s,%s,%s,%s,%s,%s,%s,%s,%s);",
            [userid,institution,state,country,major,secondmajor,degreetype,
            rating,review])
            return "successfully added education entry!"


    except MySQLdb.IntegrityError as err:
        return "Error"
