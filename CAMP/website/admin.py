from website import mysql  # Import MySQL connection instance
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from functools import wraps


from .models import Student  # Import the Student model
from .models import Admin  # Import the relevant methods/models if needed
from .models import Faculty  # Import the relevant methods/models if needed

# Create a Blueprint instance for admin routes
admin = Blueprint('admin', __name__)

# Custom decorator to restrict access to admin-only pages
def admin_login_required(f):
    @wraps(f)  # Ensures function metadata remains intact
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:  # Check if admin is logged in
            return redirect(url_for('auth.loginadmin'))  # Redirect to admin login page if not authenticated
        return f(*args, **kwargs)  # Proceed to the original function if authenticated

    return decorated_function

# Define the admin dashboard route, restricted to logged-in admins
@admin.route('/admin/dashboard', methods=['GET', 'POST'])
@admin_login_required
def admin_dashboard():
    """Admin dashboard route, now includes the student and faculty management sections."""
    students = []
    search_query = request.form.get('search_query')  # Get search input from form

    if search_query:  # If searching, fetch only matching students
        students = Student.get_all_students(search_query)
    else:  # If no search, show all students
        students = Student.get_all_students()

    # Get the student counts
    student_counts = Student.get_student_counts()

    # Get the faculty count
    faculty_count = Faculty.get_faculty_count()

    return render_template(
        "Admin/adminDashboard.html",
        students=students,
        search_query=search_query,
        student_counts=student_counts,  # Pass student counts to the template
        faculty_count=faculty_count  # Pass faculty count to the template
    )

