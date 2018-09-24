from flask import Flask, request, redirect, render_template
import cgi

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too


def get_current_watchlist():
    # returns user's current watchlist--hard coded for now
    return [ "Star Wars", "Minions", "Freaky Friday", "My Favorite Martian" ]



@app.route('/signup')
def display_user_signup_form():
    return render_template('edit.html')

@app.route("/signup", methods=['POST'])
def validate_form():
    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']
    email = request.form['email']

    if username == "":
        error = "Username can not be left blank"

        return render_template('edit.html', username=username, email=email, error=error)

    if password == "":
        error = "Password can not be left blank"

        return render_template('edit.html', username=username, email=email, error=error)

    if verify == "":
        error = "Password can not be left blank"

        return render_template('edit.html', username=username, email=email, error=error)

    if password != verify:
        error = "Passwords do not match"

        return render_template('edit.html', username=username, email=email, error=error)

    if len(username) < 3 or \
            len(username) > 20 or \
            ' ' in username:
        error = "Username must be more than 3 characters \n " \
                "Username must be less than 20 characters \n " \
                "Username cannot contain spaces"

        return render_template('edit.html', username=username, email=email, error=error)

    if len(password) < 3 or \
            len(password) > 20 or \
            ' ' in password:
        error = "Password must be more than 3 characters \n " \
                "Password must be less than 20 characters \n " \
                "Password cannot contain spaces"

        return render_template('edit.html', username=username, email=email, error=error)

    if len(email) > 0 and \
            len(email) < 3 or \
            len(email) > 20 or \
            ' ' in email or \
            email.find('.') == -1 or \
            email.find('@') == -1 :
        error = "Email must be more than 3 characters \n " \
                "Email must be less than 20 characters \n " \
                "Email cannot contain spaces \n " \
                "Email must contain a single period \n " \
                "Email must contain a single @"

        return render_template('edit.html', username=username, email=email, error=error)

    # if we didn't redirect by now, then all is well
    return render_template('signup.html', username=username)

@app.route("/add", methods=['POST'])
def add_movie():
    # look inside the request to figure out what the user typed
    new_movie = request.form['new-movie']

    # if the user typed nothing at all, redirect and tell them the error
    if (not new_movie) or (new_movie.strip() == ""):
        error = "Please specify the movie you want to add."
        return redirect("/?error=" + error)

    # if the user wants to add a terrible movie, redirect and tell them the error
    if new_movie in terrible_movies:
        error = "Trust me, you don't want to add '{0}' to your Watchlist".format(new_movie)
        return redirect("/?error=" + error)

    # 'escape' the user's input so that if they typed HTML, it doesn't mess up our site
    new_movie_escaped = cgi.escape(new_movie, quote=True)

    # TODO:
    # Create a template called add-confirmation.html inside your /templates directory
    # Use that template to render the confirmation message instead of this temporary message below
    return render_template('add.html', new_movie=new_movie)

# TODO:
# Modify the edit.html file to display the watchlist in an unordered list with bullets in front of each movie.
# Put the list between "Flicklist" and "Edit My Watchlist" under this heading: <h2>My Watchlist</h2>

# TODO:
# Change get_current_watchlist to return []. This simulates a user with an empty watchlist.
# Modify edit.html to make sense in such a situation:
#  First: Hide the <h2>My Watchlist</h2> and it's unordered list.
#  Second: Hide the crossoff form, since there are no movies to cross off.
# Then you can change get_current_watchlist back to the list of hard-coded movies.

@app.route("/")
def index():
    encoded_error = request.args.get("error")
    return render_template('edit.html', watchlist=get_current_watchlist(), error=encoded_error and cgi.escape(encoded_error, quote=True))

app.run()
