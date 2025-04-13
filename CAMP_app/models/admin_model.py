import mysql

class AdminModel:
    def __init__(self, database):
        self.db = database

    def get_student_count(self):
        conn = self.db.get_connection()

        # Connection failed
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM student_tbl"
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def get_female_count(self):
        conn = self.db.get_connection()

        # Connection failed
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM student_tbl WHERE stu_sex = 'Female'"
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def get_male_count(self):
        conn = self.db.get_connection()

        # Connection failed
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM student_tbl WHERE stu_sex = 'Male'"
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def get_faculty_count(self):
        conn = self.db.get_connection()

        # Connection failed
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM faculty_tbl"
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def get_students(self):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT stu_full_name, stu_id FROM student_tbl ORDER BY stu_full_name ASC"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def get_student_profile(self, stu_id):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM student_tbl WHERE stu_id = %s"
            cursor.execute(query, (stu_id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def is_faculty_username_taken(self, username):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "SELECT * FROM faculty_tbl WHERE fac_username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def is_student_username_taken(self, username):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "SELECT * FROM student_tbl WHERE stu_username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def admit_student(self, first_name, middle_name, last_name,birth_date, sex, username, password, phone_number, lrn, citizenship, email, religion, address):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "INSERT INTO student_tbl (stu_first_name, stu_middle_name, stu_last_name, stu_birthdate, stu_sex, stu_username, stu_password, stu_phone_number, stu_lrn, stu_citizenship, stu_emailadd, stu_religion, stu_address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (first_name, middle_name, last_name,birth_date, sex, username, password, phone_number, lrn, citizenship, email, religion, address))
            if cursor.rowcount > 0:
                conn.commit()
                cursor.close()
                return True
            else:
                conn.rollback()
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def update_student_pfp(self, stu_id, file_name):
        conn = self.db.get_connection()

        if not conn:
            return None


        try:
            cursor = conn.cursor()
            query = "UPDATE student_tbl SET profile_picture = %s WHERE stu_id = %s"
            cursor.execute(query, (file_name, stu_id))
            if cursor.rowcount > 0:
                conn.commit()
                cursor.close()
                print("Profile picture updated successfully!")
                return True
            else:
                print("Failed to upload profile picture")
                conn.rollback()
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def expel_student(self, stu_id):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "DELETE FROM student_tbl WHERE stu_id = %s"
            cursor.execute(query, (stu_id,))
            if cursor.rowcount > 0:
                conn.commit()
                cursor.close()
                print("Student Expelled")
                return True
            else:
                print("Student was not expelled")
                conn.rollback()
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def update_student_profile(self, stu_id, new_username, new_password, new_birthdate, new_phone_number, new_emailadd,
                               new_address, new_lrn, new_citizenship, new_religion, new_sex):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "UPDATE student_tbl SET stu_username = %s, stu_password = %s, stu_birthdate = %s, stu_phone_number = %s, stu_emailadd = %s, stu_address = %s, stu_lrn = %s, stu_citizenship = %s, stu_religion = %s, stu_sex = %s WHERE stu_id = %s"
            cursor.execute(query, (
            new_username, new_password, new_birthdate, new_phone_number, new_emailadd, new_address, new_lrn,
            new_citizenship, new_religion, new_sex, stu_id))
            if cursor.rowcount > 0:
                conn.commit()
                cursor.close()
                return True
            else:
                conn.rollback()
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()


    def get_faculties(self):
        conn = self.db.get_connection()

        # Connection failed
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT f.fac_id, f.fac_full_name, c.cou_name AS course_name FROM faculty_tbl AS f LEFT JOIN course_tbl AS c ON f.fac_id = c.fac_id_fk"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def get_faculty_students(self, fac_id):
        conn = self.db.get_connection()

        # Connection failed
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT DISTINCT s.stu_id, s.stu_full_name FROM apply_tbl a JOIN student_tbl s ON a.stu_id_fk = s.stu_id JOIN course_tbl c ON a.cou_id_fk = c.cou_id JOIN faculty_tbl f ON c.fac_id_fk = f.fac_id WHERE f.fac_id = %s"
            cursor.execute(query, (fac_id,))
            fac_students = cursor.fetchall()
            cursor.close()
            return fac_students
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def get_course_id_by_faculty(self, fac_id):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT cou_id FROM course_tbl WHERE fac_id_fk = %s"
            cursor.execute(query, (fac_id,))
            result = cursor.fetchone()
            cursor.close()
            return result["cou_id"] if result else None
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def remove_faculty_student(self, cou_id, stu_id):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "DELETE FROM apply_tbl WHERE cou_id_fk = %s AND stu_id_fk = %s"
            cursor.execute(query, (cou_id, stu_id))
            if cursor.rowcount > 0:
                conn.commit()
                cursor.close()
                print("Student removed")
                return True
            else:
                print("Student was not removed")
                conn.rollback()
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def add_faculty(self, username, password, first_name, middle_name, last_name, email, phone_number):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO faculty_tbl (fac_username, fac_password, fac_first_name, fac_middle_name, fac_last_name, fac_email, fac_phone_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (username, password, first_name, middle_name, last_name, email, phone_number))

            if cursor.rowcount > 0:
                conn.commit()
                cursor.close()
                print("Faculty Added Successfully")
                return True
            else:
                print("Failed to Add Faculty")
                conn.rollback()

        except mysql.connector.Error as error:
            print(error)
            return None

        finally:
            conn.close()

    def get_courses(self):
        conn = self.db.get_connection()

        # Connection failed
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT
                course_name,    
                day_of_week, 
                time_start, 
                time_end,
                concat(fac_first_name, ' ', IFNULL(fac_middle_name, ''), ' ', fac_last_name) AS faculty_name
            FROM
                course_schedule_faculty
            WHERE
                course_name IS NOT NULL
                """
            cursor.execute(query)
            course = cursor.fetchall()
            cursor.close()
            return course
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def get_course_id_by_name(self, course_name):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT cou_id FROM course_tbl WHERE cou_name = %s"
            cursor.execute(query, (course_name,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                return result['cou_id']
            else:
                return None
        except mysql.connector.Error as error:
            print(f"Error fetching course ID: {error}")
            return None
        finally:
            conn.close()

    def get_schedule_days(self):
        conn = self.db.get_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            query = "SELECT DISTINCT day_of_week FROM schedule_tbl"
            cursor.execute(query)
            days = [row[0] for row in cursor.fetchall()]
            return days
        except mysql.connector.Error as error:
            print(f"Error fetching schedule days: {error}")
            return []
        finally:
            cursor.close()
            conn.close()

    def get_unassigned_faculties(self):
        conn = self.db.get_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            query = """
            SELECT f.fac_full_name 
            FROM faculty_tbl f
            LEFT JOIN course_tbl c ON f.fac_id = c.fac_id_fk
            WHERE c.fac_id_fk IS NULL
            """
            cursor.execute(query)
            faculty_names = [row[0] for row in cursor.fetchall()]
            return faculty_names
        except mysql.connector.Error as error:
            print(f"Error fetching faculty names: {error}")
            return []
        finally:
            cursor.close()
            conn.close()

    def get_schedule_times(self):
        conn = self.db.get_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            query = "SELECT CONCAT(time_start, ' - ', time_end) AS time_range FROM schedule_tbl"
            cursor.execute(query)
            schedule_times = [row[0] for row in cursor.fetchall()]
            return schedule_times
        except mysql.connector.Error as error:
            print(f"Error fetching schedule times: {error}")
            return []
        finally:
            cursor.close()
            conn.close()

    def is_schedule_taken(self, day, time_start, time_end):
        conn = self.db.get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            query = """
                SELECT c.cou_name, s.day_of_week, s.time_start, s.time_end
                FROM schedule_tbl as s
                INNER JOIN course_tbl as c ON s.sch_id = c.sch_id_fk
                WHERE s.day_of_week = %s AND s.time_start = %s AND s.time_end = %s
            """
            cursor.execute(query, (day, time_start, time_end))
            status = cursor.fetchone()
            return status
        except mysql.connector.Error as error:
            print(f"Error checking schedule: {error}")
            return False
        finally:
            cursor.close()
            conn.close()

    def get_faculty_id_by_name(self, faculty_name):
        conn = self.db.get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT fac_id FROM faculty_tbl WHERE fac_full_name = %s", (faculty_name,))
            result = cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as error:
            print(f"Error fetching faculty ID: {error}")
            return None
        finally:
            cursor.close()
            conn.close()

    def get_schedule_id(self, day, time_start, time_end):
        conn = self.db.get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = """
                SELECT sch_id FROM schedule_tbl 
                WHERE day_of_week = %s AND time_start = %s AND time_end = %s
            """
            cursor.execute(query, (day, time_start, time_end))
            result = cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as error:
            print(f"Error fetching schedule ID: {error}")
            return None
        finally:
            cursor.close()
            conn.close()

    def add_course(self, course_name, faculty_id, schedule_id):
        conn = self.db.get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()

            # Check if course name already exists
            cursor.execute("SELECT COUNT(*) FROM course_tbl WHERE cou_name = %s", (course_name,))
            if cursor.fetchone()[0] > 0:
                print("Course name already exists.")
                return False

            # Insert course into course_tbl
            query = """
                INSERT INTO course_tbl (cou_name, fac_id_fk, sch_id_fk)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (course_name, faculty_id, schedule_id))

            if cursor.rowcount > 0:
                conn.commit()
                cursor.close()
                print("Course Added Successfully")
                return True
            else:
                print("Failed to Add Course")
                conn.rollback()

        except mysql.connector.Error as error:
            print(error)
            return None

        finally:
            conn.close()