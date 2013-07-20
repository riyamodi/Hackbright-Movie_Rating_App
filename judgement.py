from flask import Flask, render_template, redirect, request, flash, session, g, url_for
import model

app = Flask(__name__)


USER_ID = None 

@app.before_request
def before_request():
    # anon_pages = ["/", "/login"]
    user_id=session.get("user_id")
    # print "user_id in before request is: ", user_id
    if user_id:
        user=model.session.query(model.User).get(user_id)
        g.user=user
        # print "g.user.id is: ", g.user.id
    else:
        g.user=None
        # if request.path not in anon_pages
        #     return redirect("/login")

    #use the commented out lines of code so on other pages, like "/add_rating"
    #I don't need to use my if and else statements because if a person is on
    #those pages, that means they are logged in


@app.route("/")
def index():
    return render_template("homepage.html", users=user_list)

@app.route("/user_list")
def user_list():
    user_list = model.session.query(model.User).limit(20).all()
    return render_template("user_list.html", users=user_list)

@app.route("/add_user" , methods=['GET','POST'])
def add_user():
    print "BEGINING OF FUNCTION!"
    #form = RegistrationForm(request.form)
    if request.method=='POST':
        u = model.User()
        u.email=request.form["email"]
        u.password=request.form["password"]
        u.zipcode=request.form["zipcode"]
        u.occupation=request.form["occupation"]
        u.age=request.form["age"]
        u.gender=request.form["gender"]
    # to create an object of the User class and create the attributes in one line is:
    # u=User(email=request.args.get("email"), password=request.args.get("password")...)
        model.session.add(u)
        model.session.commit()
        print "committed everything"
    return render_template("new_user.html", user=u)

@app.route("/log_in", methods=['POST'])
def log_in():
    if request.method=='POST':
        email=request.form["email"]
        password=request.form["password"]
        #there should be a better way of getting the id, correct?
        the_user=model.session.query(model.User).filter_by(email=email, password=password).one()
        if not the_user:
            print "Email address not registered. Check spelling or sign up."
            #find a way to display that message to the screen
            #flash(u'Email address not registered. Check spelling or Sign Up')
            return redirect("/")
        else:
            session['user_id']=the_user.id
            return render_template("user_page.html", user=the_user)

@app.route("/user", methods=['GET','POST'])
def users():
    
    if request.args.get("id"):
        user_id = request.args.get("id") ## Actually, check this instead
        print "user_id is: ", user_id
        user=model.session.query(model.User).get(user_id)
    else:    
        user=g.user
    
    return render_template("user_page.html",user=user)

    # if 'user_id' in session:
    #     user=g.user
    # else:
    #     user_id = request.args.get("id") ## Actually, check this instead
    #     print "user_id is: ", user_id
    #     user=model.session.query(model.User).get(user_id)
        #print "user is: ", user
    # return render_template("user_page.html",user=user)

@app.route("/movie_page")
def movie():
    movie_title = request.args.get("title")
    movie=model.session.query(model.Movie).filter_by(movie_title=movie_title).one()

    sum_of_ratings = 0

    for i in movie.ratings:
        sum_of_ratings += i.rating

    avg_rating = sum_of_ratings/len(movie.ratings)

    # user=g.user

    # r=model.Rating()
    # rating=model.session.query(model.Movie).filter_by(movie_title=movie_title, user_id=user.id).one()
    # r.rating=rating.ratings

    return render_template("movie_page.html", avg_rating=avg_rating,movie=movie)#, user_rating=r)

@app.route("/add_rating")
def add_rating():
    if g.user: 
        r=model.Rating()
        print "R is:", r
        r.movie_title = request.args.get("movie_title")
        movie = model.session.query(model.Movie).filter_by(movie_title=r.movie_title).one()
        r.movie_id = movie.id
        r.rating = request.args.get("rating")
        print "user id is: ", r.user_id
        g.user.ratings.append(r)
        model.session.add(r)
        model.session.commit()
        return redirect("/user")
    else:
        return redirect("/")

@app.route("/update_rating")
def change_rating():
    if g.user:

        #get a user's id
        #get all of that user's ratings
        #get the rating that matches with the movie title
        user=g.user
        user_rating=user.ratings #list of all the user's ratings
        movie_id = int(request.args.get("movie_id"))
        for rating in user_rating:
            if rating.movie_id == movie_id:
                change_me = movie_id
                rating_to_change=rating.rating
            else:
                change_me = None
        if change_me==None:
            print "You haven't rated this movie yet"
            return redirect("/log_in")
        else: 
            print "the rating i want to change is: ", rating_to_change
            return "NOW I NEED TO FIGURE OUT HOW TO CHANGE THE RATING"
            #print "trying this: ", user.ratings.movie.rating
            # m=model.session.query(model.Movie).filter_by(id=movie_id).one()
            # print "m.user.rating is: ", user.ratings.m.rating


        # Now, if change_me is None, go to page saying the movie has not been rated.
        # Else, update the rating value and tell the user that you did that.


        #movie.rating exist?
        
        # users_ratings = user.ratings[0].movie.movie_title
        # print "my rating: ", users_ratings
        
        # r=model.session.query(model.Ratings).filter_by(user_id=user.id).all()
        # existing_rating=model.session.query(model.Movie).filter_by(movie_title=movie_title).one()
        

        #get a user's rating for a movie and delete it
        # r = model.Rating()
        # r.movie_title = request.args.get("movie_title")
        # movie = model.session.query(model.Movie).filter_by(movie_title=r.movie_title).one()
        # print "movie is: ", movie
        # print "movie's rating: ", movie.rating

        # new_rating = request.args.get("new_rating")

        # print "movie", movie
        # previous_rating = r.movie.rating
        # print "previous_rating is: ", previous_rating
        


        # print "movie is: ", movie_title
        # print "new rating is: ", new_rating

    else:
        return redirect("/")

@app.route("/logout")
def logout():
    del session['user_id']
    return redirect(url_for("index"))
#use a random generator to get a good secret key:
#>>import os
#>>os.urandom(37)
app.secret_key="""8\x95[_L*O\x11\xb0\x96\x11DQ\xc8\xa8?B\xa4\xd4n\xed\x9c.\xb8\xfaGx\x9c\x03\xed\xdb"o\xb6"\xe6^"""

if __name__ == "__main__":
    app.run(debug=True)