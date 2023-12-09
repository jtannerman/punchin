from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash



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
migrate = Migrate(app, db)

#Create data Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    fav_color = db.Column(db.String(120))
    punches = db.relationship('Punches', backref='users', lazy=True)
    # Do some password stuff
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute!")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


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
        return '<Punches %r>' % self.id

# Create a form class
class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(),Email()])
    fav_color = StringField("Favorite Color")
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
            user = Users(name=form.name.data, email=form.email.data, fav_color=form.fav_color.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.fav_color.data = ''
        flash("User added successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",
                           form=form,
                           name=name,
                           our_users=our_users)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    name = None
    form = UserForm()
    user_to_update = Users.query.get_or_404(id)
    our_users = Users.query.order_by(Users.date_added)
    if request.method == "POST":
        user_to_update.name = request.form['name']
        user_to_update.email = request.form['email']
        user_to_update.fav_color = request.form['fav_color']
        try:
            db.session.commit()
            flash("User updated!")
            return render_template("update.html", form=form, user_to_update=user_to_update, id=id)
        except:
            flash("Something went wrong!")
            return render_template("update.html", form=form, user_to_update=user_to_update, id=id)
    else:
        return render_template("update.html", form=form, user_to_update=user_to_update, id=id)

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted!")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html",
                           form=form,
                           name=name,
                           our_users=our_users)
    except:
        flash("Something went wrong deleting the user.")
        return render_template("add_user.html",
                           form=form,
                           name=name,
                           our_users=our_users)


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

