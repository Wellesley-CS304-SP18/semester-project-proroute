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


def register_user(conn, account_type, firstName, lastName,email, password):
    try:
        #print("blah")
        curs = conn.cursor(MySQLdb.cursors.DictCursor)

        curs.execute('INSERT into user (firstname, lastname, email, userid,password)'+
        ' values (%s,%s, %s, %s)',[firstName, lastName, email, password])

        if account_type == "Mentor":
            curs.execute('INSERT into mentor (userid) values userid')
        else:
            curs.execute('INSERT into student (userid) values userid')
        return "registered"
    except MySQLdb.IntegrityError as err:
        return ("Unsuccessful registration")

def add_question(conn, userid, questionText, posted):
    #questionID not required because of auto_increment
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('INSERT into question (userid, questionText, posted)' +
        'values (%s,%s, %s)',[userid, questionText, posted])

    except MySQLdb.IntegrityError as err:
        print "got an error"
        return "error"


def show_questions(conn):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('SELECT * FROM question')

        info=curs.fetchall()
        return info


    except MySQLdb.IntegrityError as err:
        return "error"

def get_question(conn, questionID):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('SELECT * FROM question WHERE questionID = %s', [questionID])

        info=curs.fetchone()
        return info


    except MySQLdb.IntegrityError as err:
        return "error"


def add_answer(conn, userid, questionID, answerText, posted):
    #answerID not required because of auto_increment
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)


        curs.execute('INSERT into answer (userid, answerText, posted)' +
        'values (%s,%s, %s)',[userid, answerText, posted])


    except MySQLdb.IntegrityError as err:
        return "error"


def show_answers(conn, questionID):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)


        curs.execute('SELECT * FROM answer where questionID = %s',[questionID])

        info=curs.fetchall()
        return info

    except MySQLdb.IntegrityError as err:
        return "error"




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
