import mysql

from CAMP_app.models.database import Database

class UserAuth:
    def __init__(self, main): # app parameter referenced on main
        self.main = main
        self.db = Database()

    def authenticate_admin(self, admin_username, admin_password):
        conn = self.db.get_connection()

        # Connection failed
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM admin_tbl WHERE adm_username = %s AND adm_password = %s"
            cursor.execute(query, (admin_username, admin_password))
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def authenticate_faculty(self, faculty_username, faculty_password):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM faculty_tbl WHERE fac_username = %s AND fac_password = %s"
            cursor.execute(query, (faculty_username, faculty_password))
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def authenticate_student(self, student_username, student_password):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM student_tbl WHERE stu_username = %s AND stu_password = %s"
            cursor.execute(query, (student_username, student_password))
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()