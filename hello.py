from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



# create a Flask instance
app = Flask(__name__)
# Old SQLite DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///punchin.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///punchin1.db'
# MySQL DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:devpass123@localhost/punchin'
app.config['SECRET_KEY'] = "a really good secret key that is super duper secret"
# Define Database db
db = SQLAlchemy(app)
app.app_context().push()

#Create data Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    punches = db.relationship('Punches', backref='users', lazy=True)

    # Create a String
    def __repr__(self):
        return '<Users %r>' % self.name


class Punches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum("IN", "OUT", "LIN", "LOUT", name="punch_type"))
    date_and_time = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


    # Create a String
    def __repr__(self):
        return '<Punches %r>' % self.user_id

# Create a form class
class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(),Email()])
    submit = SubmitField("Submit")


# create a route decorator
@app.route('/')

#def index():
 #   return "<h1>Hello World!</h1>"

def index():
    first_name = "Nick"
    stuff = "This is bold text"
    favorite_pizza = ["Pepperoni", "Cheese", "Mushrooms", 41]
    return render_template('index.html',
                           first_name=first_name,
                           stuff=stuff,
                           favorite_pizza=favorite_pizza)


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User added successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",
                           form=form,
                           name=name,
                           our_users=our_users)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    user_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        user_to_update.name = request.form['name']
        user_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash("User updated!")
            return render_template("update.html", form=form, user_to_update=user_to_update)
        except:
            flash("Something went wrong!")
            return render_template("update.html", form=form, user_to_update=user_to_update)
    else:
        return render_template("update.html", form=form, user_to_update=user_to_update)



@app.route('/user/<name>')

def user(name):
    return render_template('user.html', name=name)

@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    #Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully!")

    return render_template('name.html',
                           name = name,
                           form = form)

# Create custom error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

