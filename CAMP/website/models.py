from website import mysql  # Import MySQL connection instance
from MySQLdb.cursors import DictCursor 

# Admin model class for managing admin-related database queries
class Admin:
    @staticmethod
    def get_admin_by_username(username):
        cur = mysql.connection.cursor()  # Create a cursor to execute SQL queries
        cur.execute("""
            SELECT 
                adm_id, adm_username, adm_password
            FROM admin_tbl 
            WHERE adm_username = %s
        """, (username,))  # Fetch admin details by username
        admin = cur.fetchone()  # Retrieve the first result
        cur.close()  # Close the cursor
        return admin  # Return admin details or None if not found

    @staticmethod
    def get_all_courses():
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT
                course_name,    
                day_of_week, 
                time_start, 
                time_end,
                concat(fac_first_name, ' ', IFNULL(fac_middle_name, ''), ' ', fac_last_name) AS faculty_name
            FROM
                course_schedule_faculty
            WHERE
                course_name IS NOT NULL;  -- Only include courses with schedule
        """)
        courses = cur.fetchall()
        cur.close()
        return courses
        

    @staticmethod
    def get_all_faculty_members():
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT
            f.fac_id,
            f.fac_full_name,
            c.cou_name AS course_name
            FROM
                faculty_tbl AS f
            LEFT JOIN
                course_tbl AS c
            ON
                f.fac_id = c.fac_id_fk
        """)
        faculty_members = cur.fetchall()
        cur.close()
        return faculty_members

    @staticmethod
    def is_schedule_taken(day, time_start, time_end):
        """Check if a day and time combination is already in use."""
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT 
                c.cou_name, s.day_of_week, s.time_start, s.time_end
            FROM 
                schedule_tbl AS s
            INNER JOIN 
                course_tbl AS c ON s.sch_id = c.sch_id_fk
            WHERE 
                s.day_of_week = %s
                AND s.time_start = %s
                AND s.time_end = %s
        """, (day, time_start, time_end))
        result = cur.fetchone()
        # print(f"DEBUG: Checking schedule for {day}, {time_start}-{time_end}: {result}") 
        cur.close()
        return result is not None
    
    @staticmethod
    def get_course_name_with_faculty(course_id):
        """Retrieve course name by course ID"""
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT 
                c. cou_name,
                CONCAT(f.fac_first_name, ' ', IFNULL(f.fac_middle_name, ''), ' ', f.fac_last_name) AS faculty_name
            FROM 
                course_tbl AS c
            LEFT JOIN
                faculty_tbl AS f ON c.fac_id_fk = f.fac_id
            WHERE
                cou_id = %s
        """, (course_id,))
        course = cur.fetchone()
        cur.close()
        return {
            "course_name": course[0],
            "faculty_name": course[1]
        }


