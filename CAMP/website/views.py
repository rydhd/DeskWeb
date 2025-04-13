from flask import Blueprint, render_template, session, redirect, url_for  # Import required Flask modules

# Initialize a Flask blueprint for managing routes
views = Blueprint('views', __name__)



@views.route('/')
def home():
    return render_template("home.html")
