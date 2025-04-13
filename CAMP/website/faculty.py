from website import mysql  # Import MySQL connection instance
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask import jsonify

from .models import Faculty

faculty = Blueprint('faculty', __name__)

# @faculty.route('/faculty/dashboard', methods=['GET'])
# def faculty_dashboard():
#     """Faculty Dashboard"""

#     faculty_id = session.get('faculty_id')  

#     students = Faculty.get_students_by_faculty(faculty_id)

#     return render_template('Faculty/facultyDashboard.html', students=students)


@faculty.route('/faculty/dashboard', methods=['GET', 'POST'])
def faculty_dashboard():
    """Faculty Dashboard - Show Students Enrolled in the Faculty's Assigned Course"""

    faculty_id = session.get('faculty_id') 

    # Fetch students and the assigned course name
    students, course_name = Faculty.get_students_by_faculty(faculty_id)

    return render_template('Faculty/facultyDashboard.html', students=students, course_name=course_name)

@faculty.route('/faculty/student_details/<int:student_id>', methods=['GET', 'POST'])
def student_details(student_id):
    """Fetch student details for the popup."""
    
    student = Faculty.get_student_popup(student_id)

    if student:
        student_data = {
            "stu_id": student[0],
            "stu_first_name": student[1],
            "stu_middle_name": student[2],
            "stu_last_name": student[3],
            "profile_picture": student[4] if student[4] else None,
            "stu_phone_number": student[5],
            "stu_emailadd": student[6],
            "stu_address": student[7],
        }
        return jsonify(student_data)
    
    return jsonify({"error": "Student not found"}), 404


@faculty.route('/faculty/search_students', methods=['POST'])
def search_students():
    """Search for students by name within the faculty's assigned course or clear the search."""
    faculty_id = session.get('faculty_id')  

    # Always retrieve the course name
    _, course_name = Faculty.get_students_by_faculty(faculty_id)

    if request.form.get('clear_search'):
        
        students, _ = Faculty.get_students_by_faculty(faculty_id)
        return render_template('Faculty/facultyDashboard.html', students=students, search_query='', course_name=course_name)
    
    search_query = request.form.get('search_query', '')  
    students = Faculty.search_student(search_query, faculty_id)  
    return render_template('Faculty/facultyDashboard.html', students=students, search_query=search_query, course_name=course_name)

@faculty.route('/faculty/add_grades', methods=['GET'])
def add_grades():
    """Render the Add Grades page."""
    faculty_id = session.get('faculty_id')  
    students, course_name = Faculty.get_students_by_faculty(faculty_id)
    course_id = Faculty.get_course_id_by_faculty(faculty_id)  # Course ID

    if not course_id:
        flash('No course assigned to you.', 'danger')
        return redirect(url_for('faculty.faculty_dashboard'))

    return render_template(
        'Faculty/facultyAddGrades.html',
        students=students,
        course_name=course_name,
        course_id=course_id
    )

@faculty.route('/faculty/submit_grades', methods=['POST'])
def submit_grades():
    """Submit, update, or delete grades for a student and update the database."""
    student_id = request.form.get('student_id')
    course_id = request.form.get('course_id')
    written_works = request.form.get('written_works')
    final_project = request.form.get('final_project')
    exams = request.form.get('exams')
    action = request.form.get('action')

    try:
        written_works = int(written_works) if written_works else 0
        final_project = int(final_project) if final_project else 0
        exams = int(exams) if exams else 0
    except ValueError:
        flash('Scores must be valid integers.', 'danger')
        return redirect(url_for('faculty.add_grades'))

    if written_works == 0 and final_project == 0 and exams == 0:
        try:
            Faculty.delete_scores(student_id, course_id)
            flash('Scores deleted successfully!', 'success')
        except Exception as e:
            flash(f'An error occurred while deleting scores: {str(e)}', 'danger')
        return redirect(url_for('faculty.add_grades'))

    raw_grade = ((written_works / 200) * 50) + ((final_project / 100) * 30) + ((exams / 150) * 20)

    def calculate_final_grade(raw_grade):
        if raw_grade >= 98:
            return 1.00
        elif raw_grade >= 91:
            return 1.25
        elif raw_grade >= 85:
            return 1.50
        elif raw_grade >= 79:
            return 1.75
        elif raw_grade >= 73:
            return 2.00
        elif raw_grade >= 67:
            return 2.25
        elif raw_grade >= 61:
            return 2.50
        elif raw_grade >= 55:
            return 2.75
        elif raw_grade >= 50:
            return 3.00
        else:
            return 5.00

    final_grade = calculate_final_grade(raw_grade)

    try:
        if action == 'submit':
            Faculty.insert_scores(student_id, course_id, written_works, final_project, exams)
        elif action == 'update':
            Faculty.update_scores(student_id, course_id, written_works, final_project, exams)

        Faculty.update_grades(student_id, course_id, raw_grade, final_grade)
        flash('Grades updated successfully!' if action == 'update' else 'Grades submitted successfully!', 'success')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')

    return redirect(url_for('faculty.add_grades'))

@faculty.route('faculty/evaluation', methods=['GET', 'POST'])
def show_evaluations():
    """Show the student evaluation form."""
    faculty_id = session.get('faculty_id') 
    evaluations = Faculty.show_evaluations(faculty_id)
    evaluations_rating = Faculty.eval_rating(faculty_id)

    # Provide a default value if no evaluations exist
    if not evaluations_rating:
        evaluations_rating = (faculty_id, 0)  # Default to 0 rating

    total_evaluations = Faculty.total_evaluations(faculty_id)  # Get total evaluations
    rating_frequencies = Faculty.get_rating_frequencies(faculty_id)  # Get rating frequencies

    # print("DEBUG: Rating Frequencies:", rating_frequencies)  

    return render_template(
        'Faculty/facultyEvaluation.html',
        evaluations=evaluations,
        evaluations_rating=evaluations_rating,
        total_evaluations=total_evaluations,
        rating_frequencies=rating_frequencies
    )

@faculty.route('/faculty/delete_evaluation/<int:evaluation_id>', methods=['POST'])
def delete_evaluation(evaluation_id):
    """Delete an evaluation by its ID."""
    try:
        Faculty.delete_evaluation(evaluation_id)  
        flash('Evaluation deleted successfully!', 'success')
    except Exception as e:
        flash(f'An error occurred while deleting the evaluation: {str(e)}', 'danger')
    return redirect(url_for('faculty.show_evaluations'))