# Student model class for managing student-related database operations
class Student:
    @staticmethod
    def verify_student(username, password):
        cur = mysql.connection.cursor()
        cur.execute("""
               SELECT 
                   stu_id, 
                   stu_username, 
                   stu_password, 
                   stu_first_name, 
                   stu_last_name,
                   profile_picture
               FROM student_tbl 
               WHERE stu_username = %s AND stu_password = %s
           """, (username, password))  # Fetch student details based on username and password
        student = cur.fetchone()
        cur.close()
        return student  # Ensure profile_picture (6th attribute) is returned

    @staticmethod
    def student_exists(username, password, phone_number, lrn, email):
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT * FROM student_tbl 
            WHERE stu_username = %s 
               OR stu_password = %s
               OR stu_phone_number = %s
               OR stu_lrn = %s
               OR stu_emailadd = %s
        """, (username, password, phone_number, lrn, email))  # Check if student already exists
        student = cur.fetchone()  # Retrieve a match if found
        cur.close()  # Close the cursor
        return student is not None  # Return True if student exists, otherwise False

    @staticmethod
    def get_student_counts():
        """Get the total count of students, and counts based on gender."""
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT 
                COUNT(*) AS total_students, 
                SUM(CASE WHEN stu_sex = 'Male' THEN 1 ELSE 0 END) AS male_students,
                SUM(CASE WHEN stu_sex = 'Female' THEN 1 ELSE 0 END) AS female_students
            FROM student_tbl
        """)
        counts = cur.fetchone()
        cur.close()
        return counts  # Returns a tuple (total_students, male_students, female_students)

    @staticmethod
    def add_student(username, password, first_name, middle_name, last_name, birthdate, sex, phone_number, lrn,
                    citizenship, emailadd, religion, address):
        if Student.student_exists(username, password, phone_number, lrn, emailadd):
            return False  # Prevent duplicate student entry
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO student_tbl (
                stu_first_name, stu_middle_name, stu_last_name, stu_birthdate, stu_sex, 
                stu_username, stu_password, stu_phone_number, stu_lrn, stu_citizenship, 
                stu_emailadd, stu_religion, stu_address
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (first_name, middle_name, last_name, birthdate, sex, username, password, phone_number, lrn, citizenship,
              emailadd, religion, address))  # Insert student details into the database
        mysql.connection.commit()  # Commit the transaction
        cur.close()  # Close the cursor
        return True  # Return True if student added successfully

    @staticmethod
    def get_all_students(search_query=None):
        """Fetch all students or filter by full name or CAMP ID."""
        cur = mysql.connection.cursor()

        if search_query:
            search_term = f"%{search_query}%"
            cur.execute("""
                SELECT 
                    stu_id, 
                    CONCAT(stu_first_name, ' ', IFNULL(stu_middle_name, ''), ' ', stu_last_name) AS full_name
                FROM 
                    student_tbl
                WHERE 
                    CONCAT(stu_first_name, ' ', IFNULL(stu_middle_name, ''), ' ', stu_last_name) LIKE %s
                    OR stu_id LIKE %s
                ORDER BY full_name ASC
                
            """, (search_term, search_term))  # Enable partial matches for full name or CAMP ID
        else:
            cur.execute("""
                SELECT 
                    stu_id, 
                    CONCAT(stu_first_name, ' ', IFNULL(stu_middle_name, ''), ' ', stu_last_name) AS full_name
                FROM 
                    student_tbl
                ORDER BY full_name ASC
            """)

        students = cur.fetchall()
        cur.close()
        return students

    @staticmethod
    def delete_student(student_id):
        """Deletes a student from the database."""
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM student_tbl WHERE stu_id = %s", (student_id,))
        mysql.connection.commit()
        cur.close()


    @staticmethod
    def get_student_by_id(student_id):
        """Fetch a student's details using their Student ID."""
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT 
                stu_id, 
                CONCAT(stu_first_name, ' ', IFNULL(stu_middle_name, ''), ' ', stu_last_name) AS full_name,
                stu_username, 
                stu_password, 
                stu_birthdate, 
                stu_phone_number, 
                stu_emailadd, 
                stu_address, 
                stu_lrn, 
                stu_citizenship, 
                stu_religion, 
                stu_sex, 
                profile_picture
            FROM student_tbl
            WHERE stu_id = %s
        """, (student_id,))

        student = cur.fetchone()  # Fetch the student's record
        cur.close()
        return student  # Return student details as a tuple or None if not found

    @staticmethod
    def student_profile(student_id):
        """Fetch a student's details using their Student ID."""
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT 
                stu_first_name, 
                stu_middle_name, 
                stu_last_name,
                stu_birthdate,  
                stu_sex,
                stu_phone_number,  
                stu_emailadd, 
                stu_address,
                stu_username,
                stu_password, 
                stu_lrn, 
                stu_citizenship, 
                stu_religion
                
            FROM student_tbl
            WHERE stu_id = %s
        """, (student_id,))

        student = cur.fetchone()  # Fetch the student's record
        cur.close()
        return student  # Return student details as a tuple or None if not found

    @staticmethod
    def get_enrolled_courses(student_id):
        """Fetch all courses the student is enrolled in, including professor IDs and evaluation status."""
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT 
                course_tbl.cou_id AS course_id,  
                course_tbl.cou_name AS course_name, 
                apply_tbl.raw_grade AS raw_grade,
                apply_tbl.final_grade AS final_grade,
                CONCAT(faculty_tbl.fac_first_name, ' ', 
                    IFNULL(faculty_tbl.fac_middle_name, ''), 
                    ' ', 
                    faculty_tbl.fac_last_name) AS assigned_professor,
                faculty_tbl.fac_id AS professor_id,
                EXISTS (
                    SELECT 1 
                    FROM evaluation_tbl 
                    WHERE evaluation_tbl.stu_id_fk = %s 
                    AND evaluation_tbl.fac_id_fk = faculty_tbl.fac_id
                ) AS already_evaluated  -- Check if the student has already evaluated this professor
            FROM apply_tbl
            INNER JOIN course_tbl ON apply_tbl.cou_id_fk = course_tbl.cou_id
            INNER JOIN faculty_tbl ON course_tbl.fac_id_fk = faculty_tbl.fac_id
            WHERE apply_tbl.stu_id_fk = %s
        """, (student_id, student_id))

        courses = cur.fetchall()
        cur.close()
        return [
            {
                "course_id": course[0],
                "course_name": course[1],
                "raw_grade": course[2],
                "final_grade": course[3],
                "assigned_professor": course[4],
                "professor_id": course[5],
                "already_evaluated": bool(course[6])  # Convert to boolean
            }
            for course in courses
        ]

    @staticmethod
    def get_available_courses():
        """Fetch all courses and their assigned professors."""
        cur = mysql.connection.cursor()
        cur.execute("""
                SELECT 
                    course_tbl.cou_id, 
                    course_tbl.cou_name, 
                    CONCAT(faculty_tbl.fac_first_name, ' ', IFNULL(faculty_tbl.fac_middle_name, ''), ' ', faculty_tbl.fac_last_name) AS assigned_professor
                FROM course_tbl
                LEFT JOIN faculty_tbl ON course_tbl.fac_id_fk = faculty_tbl.fac_id
            """)
        courses = cur.fetchall()
        cur.close()
        return [
            {
                "course_id": course[0],
                "course_name": course[1],
                "assigned_professor": course[2]
            }
            for course in courses
        ]

    @staticmethod
    def apply_for_courses(student_id, selected_courses):
        """Insert selected courses into the enrollment table."""
        cur = mysql.connection.cursor()
        success = True
        try:
            cur.execute("""
                    SELECT COUNT(*) 
                    FROM apply_tbl 
                    WHERE stu_id_fk = %s
                """, (student_id,))
            enrolled_count = cur.fetchone()[0]

            total_courses = enrolled_count + len(selected_courses)
            if total_courses > 8:
                return False, "You cannot enroll in more than 8 courses."

            # Enroll the student in the selected courses
            for course_id in selected_courses:
                cur.execute("""
                        INSERT IGNORE INTO apply_tbl (stu_id_fk, cou_id_fk)
                        VALUES (%s, %s)
                    """, (student_id, course_id))
            mysql.connection.commit()
        except Exception as e:
            mysql.connection.rollback()
            success = False
            return success, str(e)

        cur.close()
        return success, "Applied for courses successfully."

    @staticmethod
    def get_student_list_of_course(course_id):
        """Retrieve student list enrolled in a course"""
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT 
                s.stu_id, 
                s.stu_last_name,
                s.stu_first_name,
                s.stu_middle_name
            FROM student_tbl s
            JOIN apply_tbl a ON s.stu_id = a.stu_id_fk
            WHERE a.cou_id_fk = %s
            ORDER BY s.stu_last_name ASC
        """, (course_id,))
        students = cur.fetchall()
        cur.close()
        return students
    
    @staticmethod
    def remove_student_from_course(course_id, student_id):
        """Remove a student from a course."""
        cur = mysql.connection.cursor()
        cur.execute("""
            DELETE FROM apply_tbl
            WHERE cou_id_fk = %s AND stu_id_fk = %s
        """, (course_id, student_id))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def add_evaluation(student_id, professor_id, rating, comment):
        """
        Inserts a new evaluation into the evaluation_tbl.
        If anonymous, prepend 'Anonymous: ' to the comment.
        """
        try:
            cur = mysql.connection.cursor()
            eval_comment = comment
            query = """
                INSERT INTO evaluation_tbl (stu_id_fk, fac_id_fk, eval_rating, eval_comment, eval_date)
                VALUES (%s, %s, %s, %s, NOW())
            """
            cur.execute(query, (student_id, professor_id, rating, eval_comment))
            mysql.connection.commit()
            cur.close()
            return True, "Evaluation submitted successfully."
        except Exception as e:
            mysql.connection.rollback()
            return False, str(e)
    
    
        

class Faculty:
    @staticmethod
    def get_faculty_count():
        """Get the total count of faculty members."""
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) AS total_faculty FROM faculty_tbl")  # Count all faculty members
        faculty_count = cur.fetchone()
        cur.close()
        return faculty_count[0]  # Return the count

    @staticmethod
    def faculty_exists(email, username, phone_number):
        cur = mysql.connection.cursor()
        cur.execute("""
                SELECT * FROM faculty_tbl
                WHERE fac_email = %s
                   OR fac_username = %s
                   OR fac_phone_number = %s
            """, (email, username, phone_number))
        exists = cur.fetchone() is not None
        cur.close()
        return exists

    @staticmethod
    def add_faculty(username, password, first_name, middle_name, last_name, email, phone_number):
        if Faculty.faculty_exists(email, username, phone_number):
            return False  # Prevent duplicate entries

        cur = mysql.connection.cursor()
        cur.execute("""
                INSERT INTO faculty_tbl (
                    fac_username, fac_password, fac_first_name, fac_middle_name, fac_last_name, fac_email, fac_phone_number
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (username, password, first_name, middle_name, last_name, email, phone_number))
        mysql.connection.commit()
        cur.close()
        return True

    @staticmethod
    def get_faculty_without_courses():
        """Retrieve faculty members who are not assigned to any courses."""
        cur = mysql.connection.cursor()
        cur.execute("""
                SELECT 
                    f.fac_id, 
                    f.fac_full_name 
                FROM 
                    faculty_tbl AS f
                LEFT JOIN 
                    course_tbl AS c
                ON 
                    f.fac_id = c.fac_id_fk
                WHERE 
                    c.cou_name IS NULL;  -- Only include faculty without assigned courses
            """)
        faculty_without_courses = cur.fetchall()  # Fetch all matches
        cur.close()
        return faculty_without_courses  # Return the list of faculty members

    @staticmethod
    def verify_faculty(username, password):
        cur = mysql.connection.cursor()
        cur.execute("""
               SELECT 
                    fac_id, 
                    fac_username, 
                    fac_password,
                    CONCAT(fac_first_name, ' ', IFNULL(fac_middle_name, ''), ' ', fac_last_name) AS faculty_name
               FROM faculty_tbl 
               WHERE fac_username = %s AND fac_password = %s
           """, (username, password))
        faculty = cur.fetchone()
        cur.close()
        return faculty
    
    @staticmethod
    def get_students_by_faculty(faculty_id):
        """
        Retrieve students and course name for the faculty's assigned course.
        """
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT 
                s.stu_id, 
                s.stu_last_name, 
                s.stu_first_name, 
                s.stu_middle_name,
                s.profile_picture,
                c.cou_name AS course_name,
                a.raw_grade,
                a.final_grade,
                sc.score_written,  
                sc.score_project,  
                sc.score_exam      
            FROM student_tbl s
            JOIN apply_tbl a ON s.stu_id = a.stu_id_fk
            JOIN course_tbl c ON a.cou_id_fk = c.cou_id
            LEFT JOIN scores_tbl sc ON s.stu_id = sc.stu_id_fk AND c.cou_id = sc.cou_id_fk
            WHERE c.fac_id_fk = %s
            ORDER BY s.stu_last_name ASC
        """, (faculty_id,))
        students = cur.fetchall()
        cur.close()

        course_name = students[0][5] if students else "No Course Assigned"
        return students, course_name
        
    @staticmethod
    def get_student_popup(student_id):
        """Retrieve full student details by student_id."""
        
        cur = mysql.connection.cursor()  # ✅ No DictCursor (access by index)
        cur.execute("""
            SELECT 
                stu_id, 
                stu_first_name, 
                stu_middle_name, 
                stu_last_name, 
                profile_picture, 
                stu_phone_number, 
                stu_emailadd, 
                stu_address 
            FROM student_tbl
            WHERE stu_id = %s
        """, (student_id,))
        
        student = cur.fetchone()  # Fetch a single student
        cur.close()
        
        return student  # Returns a tuple (NOT a dictionary)
    
    @staticmethod
    def search_student(search_query, faculty_id):
        """Search students by first name, middle name, or last name within the faculty's assigned course."""
        cur = mysql.connection.cursor()
        search_term = f"%{search_query}%"
        cur.execute("""
            SELECT 
                s.stu_id, 
                s.stu_last_name, 
                s.stu_first_name, 
                s.stu_middle_name,
                s.profile_picture,
                c.cou_name AS course_name
            FROM 
                student_tbl s
            JOIN 
                apply_tbl a ON s.stu_id = a.stu_id_fk
            JOIN 
                course_tbl c ON a.cou_id_fk = c.cou_id
            WHERE 
                c.fac_id_fk = %s AND (
                    s.stu_first_name LIKE %s
                    OR s.stu_middle_name LIKE %s
                    OR s.stu_last_name LIKE %s
                )
            ORDER BY s.stu_last_name ASC
        """, (faculty_id, search_term, search_term, search_term))  # Restrict search to students in the course
        students = cur.fetchall()
        cur.close()
        return students

    @staticmethod
    def get_course_id_by_faculty(faculty_id):
        """
        Retrieve the course ID assigned to a faculty member.
        """
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT c.cou_id
            FROM course_tbl c
            WHERE c.fac_id_fk = %s
            LIMIT 1
        """, (faculty_id,))
        course = cur.fetchone()
        cur.close()
        return course[0] if course else None
    
    # @staticmethod
    # def get_grades_for_student(student_id, course_id):
    #     """
    #     Retrieve raw_grade and final_grade for a student in a specific course.
    #     """
    #     cur = mysql.connection.cursor()
    #     cur.execute("""
    #         SELECT raw_grade, final_grade
    #         FROM apply_tbl
    #         WHERE stu_id_fk = %s AND cou_id_fk = %s
    #     """, (student_id, course_id))
    #     grades = cur.fetchone()
    #     cur.close()
    #     return grades if grades else (None, None)
    
    
    @staticmethod
    def insert_scores(student_id, course_id, written_works, final_project, exams):
        """Insert scores into the scores_tbl."""
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO scores_tbl (stu_id_fk, cou_id_fk, score_written, score_project, score_exam)
            VALUES (%s, %s, %s, %s, %s)
        """, (student_id, course_id, written_works, final_project, exams))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def update_scores(student_id, course_id, written_works, final_project, exams):
        """Update scores in the scores_tbl."""
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE scores_tbl
            SET score_written = %s, score_project = %s, score_exam = %s
            WHERE stu_id_fk = %s AND cou_id_fk = %s
        """, (written_works, final_project, exams, student_id, course_id))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def update_grades(student_id, course_id, raw_grade, final_grade):
        """Update raw_grade and final_grade in apply_tbl."""
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE apply_tbl
            SET raw_grade = %s, final_grade = %s
            WHERE stu_id_fk = %s AND cou_id_fk = %s
        """, (raw_grade, final_grade, student_id, course_id))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def delete_scores(student_id, course_id):
        """Delete scores from scores_tbl and reset grades in apply_tbl."""
        cur = mysql.connection.cursor()
        cur.execute("""
            DELETE FROM scores_tbl
            WHERE stu_id_fk = %s AND cou_id_fk = %s
        """, (student_id, course_id))
        cur.execute("""
            UPDATE apply_tbl
            SET raw_grade = NULL, final_grade = NULL
            WHERE stu_id_fk = %s AND cou_id_fk = %s
        """, (student_id, course_id))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def show_evaluations(faculty_id):
        """Retrieve evaluations from students."""
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT 
                CONCAT(s.stu_first_name, ' ', IFNULL(s.stu_middle_name, ''), ' ', s.stu_last_name) AS student_name,
                e.eval_rating, 
                e.eval_comment, 
                e.eval_date,
                s.profile_picture,
                e.eval_id 
            FROM 
                evaluation_tbl AS e
            JOIN 
                student_tbl AS s ON e.stu_id_fk = s.stu_id
            WHERE 
                e.fac_id_fk = %s
            ORDER BY 
                e.eval_date DESC
        """, (faculty_id,))
        evaluations = cur.fetchall()
        cur.close()
        return evaluations

    @staticmethod
    def eval_rating(faculty_id):
        """Calculate the average evaluation rating for a specific professor."""
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT 
                fac_id_fk, 
                ROUND(AVG(eval_rating), 2) AS average_rating
            FROM 
                evaluation_tbl
            WHERE 
                fac_id_fk = %s
            GROUP BY 
                fac_id_fk
        """, (faculty_id,))
        ratings = cur.fetchone()
        cur.close()
        return ratings
    
    @staticmethod
    def total_evaluations(faculty_id):
        """Count the total number of evaluations for a specific professor."""
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT 
                COUNT(*) AS total_evaluations
            FROM 
                evaluation_tbl
            WHERE 
                fac_id_fk = %s
        """, (faculty_id,))
        total = cur.fetchone()
        cur.close()
        return total [0]
    
    @staticmethod
    def delete_evaluation(evaluation_id):
        """Delete an evaluation from the database."""
        cur = mysql.connection.cursor()
        cur.execute("""
            DELETE FROM evaluation_tbl
            WHERE eval_id = %s
        """, (evaluation_id,))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def get_rating_frequencies(faculty_id):
        """Retrieve the frequency of each rating (5-star, 4-star, etc.) for a faculty."""
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT eval_rating, COUNT(*) AS frequency
            FROM evaluation_tbl
            WHERE fac_id_fk = %s
            GROUP BY eval_rating
            ORDER BY eval_rating DESC
        """, (faculty_id,))
        frequencies = cur.fetchall()
        cur.close()

        # Convert to a dictionary with default values for missing ratings
        rating_frequencies = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
        for rating, count in frequencies:
            rating_frequencies[int(rating)] = count
            
        return rating_frequencies

    
    

            

 


    
        
   






