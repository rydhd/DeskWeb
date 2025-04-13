from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import Admin, Student, Faculty
from datetime import datetime


# Create a Blueprint instance for authentication routes
auth = Blueprint('auth', __name__)

# Student login route
@auth.route('/studentlogin', methods=['GET', 'POST'])
def loginstudent():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        student = Student.verify_student(username, password)

        if student:
            full_student_details = Student.get_student_by_id(student[0])

            # Display student details
            session['student_id'] = full_student_details[0]
            session['student_name'] = full_student_details[1]
            session['student_username'] = full_student_details[2]
            session['student_picture'] = full_student_details[12] if full_student_details[
                12] else 'profile_pictures/default-profile.jpg'

            flash('Logged in successfully!', category='success')
            return redirect(url_for('student.student_dashboard'))
        else:
            flash('Invalid username or password.', category='error')

    return render_template("Student/studentLogin.html")

# Admin login route
@auth.route('/adminlogin', methods=['GET', 'POST'])
def loginadmin():
    if request.method == 'POST':  # Handle form submission
        username = request.form.get('username')  # Get username from form
        password = request.form.get('password')  # Get password from form

        admin = Admin.get_admin_by_username(username)  # Retrieve admin details from the database

        if admin and admin[2] == password:  # Verify password
            session['admin_id'] = admin[0]  # Store admin ID in session
            session['admin_username'] = admin[1]  # Store admin username in session
            flash('Logged in successfully!', category='success')  # Display success message
            return redirect(url_for('admin.admin_dashboard'))  # Redirect to admin dashboard
        else:
            flash('Invalid username or password.', category='error')  # Display error message

    return render_template("Admin/adminLogin.html")  # Render admin login page

@auth.route('/facultylogin', methods=['GET', 'POST'])
def facultylogin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        faculty = Faculty.verify_faculty(username, password)

        if faculty and faculty[1] == username and faculty[2] == password:
            session['faculty_id'] = faculty[0] 
            session['faculty_username'] = faculty[1] 
            session['faculty_name'] = faculty[3]  
            flash('Logged in successfully!', category='success')
            return redirect(url_for('faculty.faculty_dashboard'))
        else:
            flash('Invalid username or password.', category='error')

    return render_template("Faculty/facultyLogin.html")


# Logout route
@auth.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('views.home'))  # Redirect to homepage

# auth.py handles authentication for admins and students, including login and logout functionality.