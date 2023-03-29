from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import smtplib
import os
import email_validator

MY_EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

Bootstrap(app)


# Database
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    overview = db.Column(db.String(1000), nullable=False)
    tools = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(100), nullable=False)


# Form
class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Submit")


def send_email():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=MY_EMAIL,
                            msg=f"Subject:New Message\n\n"
                                f"Name: {name}\n"
                                f"Email address: {email}\n"
                                f"Message: {message}")


db.create_all()
projects = Project.query.all()


@app.route("/", methods=['GET', 'POST'])
def home():
    form = ContactForm()
    if request.method == "POST":
        send_email()
        return redirect(url_for('home'))

    return render_template("index.html", all_projects=projects, form=form)


@app.route("/project/<title>", methods=['GET', 'POST'])
def get_project(title):
    form = ContactForm()
    if request.method == "POST":
        send_email()
        return redirect(url_for('home'))

    clicked_project = None
    for proj in projects:
        if proj.title == title:
            clicked_project = proj
    return render_template("project.html", project=clicked_project, form=form)


if __name__ == '__main__':
    app.run(debug=True)