import tkinter as tk
from tkinter import ttk,messagebox
import customtkinter as ctk

from CAMP_app.views.student.faculty_eval import FacultyEvalView

from CAMP_app.views.student.course_apply import CourseApplication



class StudentCoursesTab(tk.Frame):
    def __init__(self, parent, main, student_landing):
        super().__init__(parent)
        self.main = main
        self.student_landing = student_landing
        self.student_session = student_landing.student_session
        self.config(bd=0, highlightthickness=0)

        self.style = ttk.Style()
        self.style.configure("Custom.TLabel", font=("Lexend Deca", 20, "bold"), foreground="#8D0404")

        self.lbl = ttk.Label(self, text="COURSES", style="Custom.TLabel")
        self.lbl.grid(row=0, column=0, columnspan=3, pady=10,padx=10)

        style = ttk.Style()
        style.configure("Treeview", rowheight=30, font=("Lexend Deca", 10, "bold"))
        self.style.configure("Treeview.Heading", background="lightblue", font=("Lexend Deca", 10, "bold"))

        self.course_list = ttk.Treeview(self,
                                        columns=["cou_name", "raw_grade", "final_grade", "assigned_prof", "evaluate"],style="Treeview",show="headings")
        self.course_list.place(x=10, y=50, width=800, height=400)

        self.course_list.bind("<<TreeviewSelect>>", self.disable_selection)
        # Disable clicking on headers
        self.course_list.bind("<Button-1>", self.disable_header_click)

        # Define column headings
        self.course_list.heading("cou_name", text="Course Name")
        self.course_list.heading("raw_grade", text="Raw Grade")
        self.course_list.heading("final_grade", text="Final Grade")
        self.course_list.heading("assigned_prof", text="Assigned Professor")
        self.course_list.heading("evaluate", text="")

        # Define column widths
        self.course_list.column("#0", width=0, stretch=tk.NO)
        self.course_list.column("cou_name", width=100, anchor="center")
        self.course_list.column("raw_grade", width=100, anchor="center")
        self.course_list.column("final_grade", width=100, anchor="center")
        self.course_list.column("assigned_prof", width=150, anchor="center")
        self.course_list.column("evaluate", width=100, anchor="center")

        self.display_enrolled_courses(self.student_session["stu_id"])

        self.apply_btn = ctk.CTkButton(self, text="+ Enlist Course", corner_radius=7, fg_color="#8D0404",font=("Lexend Deca", 13,),
                                       text_color="white", command=self.open_course_application)
        self.apply_btn.place(x=659, y=459)

    def display_enrolled_courses(self, stu_id):
        enrolled_courses = self.main.student_model.get_courses(stu_id)

        print("Displaying schedule for student ID:", stu_id)

        button_y_offset = 75
        row_height = 30
        self.evaluate_buttons = []

        # Configure row tags for styling
        self.course_list.tag_configure('even', background='#f0f0f0')  # light gray
        self.course_list.tag_configure('odd', background='#ffffff')  # white

        for index, course in enumerate(enrolled_courses):
            tag = 'even' if index % 2 == 0 else 'odd'
            item_id = self.course_list.insert(
                "", "end",
                values=(
                    course["course_name"],
                    course["raw_grade"],
                    course["final_grade"],
                    course["assigned_professor"],
                    ""
                ),
                tags=(tag,)
            )

            is_disabled = course.get("is_evaluated", False)

            # Button color and state
            button_state = tk.DISABLED if is_disabled else tk.NORMAL
            button_color = "#B0B0B0" if is_disabled else "#8D0404"
            button_text = "Evaluated" if is_disabled else "Evaluate"

            btn = ctk.CTkButton(
                self,
                text=button_text,
                corner_radius=5,
                fg_color=button_color,
                text_color="white",
                width=90,
                height=25,
                font=("Lexend Deca", 12, "bold"),
                command=(
                    None if is_disabled else lambda c=course: self.evaluate_course(
                        c["course_name"], c["assigned_professor"]
                    )
                )
            )
            btn.configure(state=button_state)
            btn.place(x=705, y=button_y_offset + (index * row_height))

            self.evaluate_buttons.append(btn)

    def open_course_application(self):
        # Get student ID from the current session
        stu_id = self.student_session["stu_id"]

        student_data = self.main.student_model.fetch_courses(stu_id)
        # Initialize the CourseApplication and pass the student ID
        CourseApplication(self, self.student_landing, self.main, student_data, stu_id,on_submit=self.refresh_courses)

    def evaluate_course(self, course_name, professor_name):
        """ Opens the Faculty Evaluation Form with the selected course & professor """
        stu_id = self.student_session["stu_id"]
        # Retrieve faculty_id using professor's name
        faculty_id = self.main.student_model.get_faculty_id(professor_name)
        faculty_name = professor_name
        course_name = course_name

        if not faculty_id:
            tk.messagebox.showerror("Error", f"Faculty ID not found for {professor_name}.")
            return

        print(f"Evaluating Course: {course_name}, Professor: {professor_name} (ID: {faculty_id})")  # Debugging

        FacultyEvalView(self, self.main, self.student_session, stu_id, faculty_id,faculty_name,course_name,on_submit=self.refresh_courses)

    def disable_selection(self, event):
        self.course_list.selection_remove(self.course_list.selection())

    # Function to disable header clicks
    def disable_header_click(self, event):
        """ Prevents column header clicks from sorting or being interactive """
        region = self.course_list.identify("region", event.x, event.y)
        if region == "heading":  # If clicked on the header, do nothing
            return "break"

    def refresh_courses(self):
        # Refresh course list
        for item in self.course_list.get_children():
            self.course_list.delete(item)

        for btn in self.evaluate_buttons:
            btn.destroy()
        self.evaluate_buttons.clear()

        self.display_enrolled_courses(self.student_session["stu_id"])

        # ✅ Refresh schedule tab as well
        if hasattr(self.student_landing, "schedule_tab"):
            self.student_landing.schedule_tab.display_schedule(self.student_session["stu_id"])










