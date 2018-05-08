
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, session, send_from_directory, jsonify, flash)

app = Flask(__name__)
app = Flask(__name__, static_url_path="/static")

import sys,os,random
import dbconn2
import helperFunctions
import MySQLdb

app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.config['SECRET_KEY'] = 'something very secret'

# Route for rating movies
# @app.route('/rateMovies/', methods=['GET', 'POST'])
# def rateMovies():
#     conn = dbconn2.connect(DSN)
#
#     # check if there's a useridCookie in the browser already
#     userid = request.cookies.get('useridCookie')
#
#     if request.method == "GET":
#         # if user is not logged in, redirect them to login page
#         if not userid:
#             return redirect(url_for('login'))
#         # if user is logged in, direct them to rateMovies page
#         else:
#             if request.method == "GET":
#                 movies = helperFunctions.getMovies(conn)
#                 return render_template('rateMovies.html',
#                                         header = 'Rate Movies',
#                                         movies = movies, userid=userid)
#
#     if request.method == "POST":
#         # get the user's rating of a movie and that movie's tt from the form
#         movie_rating = request.form['stars']
#         tt = request.form['movie_tt']
#
#         # if user submitted form but didn't select a movie rating
#         if not movie_rating:
#             flash('Please select a movie rating')
#             return render_template('rateMovies.html',
#                                     header = 'Rate Movies',
#                                     movies = movies,userid=userid)
#         # update the movie rating in the database and re-render the page
#         # with all updated movies
#         else:
#             movies=helperFunctions.updateMovieRating(conn,userid,tt,movie_rating)
#             return render_template('rateMovies.html',
#                                     header='Rate Movies',
#                                     movies=movies,userid=userid)

# Route for logging in
@app.route('/login/', methods=['GET', 'POST'])
def login():
    conn = dbconn2.connect(DSN)
    # check if there's a useridCookie in the browser already
    useridCookie = request.cookies.get('useridCookie')

    if request.method == "GET":
        return render_template('home/login.html')

    if request.method == "POST":
        # get userid and password from the form
        try:
            email=request.form['email']
            password= request.form['password']
            conn = dbconn2.connect(DSN)
            # userid=assignUID(conn)
            # returns true or false
            loginSuccess = helperFunctions.loginSuccess(conn, email, password)
            print loginSuccess
            # if login credentials are verified, tell user they've logged in
            # and set their userid as a cookie
            if loginSuccess == "success":
                flash("Login succeeded!")
                resp = make_response(render_template('home/updateProfile.html',
                                                     allCookies=request.cookies))
                resp.set_cookie('useridCookie',value=email)
                return resp
            # if login is unsuccessful because user provides wrong password
            # or no userid, prompt them to re-attempt to login
            else:
                flash("Email or password are incorrect. Please try again")
                return render_template('home/login.html')
        except Exception as err:
                print 'error is', typer(err), err
                flash('Missing inputs')
                error = True

@app.route('/register/', methods=['GET', 'POST'])
def register():
    conn = dbconn2.connect(DSN)
    if request.method == "GET":
        return render_template('home/register.html',message="")
    # form = RegisterForm(request.form)
    if request.method == 'POST':
        usertype= request.form['usertype']
        firstName=request.form['firstName']
        lastName=request.form['lastName']
        email=request.form['myEmail']
        password=request.form['password']
        confirm_password=request.form["confirm_pass"]
        if password!=confirm_password:
            flash("Passwords don't match. Please try again")
            return render_template('home/register.html')
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute("SELECT * from user where email=%s;",[email])
        existing_email = curs.fetchone()
        if (existing_email != None):
            flash("This email address is already associated with an account."+
            "Please sign in")
            return render_template('home/register.html')
        else:
            curs.execute("insert into user (firstname,lastname,email,password)"+
            "values (%s, %s, %s,%s);", (firstName, lastName, email,password))


        print usertype;
        return render_template('home/updateProfile.html')

    #     if form.validate_on_submit():
    #         try:
    #             new_user = User(form.email.data, form.password.data)
    #             new_user.authenticated = True
    #             db.session.add(new_user)
    #         db.session.commit()
    #             flash('Thanks for registering!', 'success')
    #             return redirect(url_for('recipes.index'))
    #         except IntegrityError:
    #             db.session.rollback()
    #             flash('ERROR! Email ({}) already exists.'.format(form.email.data), 'error')
    # return render_template('register.html', form=form)


