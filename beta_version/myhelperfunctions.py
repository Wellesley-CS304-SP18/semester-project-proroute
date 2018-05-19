#database insertion statements
#additional statemnts will be added for displaying information

import dbconn2
import MySQLdb
import os
import sys
#from jaguilar2_db #import DSN


DATABASE = 'idalessa_db' #database to insert into needs to be changed to group db

DEBUG = False
"""HELPER FUNCTIONS FOR THE FORUM"""

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


def add_question(conn, userid, questionText, tags, posted):
    """ adds a question to the database"""
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('INSERT into question (userid,questionText,tag,posted)' +
        'values (%s,%s, %s,%s)',[userid, questionText,tags,posted])
    except MySQLdb.IntegrityError as err:
        return "error"


def show_questions(conn):
    """ returns the questions stored in the database"""
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('SELECT * FROM question')

        info=curs.fetchall()
        return info


    except MySQLdb.IntegrityError as err:
        return "error"

def get_question(conn, questionID):
    """ returns a particular question by its id"""
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('SELECT * FROM question WHERE questionID = %s', [questionID])

        info=curs.fetchone()
        return info


    except MySQLdb.IntegrityError as err:
        return "error"


def add_answer(conn, userid, questionID, answerText, posted):
    """ an answer is added to the database"""
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        print 'inside the querything'

        curs.execute('INSERT into answer (userid, questionID,answerText,posted)' +
        'values (%s,%s, %s,%s);',[userid,questionID,answerText, posted])

        print "WEVE ADDED A ANSWER in ADD_ANSWER"
    except MySQLdb.IntegrityError as err:
        return "error"


def show_answers(conn, questionID):
    """ returns the answer stored in the database"""
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)


        curs.execute('SELECT * FROM answer where questionID = %s',[questionID])

        info=curs.fetchall()
        return info

    except MySQLdb.IntegrityError as err:
        return "error"
