from flask import Flask, render_template, redirect, request, flash, session, g, url_for
import model

app = Flask(__name__)


USER_ID = None 

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
        u=model.User()
        u.email=request.form["email"]
        u.password=request.form["password"]
        #there should be a better way of getting the id, correct?
        the_user=model.session.query(model.User).filter_by(email=u.email).one()
        u.id=the_user.id
        print "USER ID IS: ", u.id
        if not (model.session.query(model.User).filter_by(email=u.email).filter_by(password=u.password).all()):
            print "Email address not registered. Check spelling or sign up."
            #find a way to display that message to the screen
            #flash(u'Email address not registered. Check spelling or Sign Up')
            return redirect("/")
        else:
            session['user_id']=u.id
            return render_template("user_page.html", user=u)

@app.route("/user", methods=['GET','POST'])
def users():
    user_id = request.args.get("id")
    user=model.session.query(model.User).get("user_id")
    return render_template("user_page.html",user=user)#,ratings=ratings)

@app.route("/movie_page")
def movie():
    movie_title = request.args.get("title")
    movie=model.session.query(model.Movie).filter_by(movie_title=movie_title).one()

    sum_of_ratings = 0

    for i in movie.rating:
        sum_of_ratings += i.rating

    avg_rating = sum_of_ratings/len(movie.rating)
    return render_template("movie_page.html", avg_rating=avg_rating,movie=movie_title)

@app.before_request
def before_request():
    # anon_pages = ["/", "/login"]
    user_id=session.get("user_id")
    print "user_id in before request is: ", user_id
    if user_id:
        user=model.session.query(model.User).get(user_id)
        g.user=user
        print "g.user.id is: ", g.user.id
    else:
        g.user=None
        # if request.path not in anon_pages
        #     return redirect("/login")

    #use the commented out lines of code so on other pages, like "/add_rating"
    #I don't need to use my if and else statements because if a person is on
    #those pages, that means they are logged in


@app.route("/add_rating")
def add_rating():
    #user_id=session.get("user_id")
    #print "user id w/ session is: ", user_id
    print "g.user is:", g.user.id
    if g.user:#user_id: 
        r=model.Rating()
        print "R is:", r
        r.movie_title = request.args.get("movie_title")
        r.rating = request.args.get("rating")
        print "user id is: ", r.user_id
        g.user.ratings.append(r)
        model.session.add(r)
        model.session.commit()
        return redirect("/user")
    else:
        print "user doesn't exist!"
    # else:
    # print "not logged in!!!"
    # return redirect("/")


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