# Route for updating a movie's rating using ajax
# @app.route('/setRatingAjax/',methods=['POST'])
# def setRatingAjax():
#     try:
#         conn = dbconn2.connect(DSN)
#         # check if there's a useridCookie in the browser already
#         useridCookie = request.cookies.get('useridCookie')
#
#         # get movie rating and tt from form
#         movie_rating = request.form['rating']
#         tt = request.form['tt']
#
#         # update rating in the database
#         helperFunctions.updateMovieRating(conn,useridCookie,tt,movie_rating)
#
#         # find the movie's newly updated average rating
#         averageRating= helperFunctions.getAverageRating(conn,tt)['averageRating']
#
#         # send the data back to the frontend
#         return jsonify({'useridCookie':useridCookie,'movie_rating':movie_rating,
#         'movie_tt':tt,'averageRating':averageRating})
#
#     except Exception as err:
#         return jsonify({'error':True,'err':str(err)})
#

# Route for updating a movie
# @app.route('/update/<tt>', methods=['GET', 'POST'])
# def update(tt):
#     conn = dbconn2.connect(DSN)
#     if request.method == "GET":
#         movie = helperFunctions.findMovie(conn, tt)
#         return render_template('update.html',
#                                 movie=movie,
#                                 header = 'Update Movie')
#
#     if request.method == "POST":
#         title = request.form['movie-title']
#         new_tt = request.form['movie-tt']
#         release = request.form['movie-release']
#         addedby = request.form['movie-addedby']
#         director = request.form['movie-director']
#
#         # if update button was pressed
#         if request.form['submit'] == "update":
#             status = helperFunctions.updateMovie(conn, tt, new_tt, title,
#                                                 release, addedby, director)
#
#             # if movie was updated successfully
#             if status == 200:
#                 # if the tt wasn't changed, re-render page with new movie info
#                 if tt == new_tt:
#                     movie = {'title': title,
#                              'tt': tt,
#                              'release': release,
#                              'addedby': addedby,
#                              'director': director}
#                     return render_template('update.html',
#                                             movie = movie,
#                                             header = 'Update Movie')
#                 # if the tt was updated, redirect to the corresponding url
#                 else:
#                     return redirect(url_for('update', tt = new_tt))
#             # if there was an error in updating the movie
#             else:
#                 movie = helperFunctions.findMovie(conn, tt)
#                 return render_template('update.html',
#                                         movie = movie,
#                                         header = 'Update Movie')
#         # if delete button was pressed
#         else:
#             helperFunctions.deleteMovie(conn, tt)
#             return redirect(url_for('index'))
#
# Route for searching for a movie title
# @app.route('/search/', methods=['GET', 'POST'])
# def search():
#     conn = dbconn2.connect(DSN)
#
#     if request.method == "GET":
#         return render_template('search.html', header = 'Search by Title')
#
#     if request.method == "POST":
#         # Get input string for search title from form
#         search_title = request.form['search-title']
#         tt = helperFunctions.findMovieTT(conn, search_title)
#         # If no matching movie found, flash error message and re-render
#         if tt == None:
#             flash("No matching movie.")
#             return render_template('search.html', header = 'Search by Title')
#         # If matching movie found, redirect to corresponding movie page
#         else:
#             return redirect(url_for('update', tt = tt))

# Route for selecting movies that have a null value for release / director
# @app.route('/select/', methods=['GET', 'POST'])
# def select():
#     conn = dbconn2.connect(DSN)
#
#     if request.method == "GET":
#         allmovies = helperFunctions.selectMovie(conn)
#         return render_template('select.html',
#                                 allmovies = allmovies,
#                                 header = 'Select Movie')
#
#     if request.method == "POST":
#         selected_movie_tt = request.form.get('menu-tt')
#         movie = helperFunctions.findMovie(conn, selected_movie_tt)
#         return redirect(url_for('update', tt = movie['tt']))

# Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = dbconn2.connect(DSN)
    userid = request.cookies.get('useridCookie')
    if not userid:
        print 'no userid'
        return redirect(url_for('login'))
    else:
        return render_template('home/updateProfile.html')
    # return redirect(url_for('login'))
    # return render_template('home/login.html')

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
