from website import mysql  # Import MySQL connection instance
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime



from .models import Student  # Import the Student model


# Create a Blueprint instance for admin routes
student = Blueprint('student', __name__)

# Define the student dashboard route
@student.route('/student/dashboard')
def student_dashboard():
    if 'student_id' not in session:  # Ensure the student is logged in
        return redirect(url_for('auth.loginstudent'))

    # Fetch the full student details by ID
    student_id = session['student_id']
    full_student_details = Student.student_profile(student_id)  # Fetch all student details

    # Pass all retrieved details to the template
    return render_template(
        "Student/studentDashboard.html",
        student_name=session['student_name'],
        student_details={
            'first_name': full_student_details[0],
            'middle_name': full_student_details[1],
            'last_name': full_student_details[2],
            'birthdate': full_student_details[3],
            'gender': full_student_details[4],
            'cellphone_no': full_student_details[5],
            'email': full_student_details[6],
            'address': full_student_details[7],
            'username': full_student_details[8],
            'password': full_student_details[9],
            'lrn': full_student_details[10],
            'citizenship': full_student_details[11],
            'religion': full_student_details[12],
        }
    )


@student.route('/student/upload_picture/<int:student_id>', methods=['POST'])
def upload_student_picture(student_id):
    """Handle profile picture upload for students."""

    # Base path of the current directory of the `website` package
    base_path = os.path.dirname(os.path.realpath(__file__))  # Get the path to 'website'
    static_path = os.path.join(base_path, 'static')  # Define the absolute path to the `static` folder
    upload_folder = os.path.join(static_path,
                                 'student_pictures')  # Ensure the uploads folder is under the correct static folder

    # Allowed file extensions for upload
    allowed_extensions = {'jpg', 'jpeg', 'png'}

    # Retrieve the uploaded file
    file = request.files.get('profile_picture')

    # Check if a file is provided
    if not file or file.filename == '':
        flash('No file selected!', category='error')
        return redirect(url_for('student.student_dashboard'))

    # Validate file type
    if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        flash('Invalid file type. Only JPG, JPEG, and PNG are allowed.', category='error')
        return redirect(url_for('student.student_dashboard'))

    # Secure the file name and define the upload path
    filename = secure_filename(f"student_{student_id}.jpg")  # Save as student_<id>.jpg
    os.makedirs(upload_folder, exist_ok=True)  # Create the folder if it doesn’t exist

    # Save the file to the uploads folder inside the static folder
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    # Relative path to be stored in the database
    relative_file_path = f"student_pictures/{filename}"  # Use a relative path for database storage

    # Attempt to update the student's profile picture in the database
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE student_tbl
            SET profile_picture = %s
            WHERE stu_id = %s
        """, (relative_file_path, student_id))
        mysql.connection.commit()  # Commit the changes

        # Update the session to reflect the new profile picture
        session['student_pictures'] = relative_file_path

        flash('Profile picture updated successfully!', category='success')
    except Exception as e:
        flash(f"An error occurred while updating the profile picture: {e}", category='error')
    finally:
        cur.close()  # Close the cursor

    # Redirect to the student's dashboard
    return redirect(url_for('student.student_dashboard'))  # Ensure this route exists

# Define route for updating student details from the student dashboard
@student.route('/student/update_details/<int:student_id>', methods=['POST'])
def update_student_details(student_id):
    """Handle updating the student's details from their dashboard."""
    if 'student_id' not in session or session['student_id'] != student_id:
        return redirect(url_for('auth.loginstudent'))  # Ensure the student is authenticated

    # Retrieve form data for updating
    first_name = request.form.get('first_name')
    middle_name = request.form.get('middle_name')
    last_name = request.form.get('last_name')
    username = request.form.get('username')
    password = request.form.get('password')
    birthdate = request.form.get('birthdate')
    phone_number = request.form.get('cellphone_no')
    email = request.form.get('email')
    address = request.form.get('address')
    lrn = request.form.get('lrn')
    citizenship = request.form.get('citizenship')
    religion = request.form.get('religion')
    gender = request.form.get('gender')

    # Validate required fields
    if not all([first_name, last_name, username, birthdate, phone_number, email]):
        flash("All required fields must be filled!", category="error")
        return redirect(url_for('student.student_dashboard'))  # Return to the dashboard in case of error

    # Update the student information in the database
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE student_tbl
        SET stu_first_name = %s,
            stu_middle_name = %s,
            stu_last_name = %s,
            stu_username = %s,
            stu_password = %s,
            stu_birthdate = %s,
            stu_phone_number = %s,
            stu_emailadd = %s,
            stu_address = %s,
            stu_lrn = %s,
            stu_citizenship = %s,
            stu_religion = %s,
            stu_sex = %s
        WHERE stu_id = %s
    """, (
        first_name, middle_name, last_name, username, password, birthdate, phone_number, email, address, lrn, citizenship,
        religion,
        gender, student_id))
    mysql.connection.commit()
    cur.close()

    # Update session with the new name (reflect changes across pages)
    session['student_name'] = f"{first_name} {middle_name} {last_name}"

    # Flash success message and redirect to the student dashboard
    flash("Your information has been updated successfully!", category="success")
    return redirect(url_for('student.student_dashboard'))  # Redirect back to the student dashboard


# Define the route for courses
@student.route('/student/courses')
def student_courses():
    if 'student_id' not in session:  # Ensure student is logged in
        return redirect(url_for('auth.loginstudent'))  # Redirect to login if session is missing

    student_id = session['student_id']  # Retrieve student ID from the session
    courses = Student.get_enrolled_courses(student_id)  # Fetch the enrolled courses

    print("Courses:", courses)


    return render_template("Student/studentViewCourses.html", courses=courses)


@student.route('/student/apply_course', methods=['GET', 'POST'])
def apply_course():
    if 'student_id' not in session:  # Ensure student is logged in
        return redirect(url_for('auth.loginstudent'))

    student_id = session['student_id']  # Get logged-in student ID

    if request.method == 'POST':
        # Retrieve the list of selected courses from the form
        selected_course_ids = request.form.getlist('selected_course_ids')  # Get a list of selected course IDs

        if not selected_course_ids:
            flash("No courses selected.", category="error")
            return redirect(url_for('student.apply_course'))

        
        selected_course_ids = [int(course_id) for course_id in selected_course_ids]

  
        success, message = Student.apply_for_courses(student_id, selected_course_ids)

        if success:
            flash(message, category="success")
        else:
            flash(message, category="error")

        return redirect(url_for('student.student_courses'))

    # Fetch available courses and enrolled courses via the Student model
    courses = Student.get_available_courses()  # All courses
    enrolled_courses = [course['course_id'] for course in
                        Student.get_enrolled_courses(student_id)]  # IDs of enrolled courses
    enrolled_count = len(enrolled_courses)  # Get count of already enrolled courses

    # Pass enrolled_courses, courses, and enrolled_count to the template
    return render_template("Student/studentApplyCourse.html", 
                           courses=courses,
                           enrolled_courses=enrolled_courses,
                           enrolled_count=enrolled_count
                           )


# from datetime import datetime

@student.route('/student/view_schedule')
def student_view_schedule():
    """Fetch and display the student's schedule grouped by time slots and days."""
    student_id = session.get("student_id")

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT day_of_week, course_name, 
               TIME_FORMAT(time_start, '%%h:%%i %%p') as time_start, 
               TIME_FORMAT(time_end, '%%h:%%i %%p') as time_end
        FROM student_schedule
        WHERE student_id = %s
    """, (student_id,))

    schedule_data = cur.fetchall()
    cur.close()

    # Create ordered structure {time: {day: course_name}}
    schedule_by_time = {}
    unique_days = set()

    for row in schedule_data:
        day, course_name, time_start, time_end = row
        time_range = f"{time_start} - {time_end}"

        if time_range not in schedule_by_time:
            schedule_by_time[time_range] = {}

        schedule_by_time[time_range][day] = course_name
        unique_days.add(day)

    # Convert time strings to datetime objects for proper AM/PM sorting
    sorted_schedule_by_time = dict(sorted(
        schedule_by_time.items(),
        key=lambda x: datetime.strptime(x[0].split(" - ")[0], "%I:%M %p")
    ))

    return render_template(
        'Student/studentViewSchedule.html',
        schedule_by_time=sorted_schedule_by_time,
        unique_days=sorted(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    )

@student.route('/student/evaluate_faculty', methods=['POST'])
def evaluate_faculty():
    """
    Handles the submission of faculty evaluations by students.
    """
    try:
        # Get the student ID from the session
        student_id = session.get('student_id')  # Ensure student_id is stored in session
        if not student_id:
            return jsonify({'error': 'Unauthorized access. Please log in.'}), 401

        # Get form data
        professor_id = request.form.get('professorId')
        rating = int(request.form.get('rating'))
        comment = request.form.get('comment')

    
        # print("Student ID:", student_id)
        # print("Professor ID:", professor_id)
        # print("Rating:", rating)
        # print("Comment:", comment)
        # print("Anonymous:", anonymous)

        # Validate inputs
        if not professor_id or not rating or not comment:
            return jsonify({'error': 'All fields are required.'}), 400

        # Call the database logic to add the evaluation
        success, message = Student.add_evaluation(student_id, professor_id, rating, comment)

        if success:
            return jsonify({'message': message}), 200
        else:
            return jsonify({'error': message}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500





