from flask import Flask, render_template, redirect, request, flash, session, g, url_for
import model

app = Flask(__name__)


USER_ID = None 

@app.before_request
def before_request():
    # anon_pages = ["/", "/login"]
    user_id=session.get("user_id")
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
        #should i be doing .one() bc it will throw an error if it can't find anything
        the_user=model.session.query(model.User).filter_by(email=email, password=password).one()
        if not the_user:
            print "Email address not registered. Check spelling or sign up."
            #find a way to display that message to the screen
            #flash("Email address not registered. Check spelling or Sign Up")
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
    movie_id = request.args.get("id")
    movie=model.session.query(model.Movie).filter_by(id=movie_id).one()
    print "movie is: ", movie.id

    ratings = movie.ratings #list of all ratings for the specific movie
    # print "list of ratings are: ", ratings
    
    rating_nums = []
    user_rating = None

    for r in ratings:
        if g.user:
            if r.user_id == session['user_id']:
                user_rating = r
        rating_nums.append(r.rating)
    avg_rating = float(sum(rating_nums))/len(rating_nums)

    #Prediction code: only predict if the user hasn't rated the movie yet
    if g.user:  #can only do the following code if a user has logged in
        user = model.session.query(model.User).get(session['user_id'])
        prediction = None 
        if not user_rating:
            prediction = user.predict_rating(movie)
            # print "prediction is: ", prediction
            effective_rating = prediction
        else:
            effective_rating=user_rating.rating

        the_eye= model.session.query(model.User).filter_by(email="theeye@ofjudgement.com").one()
        eye_rating = model.session.query(model.Rating).filter_by(user_id=the_eye.id, movie_id=movie.id).first()

        if not eye_rating:
            eye_rating = the_eye.predict_rating(movie)
        else:
            eye_rating = eye_rating.rating

        difference = abs(eye_rating - effective_rating)

        messages = ["I suppose you don't have the worst taste possible.",
                    "Not the worst opinion but not the best.",
                    "You need to reevaluate your tastes and/or personality.", 
                    "I regret every decision that I've made to listen to your opinion."]

        beratement = messages[int(difference)]

        return render_template("movie_page.html", avg_rating=avg_rating,movie=movie, 
                            user_rating=user_rating,prediction= prediction, beratement=beratement)#, user_rating=r)
   
    #if no user has logged in, return this:
    return render_template("movie_page.html", avg_rating=avg_rating,movie=movie)
######################################
    # user=g.user

    # r=model.Rating()
    # rating=model.session.query(model.Movie).filter_by(movie_title=movie_title, user_id=user.id).one()
    # r.rating=rating.ratings


#should make a check so peope can't add multiple ratings for the same movie
@app.route("/add_rating")
def add_rating():
    if g.user: 
        r=model.Rating()
        print "R is:", r
        r.movie_id = request.args.get("movie_id")
        print "movie_id is: ", r.movie_id
       
        #check to see if we got to this route by just entering the movie title
        if r.movie_id is None:
            r.movie_title=request.args.get("movie_title")
            print "the movie title is: ", r.movie_title
            movie = model.session.query(model.Movie).filter_by(movie_title=r.movie_title).one()
            r.movie_id = movie.id
            return render_template("movie_page.html", movie=movie, rating=r)

        r.rating = request.args.get("rating")
        r.user_id=g.user.id
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

        user=g.user
        
        movie_id = int(request.args.get("movie_id"))
        print "movie id is: ", movie_id
        
        new_rating = request.args.get("new_rating")
        print "the new rating is: ", new_rating

        movie_title = request.args.get("title")
        print "movie_title is: ", movie_title

        users_movie_rating = model.session.query(model.Rating).filter_by(movie_id=movie_id, user_id=user.id).all()
        print "users movie rating: ", users_movie_rating

        if not users_movie_rating:
            print "you haven't rated this movie yet"
            return redirect("/movie_page?title=%s" % movie_title)

        else:    
            update_rating=model.session.query(model.Rating).filter_by(movie_id=movie_id, user_id=user.id).update({"rating": new_rating})
            print "update rating is: ", update_rating
            #model.session.add(update_rating)
            print "added session"
            model.session.commit()
            return redirect("/user")
    else:
        print "you haven't logged in yet"
        return redirect("/")
        #*************************************************

        # user=g.user
        # print "user's id is: ", user.id
        # user_rating=user.ratings #list of all the user's ratings
        # print "list of all the user's ratings: ", user_rating
        # movie_id = int(request.args.get("movie_id"))
        # print "movie id is: ", movie_id
        # for rating in user_rating:
        #     print "rating.movie_id is: ", rating.movie_id
        #     if rating.movie_id == movie_id:
        #         change_me = movie_id
        #         rating_to_change=rating.rating
        #         break
        #     else:
        #         change_me = None
        # if change_me==None:
        #     print "You haven't rated this movie yet"
        #     return redirect("/log_in")
        # else: 
        #     print "the rating I want to change is: ", rating_to_change
        #     new_rating = request.args.get("new_rating")
        #     print "the new rating is: ", new_rating

            
        #     return "NOW I NEED TO FIGURE OUT HOW TO CHANGE THE RATING"
            
        #************************************************************

        #get a user's id
        #get all of that user's ratings
        #get the rating that matches with the movie title
        

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