# CS 304 Homework 7
# April 12, 2018
# Authors: Katy Ma and Isabel D'Alessandro

import sys
import MySQLdb
import dbconn2
from flask import flash

temporaryPassword = '123'

# Update movie rating in the database and return updated list of movies
# def updateMovieRating(conn, userid, tt, movierating):
#     try:
#         curs = conn.cursor(MySQLdb.cursors.DictCursor)
#
#         # check movieRatings to see if user has already rated that movie
#         curs.execute("SELECT * FROM movieRatings WHERE userid = %s AND tt = %s",
#                     [userid, tt])
#         foundMovie = curs.fetchone()
#
#         # if user has rated the movie already, update their rating
#         if foundMovie != None:
#             curs.execute("UPDATE movieRatings SET movie_rating = %s WHERE " +
#                         "tt = %s AND userid = %s", [movierating, tt, userid])
#         # if not, insert new rating for movie associated with the userid
#         else:
#             curs.execute("INSERT INTO movieRatings (userid, movie_rating, tt)" +
#                         " VALUES (%s, %s, %s)", (userid, movierating, tt))
#
#         # calculate new average rating based on updated information
#         curs.execute("SELECT SUM(movie_rating) FROM movieRatings WHERE " +
#                     "tt = %s", [tt])
#         newSumOfRatings = curs.fetchone()['SUM(movie_rating)']
#         curs.execute("SELECT COUNT(*) FROM movieRatings WHERE tt = %s", [tt])
#         newNumRatings = curs.fetchone()['COUNT(*)']
#         newAvgRating = round((float(newSumOfRatings) / float(newNumRatings)),1)
#
#         # update average rating in the movie table
#         curs.execute("UPDATE movie SET averageRating = %s where tt = %s",
#                     [newAvgRating, tt])
#
#         # return updated movie list
#         curs.execute("SELECT * FROM movie LIMIT 20")
#         movies = curs.fetchall()
#         return movies
#
#     except MySQLdb.IntegrityError as err:
#         return "Updating movie was unsuccessful"
#
# # Get the average rating for a particular movie
# def getAverageRating(conn,tt):
#     curs = conn.cursor(MySQLdb.cursors.DictCursor)
#     curs.execute("SELECT averageRating from movie where tt=%s",[tt])
#     foundMovie=curs.fetchone()
#     return foundMovie

# Get the first 20 movies from the database
# def getMovies(conn):
#     try:
#         curs = conn.cursor(MySQLdb.cursors.DictCursor)
#         curs.execute("SELECT * FROM movie LIMIT 20")
#         movies = curs.fetchall()
#         return movies
#     except MySQLdb.IntegrityError as err:
#         return "Fetching movies was unsuccessful"

# If user enters correct password, log them in successfully
def loginSuccess(conn, email, passwd):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        if passwd == temporaryPassword:
            # curs.execute("SELECT userid FROM movieRatings WHERE userid = userid")
            return "success"
    except MySQLdb.IntegrityError as err:
        return "Login unsuccessful"


def assignUID(conn):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("SELECT max(userid) from user")
        uid=curs.fetchone()
        return uid
    except MySQLdb.IntegrityError as err:
        return "error"

# Using its title, find a movie's tt
# def findMovieTT(conn, search_title):
#     try:
#         curs = conn.cursor(MySQLdb.cursors.DictCursor)
#         # Use wildcard to find movie title containing the search string
#         like_title = "%" + search_title + "%"
#         curs.execute("SELECT tt FROM movie WHERE title LIKE %s", [like_title])
#         movie = curs.fetchone()
#         if (movie == None):
#             return None
#         return movie['tt']
    #
    # except MySQLdb.IntegrityError as err:
    #     return "No movie found"

# Using its tt, find a movie
# def findMovie(conn, tt):
#     try:
#         curs = conn.cursor(MySQLdb.cursors.DictCursor)
#         # Inner join movie and person to get info for both movie and director
#         curs.execute("SELECT * FROM movie INNER JOIN person " +
#                     "WHERE tt = %s AND director = nm", [tt])
#         movie = curs.fetchone()
#         # If director is not specified, search again for movie info only
#         if (movie == None):
#             curs.execute("SELECT * FROM movie WHERE tt = %s", [tt])
#             movie = curs.fetchone()
#         return movie
#
#     except MySQLdb.IntegrityError as err:
#         return "No movie found"

# Update a movie using new movie info
# def updateMovie(conn, tt, new_tt, title, release, addedby, director):
#     try:
#         curs = conn.cursor(MySQLdb.cursors.DictCursor)
#         # If tt is changed, check if new_tt already exists
#         if new_tt != tt:
#             curs.execute("SELECT * FROM movie WHERE tt = %s", [new_tt])
#             existing_movie = curs.fetchone()
#
#             # If new_tt already exists, flash error message, return error status
#             if (existing_movie != None):
#                 flash("This movie already exists. Try a different movie ID.")
#                 return 500
#
#         # Check if director already exists
#         curs.execute("SELECT * FROM person WHERE nm = %s", [director])
#         existing_director = curs.fetchone()
#
#         # If director doesn't exist, flash error message, return error status
#         if (existing_director == None):
#             flash("This director doesn't exist. " +
#                     "Please enter a valid director ID.")
#             return 500
#
#         # Normalize attributes
#         new_tt = check_if_none(new_tt)
#         addedby = check_if_none(addedby)
#         director = check_if_none(director)
#
#         # If no errors, update the movie and return succuss status
#         curs.execute("UPDATE movie SET tt = %s, title = %s, `release` = %s, " +
#                     "addedby = %s, director = %s where tt = %s",
#                     [new_tt, title, release, addedby, director, tt])
#         flash(title + ' was updated successfully!')
#         return 200
#
#     except MySQLdb.IntegrityError as err:
#         return "Error updating movie"
#
# # Using its tt, delete a movie
# def deleteMovie(conn, tt):
#     try:
#         curs = conn.cursor(MySQLdb.cursors.DictCursor)
#         curs.execute("DELETE FROM movie WHERE tt = %s", [tt])
#         flash('Movie was deleted')
#
#     except MySQLdb.IntegrityError as err:
#         return "Error deleting movie"
#
# # Select all movies that have a null value for release / director
# def selectMovie(conn):
#     try:
#         curs = conn.cursor(MySQLdb.cursors.DictCursor)
#         curs.execute("SELECT tt, title FROM movie " +
#                     "WHERE director is null OR `release` is null")
#         allmovies = curs.fetchall()
#         return allmovies
#
#     except MySQLdb.IntegrityError as err:
#         return "Error fetching movies"
#
# # Helper function to check if attribute is None
# # Return None if attribute is "None", "null" or 0
# def check_if_none(attribute):
#     if attribute != "None" and attribute != "null" and attribute != 0:
#         return attribute
