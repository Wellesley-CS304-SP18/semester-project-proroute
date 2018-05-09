#database insertion statements
#additional statemnts will be added for displaying information

import dbconn2
import MySQLdb
import os
import sys
#from jaguilar2_db #import DSN

tempPassword = 'secret'
DATABASE = 'jaguilar2_db' #database to insert into needs to be changed to group db

DEBUG = False


def login_user(conn, email, passwd):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)

        if passwd == tempPassword:

            curs.execute('SELECT * FROM user WHERE email = %s', [ email ])
            return "success"
    except MySQLdb.IntegrityError as err:
        return "Login Unsuccessful"


def find_user(conn, email):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)

        curs.execute('SELECT * FROM user WHERE email = %s', [ email ])
        return True;

    except MySQLdb.IntegrityError as err:
        return False;


def register_user(conn, account_type, firstName, lastName,email, password):
    try:
        #print("blah")
        curs = conn.cursor(MySQLdb.cursors.DictCursor)

        curs.execute('INSERT into user (firstname, lastname, email, userid,password) values (%s,%s, %s,2, %s)',[firstName, lastName, email, password])

        if account_type == "Mentor":
            curs.execute('INSERT into mentor (userid) values userid')
        else:
            curs.execute('INSERT into student (userid) values userid')
        return "registered"
    except MySQLdb.IntegrityError as err:
        return ("Unsuccessful registration")


#def insert_education(cursor,userid, institution, instState, instCountry, major, major2, overallRating, review):
#    try:
#        rows = cursor.execute('INSERt into user()')
#    except MySQLdb.Error as err:

#    return ''

#def insert_student(cursor,userid, goal):
#    try:

#    except MySQLdb.Error as err:

#    return ''

#def insert_mentor(cursor,userid, description, cv):
#    try:

#    except MySQLdb.Error as err:
#    return ''

#def insert_job(cursor,userid, title, jobID, company, description, favoritePart, annualSalary, task, advice, professionTag,startDate,endDate):
#    try:

#    except MySQLdb.Error as err:

#    return ''

#def insert_profession(cursor,jobID, professionID, professionName, description, tags, coTags):
#    try:

#    except MySQLdb.Error as err:

#    return ''

#def insert_professionRating(cursor,jobID, professionID, overallRating, workEnvironment, jobSecurity, advancement, skills, hours, stress, learn, beneifits, relationships, diffMental, diffPhysical):
#    try:

#    except MySQLdb.Error as err:

#    return ''

#def insert_question(cursor,userid, questionID, questionText, tag, rating, posted ):
#    try:

#    except MySQLdb.Error as err:

#    return ''

#def insert_answer(cursor,userid, questionID, answerID, answerText, rating, posted):
    #try:

    #except MySQLdb.Error as err:

    #return ''
