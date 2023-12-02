from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# create a Flask instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "a really good secret key that is super duper secret"


# Create a form class
class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

# create a route decorator
@app.route('/')

#def index():
 #   return "<h1>Hello World!</h1>"

def index():
    first_name = "John"
    stuff = "This is bold text"
    favorite_pizza = ["Pepperoni", "Cheese", "Mushrooms", 41]
    return render_template('index.html',
                           first_name=first_name,
                           stuff=stuff,
                           favorite_pizza=favorite_pizza)


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

