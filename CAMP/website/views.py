from flask import Blueprint, render_template, session, redirect, url_for  # Import required Flask modules
from flask import send_from_directory
import os

# Initialize a Flask blueprint for managing routes
views = Blueprint('views', __name__)

@views.route('/profile_pictures/<filename>')
def profile_pictures(filename):
    shared_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../shared_assets/profile_pictures'))
    return send_from_directory(shared_folder, filename)
@views.route('/')
def home():
    return render_template("home.html")