# Route to add a new student
@admin.route('/admin/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':  # Handle form submission
        # Retrieve student details from the form
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        birthdate = request.form.get('birthdate')
        sex = request.form.get('sex')
        username = request.form.get('username')
        password = request.form.get('password')
        phone_number = request.form.get('phone_number')
        lrn = request.form.get('lrn')
        citizenship = request.form.get('citizenship')
        emailadd = request.form.get('emailadd')
        religion = request.form.get('religion')
        address = request.form.get('address')

        # Ensure all required fields are filled
        if not all([first_name, last_name, birthdate, sex, username, password, phone_number, lrn, emailadd]):
            flash('Please fill in all required fields!', category='error')  # Display error message
            return redirect(url_for('admin.admin_dashboard'))  # Redirect back to form

        # Call function to add student in database
        success = Student.add_student(username, password, first_name, middle_name, last_name, birthdate, sex, phone_number, lrn, citizenship, emailadd, religion, address)

        if not success:
            flash('Username, Password, Phone Number, LRN, or Email already exists. Please use different values.', category='error')  # Display error message
            return redirect(url_for('admin.admin_dashboard'))  # Redirect back to form

        flash('Student added successfully!', category='success')  # Display success message
        return redirect(url_for('admin.admin_dashboard'))  # Redirect after successful insertion

    return render_template("Admin/adminAddStudent.html")  # Render student addition form

@admin.route('/admin/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    """Route to delete a student."""
    Student.delete_student(student_id)
    flash('Student deleted successfully!', category='success')
    return redirect(url_for('admin.admin_dashboard'))  # Redirect to the admin dashboard

@admin.route('/admin/courses', methods=['GET', 'POST'])
def view_courses():
    # Retrieve all courses to display
    courses = Admin.get_all_courses()

    # Retrieve professors without assigned courses for the modal
    available_professors = Faculty.get_faculty_without_courses()

    if request.method == 'POST':
        # Extract inputs from the form
        course_name = request.form.get('course_name')
        professor_id = request.form.get('professor')
        day = request.form.get('day')  # Day from dropdown
        time_range = request.form.get('time')  # Time range from dropdown

        # Split start and end times from the time range
        time_start, time_end = time_range.split('-')

        # Validate if the schedule is already taken
        if Admin.is_schedule_taken(day, time_start, time_end):
            return jsonify({
                "success": False,
                "message": f"The selected schedule ({day}, {time_start} - {time_end}) is already in use. Please choose another one."
            })

        # Proceed to add the course if schedule is valid
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO course_tbl (cou_name, fac_id_fk, sch_id_fk)
                VALUES (%s, %s,
                    (SELECT sch_id FROM schedule_tbl WHERE day_of_week = %s AND time_start = %s AND time_end = %s)
                )
            """, (course_name, professor_id, day, time_start, time_end))
            mysql.connection.commit()  # Save changes
            cur.close()

            return jsonify({
                "success": True,
                "message": "Course has been added successfully!"
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "message": "An error occurred while adding the course. Please try again."
            })

    # Render the view courses template and pass data
    return render_template('Admin/adminViewCourses.html', courses=courses, professors=available_professors)



@admin.route('/admin/faculty', methods=['GET', 'POST'])
def view_faculty():
   faculty_details = Admin.get_all_faculty_members()  # Use the helper method to retrieve faculty data
   return render_template('Admin/adminViewFaculty.html', faculty_details=faculty_details)

@admin.route('/admin/add_faculty', methods=['POST'])
def add_faculty():
    if request.method == 'POST':
        # Get faculty details from form
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        username = request.form.get('username')
        password = request.form.get('password')

        # Ensure required fields are not empty
        if not all([first_name, last_name, email, phone_number, username, password]):
            flash("Please fill all required fields!", category='error')
            return redirect(url_for('admin.view_faculty'))

        # Add faculty in the database
        success = Faculty.add_faculty(username, password, first_name, middle_name, last_name, email, phone_number)

        if not success:
            flash("Faculty member with given email, username, or phone number already exists.", category='error')
            return redirect(url_for('admin.view_faculty'))

        flash("Faculty member added successfully!", category='success')
        return redirect(url_for('admin.view_faculty'))
    
    

# @admin.route('/admin/add_course', methods=['GET', 'POST'])
# def add_course():
#     # Retrieve professors without assigned courses
#     available_professors = Faculty.get_faculty_without_courses()

#     if request.method == 'POST':
#         # Extract inputs from the form
#         course_name = request.form.get('course_name')
#         professor_id = request.form.get('professor')
#         day = request.form.get('day')  # Day from dropdown
#         time_range = request.form.get('time')  # Time range from dropdown

#         # Split start and end times from the time range
#         time_start, time_end = time_range.split('-')

#         # Validate if the schedule is already taken
#         if Admin.is_schedule_taken(day, time_start, time_end):
#             return jsonify({
#                 "success": False,
#                 "message": f"The selected schedule ({day}, {time_start} - {time_end}) is already in use. Please choose another one."
#             })

#         # Proceed to add the course if schedule is valid
#         try:
#             cur = mysql.connection.cursor()
#             cur.execute("""
#                 INSERT INTO course_tbl (cou_name, fac_id_fk, sch_id_fk)
#                 VALUES (%s, %s,
#                     (SELECT sch_id FROM schedule_tbl WHERE day_of_week = %s AND time_start = %s AND time_end = %s)
#                 )
#             """, (course_name, professor_id, day, time_start, time_end))
#             mysql.connection.commit()  # Save changes
#             cur.close()

#             return jsonify({
#                 "success": True,
#                 "message": "Course has been added successfully!"
#             })
#         except Exception as e:
#             return jsonify({
#                 "success": False,
#                 "message": "An error occurred while adding the course. Please try again."
#             })

#     # Render the add course template and pass data for GET requests
#     return render_template('Admin/adminAddCourse.html', professors=available_professors)

@admin.route('/admin/view_student/<int:student_id>', methods=['GET'])
def view_student(student_id):
    """Fetch and display detailed information about a specific student."""
    student = Student.get_student_by_id(student_id)  # Fetch student details from the Student model

    if not student:
        # Show error if the student is not found in the database
        flash(f"Student with ID {student_id} not found.", category="error")
        return redirect(url_for('admin.admin_dashboard'))  # Redirect back to the dashboard

    # Render the student profile page with student details
    return render_template("Admin/adminViewStudent.html", student=student)

@admin.route('/admin/upload_student_picture/<int:student_id>', methods=['GET', 'POST'])
def upload_student_picture(student_id):
    """Handle the uploading and saving of a student's profile picture."""
    from werkzeug.utils import secure_filename #Pang-secure at handle ng file names
    import os #In-import 'yung OS para ma-handle 'yung local file directory

    # Sinetup 'yung directory ng project at paglalagyan ng pictur
    base_path = os.path.dirname(os.path.realpath(__file__))  # Get the path to 'website'
    static_path = os.path.join(base_path, 'static')  # Define the absolute path to the `static` folder
    upload_folder = os.path.join(static_path, 'uploads')  # Ensure the uploads folder is under the correct static folder

    # Check if a file is uploaded
    if 'profile_picture' not in request.files or request.files['profile_picture'].filename == '':
        flash('No file selected!', category='error')
        return redirect(url_for('admin.view_student', student_id=student_id))

    # Retrieve the file and process it
    file = request.files['profile_picture']
    allowed_extensions = {'jpg', 'jpeg', 'png'}  # Allowed file types (extensions)
 
    # Pang-validate lang kung tamang file format ang pinili
    if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        flash("Invalid file type. Only JPG, JPEG, and PNG are allowed.", category="error")
        return redirect(url_for('admin.view_student', student_id=student_id))

    # Secure the file name and define upload path
    filename = secure_filename(f"student_{student_id}.jpg")  # Ni-rename 'yung piniling picture as student_<id>.jpg
    os.makedirs(upload_folder, exist_ok=True)  # Gagawa ng folder na paglalagyan (incase kung wala pang nagagawa)

    # Save the file to the uploads folder inside the static folder
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    # Update the student record in the database
    relative_file_path = f"uploads/{filename}"  # Use a relative path for database storage
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE student_tbl
        SET profile_picture = %s
        WHERE stu_id = %s
    """, (relative_file_path, student_id))  # Store relative path in the database
    mysql.connection.commit()  # Commit the changes
    cur.close()

    flash("Profile picture uploaded successfully!", category="success")
    return redirect(url_for('admin.view_student', student_id=student_id))

@admin.route('/admin/update_student/<int:student_id>', methods=['POST'])
def update_student(student_id):
    """Handle updating the student's information."""
    # Retrieve form data for updating
    username = request.form.get('username')
    password = request.form.get('password')
    birthdate = request.form.get('birthdate')
    phone_number = request.form.get('phone_number')
    email = request.form.get('email')
    address = request.form.get('address')
    lrn = request.form.get('lrn')
    citizenship = request.form.get('citizenship')
    religion = request.form.get('religion')
    sex = request.form.get('sex')

    # Validate updated data (if required, not mandatory)
    if not all([username, birthdate, phone_number, email]):
        flash("All required fields must be filled!", category="error")
        return redirect(url_for('admin.view_student', student_id=student_id))

    # Update the student's information in the database
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE student_tbl
        SET stu_username = %s,
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
    """, (username, password,birthdate, phone_number, email, address, lrn, citizenship, religion, sex, student_id))
    mysql.connection.commit()
    cur.close()

    # Flash and redirect user
    flash("Student information updated successfully!", category="success")
    return redirect(url_for('admin.view_student', student_id=student_id))

@admin.route('/admin/view_student_list/<int:course_id>', methods=['GET', 'POST'])
def view_student_list(course_id):
    """Fetch and display the list of students enrolled in a specific course."""
    course_info = Admin.get_course_name_with_faculty(course_id)  # Fetch course info

    # if not course_info:  # If course does not exist
    #     flash("No students found because this faculty is not assigned to a course yet.", "warning")
    #     return redirect(url_for('admin.view_faculty_list'))  # Redirect to faculty list page

    students = Student.get_student_list_of_course(course_id)  # Get students

    return render_template('Admin/adminViewStudentList.html', 
                           course_id=course_id, 
                           course_name=course_info.get('course_name', 'N/A'), 
                           faculty_name=course_info.get('faculty_name', 'N/A'), 
                           students=students)

@admin.route('/admin/remove_student/<int:course_id>/<int:student_id>', methods=['POST'])
def remove_student(course_id, student_id):
    """Remove a student from a specific course."""
    Student.remove_student_from_course(course_id, student_id)
    return redirect(url_for('admin.view_student_list', course_id=course_id))


