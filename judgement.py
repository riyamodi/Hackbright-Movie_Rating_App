from flask import Flask, render_template, redirect, request, flash
import model

app = Flask(__name__)

LOGGED_IN = False
USER_ID = None 

@app.route("/")
def index():
    print "LOGGED_IN: " , LOGGED_IN
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
        if not (model.session.query(model.User).filter_by(email=u.email).filter_by(password=u.password).all()):
            print "Email address not registered. Check spelling or sign up."
            #find a way to display that message to the screen
            #flash(u'Email address not registered. Check spelling or Sign Up')
            return redirect("/")
        else:
            LOGGED_IN=True
            print "LOGGED_IN", LOGGED_IN
            return render_template("user_page.html", user=u)

@app.route("/user", methods=['GET','POST'])
def users():
    user_id = request.args.get("id")
    user=model.session.query(model.User).get(user_id)
    return render_template("user_page.html",user=user)#,ratings=ratings)

@app.route("/movie_page")
def movie():
    print "LOGGED_IN", LOGGED_IN
    movie_title = request.args.get("title")
    movie=model.session.query(model.Movie).filter_by(movie_title=movie_title).one()

    sum_of_ratings = 0

    for i in movie.rating:
        sum_of_ratings += i.rating

    avg_rating = sum_of_ratings/len(movie.rating)
    return render_template("movie_page.html", avg_rating=avg_rating,movie=movie_title)

@app.route("/add_rating")
def add_rating():
    print "LOGGED_IN" , LOGGED_IN
    if LOGGED_IN==True:
        r=model.Rating()
        r.movie.movie_title = request.args.get("movie_title")
        r.rating = request.args.get("rating")
        r.user.id = USER_ID
        print "user id is: ", r.user.id
        model.session.add(r)
        model.session.commit()
        return redirect("/user")

    else:
        print "not logged in!!!"
        return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)