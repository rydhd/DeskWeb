import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
from customtkinter import *

class CourseApplication(tk.Toplevel):
    def __init__(self, parent,student_courses,main,student_data,stu_id,on_submit=None):
        super().__init__(parent)
        self.student_courses = student_courses
        self.main = main
        self.student_data = student_data
        self.stu_id = stu_id
        self.on_submit = on_submit

        self.title("Course Application")
        self.geometry("1000x600+120+20")
        self.resizable(False, False)
        self.config(bd=0, highlightthickness=0)

        # Make this window modal
        self.grab_set()  # Prevents interaction with other windows
        self.transient(parent)  # Associates this window with the parent
        self.wait_visibility()  # Ensures the window is fully drawn before proceeding

        # Frame for Available Courses
        frame = tk.Frame(self, bd=2, relief="ridge")
        frame.pack(pady=10, padx=10, fill="x")

        self.lbl = ctk.CTkLabel(frame, text="Course Application", font=("Lexend Deca", 14, "bold"),
                                text_color="white", bg_color="#8D0404")
        self.lbl.pack(fill="x")

        style = ttk.Style()
        style.configure("CustomCourses.Treeview", rowheight=30, font=("Lexend Deca", 10, "normal"))

        self.courses = ttk.Treeview(frame, columns=("cou_name", "assigned_prof"), show="headings",style="CustomCourses.Treeview")
        self.courses.heading("cou_name", text="Course Name")
        self.courses.heading("assigned_prof", text="Assigned Professor")

        self.courses.column("cou_name", width=350, anchor="center")
        self.courses.column("assigned_prof", width=350, anchor="center")
        self.courses.pack(side="left", fill="both", expand=True)

        self.get_initial_courses()

        self.selected_courses_list = {}
        self.course_buttons = {}  # Track buttons for selected courses

        # Frame for Selected Courses
        self.selected_frame = tk.Frame(self, bd=2, relief="ridge",width=50, height=150)
        self.selected_frame.pack(pady=10, padx=10, fill="x")
        self.selected_frame.propagate(False)

        self.selected_label = ctk.CTkLabel(self.selected_frame, text="Selected Course",
                                           font=("Lexend Deca", 14, "bold"),
                                           text_color="white", bg_color="#8D0404")
        self.selected_label.pack(fill="x")

        style = ttk.Style()
        style.configure("Custom.Treeview",rowheight=30,font=("Lexend Deca", 10, "normal"))

        self.selected_list = ttk.Treeview(self.selected_frame, columns=("cou_name", "assigned_prof","Action"), show="headings",style="Custom.Treeview")
        self.selected_list.heading("cou_name", text="Course Name")
        self.selected_list.heading("assigned_prof", text="Assigned Professor")
        self.selected_list.heading("Action", text="")

        self.selected_list.column("Action", width=30, anchor="center")
        self.selected_list.column("cou_name", anchor="center")
        self.selected_list.column("assigned_prof", anchor="center")
        self.selected_list.pack(fill="both", expand=True)

        self.confirm_btn = ctk.CTkButton(
            self, text="Confirm Application", fg_color="#8D0404", text_color="white",font=("Lexend Deca", 14, "normal"),
            command=lambda: self.confirm_application())

        self.confirm_btn.place(relx=0.95, rely=0.95, anchor="se")

        self.selected_list.bind("<Button-1>", self.on_tree_click)

    def get_initial_courses(self):
        student_id = self.stu_id
        initial_courses = self.main.student_model.fetch_courses(student_id)

        if initial_courses and isinstance(initial_courses[0], dict):
            initial_courses = [
                (course.get("cou_id"), course.get("cou_name", "N/A"), course.get("fac_full_name", "N/A"))
                for course in initial_courses
            ]

        self.courses.delete(*self.courses.get_children())

        # Clear existing buttons if needed
        if hasattr(self, 'course_buttons_panel'):
            for btn in self.course_buttons_panel:
                btn.destroy()
        self.course_buttons_panel = []

        style = ttk.Style()
        row_height = style.lookup("Treeview", "rowheight") or 20

        top_offset = self.courses.winfo_rooty() - self.winfo_rooty() + 30  # Match Treeview offset
        button_padding = 38

        for index, (course_id, course_name, professor) in enumerate(initial_courses):
            row_id = self.courses.insert("", "end", values=(course_name, professor))

            btn = ctk.CTkButton(
                self, text="Select", corner_radius=7, fg_color="#8D0404", text_color="white",font=("Lexend Deca", 13, "normal"),
                width=100, height=20,
                command=lambda c=(course_id, course_name, professor): self.selected_courses(c)
            )

            y_pos = top_offset + index * row_height + button_padding
            btn.place(x=870, y=y_pos)
            self.course_buttons_panel.append(btn)

    def selected_courses(self, course):
        if len(course) == 3:
            course_id, course_name, professor = course
        elif len(course) == 2:
            course_id = "N/A"
            course_name, professor = course
            print(f"Warning: Missing course_id for {course_name}. Using 'N/A'.")
        else:
            print(f"Invalid course data: {course}")
            return

        if course_name not in self.selected_courses_list:
            self.selected_courses_list[course_name] = (professor, course_id)
            self.selected_list.insert("", "end", values=(course_name, professor, "🗑"))

    def realign_buttons(self):
        """ Adjusts button positions to match row positions dynamically """
        self.update_idletasks()

        for course, (row_id, btn) in self.course_buttons.items():
            # Get the bounding box for the row in the main Treeview
            bbox = self.courses.bbox(row_id)
            if bbox:
                x_pos = bbox[2] + 10  # Position the button next to the last column
                y_pos = bbox[1]  # Align with the row's top y-coordinate

                btn.place(x=x_pos, y=y_pos)  # Adjust the button position next to the row

    def remove_course(self, course_name):
        # Remove from data structure
        if course_name in self.selected_courses_list:
            del self.selected_courses_list[course_name]

        # Find and delete the row from Treeview
        for row_id in self.selected_list.get_children():
            values = self.selected_list.item(row_id)["values"]
            if values and values[0] == course_name:
                self.selected_list.delete(row_id)
                break

    def confirm_application(self):
        student_id = self.stu_id

        # Get how many courses the student already has
        existing_courses = self.main.student_model.get_courses(student_id)
        total_existing = len(existing_courses) if existing_courses else 0
        total_selected = len(self.selected_courses_list)

        if total_existing + total_selected > 8:
            tk.messagebox.showwarning(
                "Course Limit Reached",
                f"You can only apply for 8 courses total.\n"
                f"You currently have {total_existing}.\n"
                f"You selected {total_selected}.\n"
                f"Please remove some courses before confirming."
            )
            return

        # Proceed with application
        for course_name, (professor, course_id) in self.selected_courses_list.items():
            print(f"Applying for {course_name} with ID {course_id}...")
            result = self.main.student_model.apply_for_course(student_id, course_id)

            if result:
                messagebox.showinfo("Success", f"Successfully applied for course: {course_name}")
            else:
                messagebox.showinfo("Failed", f"Failed to apply for course: {course_name}")

        self.destroy()
        if self.on_submit:
            self.on_submit()

    def on_tree_click(self, event):
        region = self.selected_list.identify("region", event.x, event.y)
        if region == "cell":
            row_id = self.selected_list.identify_row(event.y)
            col = self.selected_list.identify_column(event.x)

            if col == "#3":
                values = self.selected_list.item(row_id)["values"]
                if values:
                    course_name = values[0]
                    self.remove_course(course_name)






