import mysql

class FacultyModel:
    def __init__(self, database):
        self.db = database

    def get_faculty_course(self, fac_id):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
        SELECT 
            c.cou_id,
            c.cou_name
        FROM course_tbl c
        WHERE c.fac_id_fk = %s
        """
            cursor.execute(query, (fac_id,))
            course = cursor.fetchone()
            cursor.close()
            return course
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def get_students(self, fac_id):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
         SELECT 
            s.stu_id,
            s.stu_first_name,
            s.stu_middle_name,
            s.stu_last_name
        FROM apply_tbl a
        JOIN student_tbl s ON a.stu_id_fk = s.stu_id
        JOIN course_tbl c ON a.cou_id_fk = c.cou_id
        WHERE c.fac_id_fk = %s
        ORDER BY s.stu_last_name ASC
        """
            cursor.execute(query, (fac_id,))
            students = cursor.fetchall()
            cursor.close()
            return students
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

    def submit_scores(self, cou_id, stu_id, written_works, final_project, examination):
        conn = self.db.get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()

            # Check if the student already has a record
            check_query = """
            SELECT 1 FROM scores_tbl WHERE stu_id_fk = %s AND cou_id_fk = %s
            """
            cursor.execute(check_query, (stu_id, cou_id))
            record_exists = cursor.fetchone()

            if record_exists:
                # Prepare dynamic UPDATE query to only update non-null values
                update_fields = []
                params = []

                if written_works is not None:
                    update_fields.append("score_written = %s")
                    params.append(written_works)
                if final_project is not None:
                    update_fields.append("score_project = %s")
                    params.append(final_project)
                if examination is not None:
                    update_fields.append("score_exam = %s")
                    params.append(examination)

                if update_fields:  # Ensure there is at least one field to update
                    update_query = f"""
                    UPDATE scores_tbl
                    SET {', '.join(update_fields)}
                    WHERE stu_id_fk = %s AND cou_id_fk = %s
                    """
                    params.extend([stu_id, cou_id])
                    cursor.execute(update_query, tuple(params))

            else:
                # Insert new record if no existing scores
                insert_query = """
                INSERT INTO scores_tbl (stu_id_fk, cou_id_fk, score_written, score_project, score_exam)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (stu_id, cou_id, written_works, final_project, examination))

            conn.commit()
            cursor.close()
            return True

        except mysql.connector.Error as error:
            print(f"Database Error: {error}")
            return False

        finally:
            conn.close()

    def update_grades(self, cou_id, stu_id, raw_grade, final_grade):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = """
                UPDATE apply_tbl
            SET raw_grade = %s, final_grade = %s
            WHERE cou_id_fk = %s AND stu_id_fk = %s
            """
            cursor.execute(query, (raw_grade, final_grade, cou_id, stu_id))

            if cursor.rowcount > 0:
                conn.commit()
                cursor.close()
                print("Grades updated successfully")
                return True
            else:
                print("Failed to update grades")
                conn.rollback()
        except mysql.connector.Error as error:
            print(error)
            return None

        finally:
            conn.close()

    def get_student_scores(self, cou_id, stu_id):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT 
                    COALESCE(score_written, '') AS score_written, 
                    COALESCE(score_project, '') AS score_project, 
                    COALESCE(score_exam, '') AS score_exam
                FROM scores_tbl 
                WHERE cou_id_fk = %s AND stu_id_fk = %s
            """
            cursor.execute(query, (cou_id, stu_id))
            scores = cursor.fetchone()
            cursor.close()
            return scores if scores else {"score_written": "", "score_project": "", "score_exam": ""}
        except mysql.connector.Error as error:
            print(f"Error fetching scores: {error}")
            return None
        finally:
            conn.close()

    def get_student_grades(self, cou_id, stu_id):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT raw_grade, final_grade FROM apply_tbl WHERE cou_id_fk = %s AND stu_id_fk = %s"
            cursor.execute(query, (cou_id, stu_id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def get_evaluations(self, fac_id):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
        SELECT
            e.eval_id,
            e.stu_id_fk,
            e.eval_rating,
            e.eval_comment,
            e.eval_date,
            s.profile_picture,
            s.stu_full_name
        FROM evaluation_tbl e
        JOIN student_tbl s ON e.stu_id_fk = s.stu_id
        WHERE e.fac_id_fk = %s
        """
            cursor.execute(query, (fac_id,))
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def delete_evaluation(self, eval_id):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "DELETE FROM evaluation_tbl WHERE eval_id = %s"
            cursor.execute(query, (eval_id,))

            if cursor.rowcount > 0:
                conn.commit()
                print("Evaluation deleted successfully.")
                return True
            else:
                print("No ealuation found with the given ID.")
                conn.rollback()
                return False

        except mysql.connector.Error as error:
            print(f"Error removing evaluation: {error}")
            return None

        finally:
            cursor.close()
            conn.close()

    def get_average_rating(self, fac_id):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT 
                fac_id_fk, 
                ROUND(AVG(eval_rating), 2) AS average_rating
            FROM 
                evaluation_tbl
            WHERE 
                fac_id_fk = %s
            GROUP BY 
                fac_id_fk
                """
            cursor.execute(query, (fac_id,))
            ratings = cursor.fetchone()
            if ratings:
                return ratings["average_rating"]
            else:
                return 0.00
            cursor.close()
            return ratings

        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()

    def get_faculty_ratings(self, fac_id):
            conn = self.db.get_connection()

            if not conn:
                return None

            try:
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT eval_rating, COUNT(*) as count 
                    FROM evaluation_tbl 
                    WHERE fac_id_fk = %s 
                    GROUP BY eval_rating
                """
                cursor.execute(query, (fac_id,))
                results = cursor.fetchall()
                cursor.close()

                # Create a dictionary with rating counts initialized to 0
                ratings = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

                # Fill the dictionary with actual counts
                for row in results:
                    ratings[row["eval_rating"]] = row["count"]

                return ratings

            except mysql.connector.Error as error:
                print(error)
                return None
            finally:
                conn.close()

    def get_total_evaluations(self, fac_id):
        conn = self.db.get_connection()

        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT COUNT(*) FROM evaluation_tbl WHERE fac_id_fk = %s"
            cursor.execute(query, (fac_id,))
            count = cursor.fetchone()
            if count:
                return count["COUNT(*)"]
            else:
                return 0
            cursor.close()
            return ratings

        except mysql.connector.Error as error:
            print(error)
            return None
        finally:
            conn.close()
