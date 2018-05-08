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



    #print "the begin of login_user"
    #try:
    #    rows = cursor.execute('SELECT * FROM user WHERE email = (%s)', email)
#    except MySQLdb.Error as err:
        #print "MySQL exception %s while signing up person %s"%(err,
        #email)


#def insert_user(cursor, firstName, lastName, userName, email
#    userId, password, age, gender, homeState, homeCountry,ethnicity):
#    try:
#        rows = cursor.execute('INSERT into user(firstname, lastname, username, email, userid, password, age, gender,
#        homeState, homeCountry, Ethnicity) values (%s,%s, %s,%s, %d, %s, %d,%s,%s,%s,%s)'),
###
    #except MySQLdb.Error as err:
    #    print "MySQL exception %s while signing up person %s, %s, %s"%(err,
    #    firstname, lastName, userName)
    #    raise
    #if rows != 1:
    #    print ("Insert might not have worked at %s" %(rows,))

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
