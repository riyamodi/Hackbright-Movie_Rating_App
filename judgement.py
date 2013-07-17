from flask import Flask, render_template, redirect, request, flash
import model

app = Flask(__name__)

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
        print "email is: ", u.email
        u.password=request.form["password"]
        print "password is: ", u.password
        u.zipcode=request.form["zipcode"]
        print "zipcode is: ", u.zipcode
        u.occupation=request.form["occupation"]
        print "occupation is: ", u.occupation
        u.age=request.form["age"]
        print "age is: ", u.age
        u.gender=request.form["gender"]
        print "gender is: ", u.gender
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
            print "Email address not registered. Check spelling or Sign Up"
            #find a way to display that message to the screen
            #flash(u'Email address not registered. Check spelling or Sign Up')
            return redirect("/")
        else:
             return render_template("user_page.html", user=u)

# @app.route("/user")
# def users():
#     return render_template("user_page.html")


if __name__ == "__main__":
    app.run(debug=True)