#database insertion statements
#additional statemnts will be added for displaying information

import dbconn2
import MySQLdb
import os
from jaguilar2_db import DSN

DATABASE = 'jaguilar2_db' #database to insert into needs to be changed to group db

DEBUG = False

def cursor (database = DATABASE):
    DSN['db'] = database
    conn = dbconn2.connect(DSN)
    return conn.cursor(MySQLdb.cursors.DictCursor)

def insert_user(cursor, user_firstName, user_lastName, user_userName, user_email
    user_userId, user_password, user_age, user_gender, user_homeState, user_homeCountry,user_ethnicity):
    try:
        rows = cursor.execute('INSERT into user(firstname, lastname, username, email, userid, password, age, gender,
        homeState, homeCountry, Ethnicity) values (%s,%s, %s,%s, %d, %s, %d,%s,%s,%s,%s)'),
        (user_firstName,user_lastName, user_userName, user_email, user_userId, user_password, user_age
        user_gender,user_homeState, user_homeCountry, user_ethnicity)

    except MySQLdb.Error as err:
        print "MySQL exception %s while signing up person %s, %s, %s"%(err,
        user_firstName, user_lastName, user_userName)
        raise
    if rows != 1:
        print ("Insert might not have worked at %s" %(rows,))

def insert_education():
    return ''

def insert_student():
    return ''

def insert_mentor():
    return ''

def insert_job():
    return ''

def insert_profession():
    return ''

def insert_professionRating():
    return ''

def insert_question():
    return ''

def insert_answer():
    return ''
