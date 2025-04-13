import tkinter as tk
from tkinter import messagebox, font


class AddCourse(tk.Toplevel):
    def __init__(self, parent, main, admin_courses):
        super().__init__(parent)
        self.main = main
        self.admin_courses = admin_courses
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.title("Add Course")
        self.geometry("510x190+400+230")
        self.resizable(False, False)

        # Main frame
        self.main_frame = tk.Frame(self,  bg="#FFFFFF")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        tk.Label(self.main_frame, text="Add Course", font=("Lexend Deca", 20, "bold"), fg="#FFFFFF",
                 bg="#8D0404").pack(fill="x", expand=True, anchor="nw")

        lbl_font = font.Font(family="Lexend Deca", size=10, weight="bold")
        entry_font = font.Font(family="Lexend Deca", size=8)

        # Course Name
        tk.Label(self.main_frame, text="Course Name", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=20, y=62)
        self.course_name = tk.Entry(
            self,
            width=24,
            bg="#FFFFFF",
            fg="#020202",  # Black text
            relief="flat",  # Flat border for modern look
            highlightthickness=1,  # Thin outline
            highlightbackground="#020202",  # Border color (unfocused)
            highlightcolor="#8D0404",  # Border color (focused)
            insertbackground="#020202",  # Cursor color
            font=entry_font,
        )
        self.course_name.place(x=120, y=65)

        # Professor
        prof_names = self.main.admin_model.get_unassigned_faculties()
        prof_lbl = tk.Label(self.main_frame, text="Professor", font=lbl_font, fg="#020202", bg="#FFFFFF")
        prof_lbl.place(x=20, y=106)

        self.professor_var = tk.StringVar()
        self.professor_var.set("Select Professor \u25BE")
        self.professor_dropdown = tk.OptionMenu(
            self.main_frame,
            self.professor_var,
            *prof_names
        )

        # Dropdown design
        self.professor_dropdown.config(
            font=("Lexend Deca", 5, "bold"),
            bg="#FFFFFF",
            fg="#020202",
            activebackground="#E0E0E0",
            activeforeground="#020202",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#020202",
            bd=1,
            padx=41,
        )

        menu = self.professor_dropdown["menu"]
        menu.config(
            font=entry_font,
            bg="#FFFFFF",
            fg="#020202",
            activebackground="#8D0404",
            activeforeground="#FFFFFF",
            bd=0,
            tearoff=0
        )
        self.professor_dropdown.place(x=120, y=110)

        # Day
        days_of_week = self.main.admin_model.get_schedule_days()
        day_lbl = tk.Label(self.main_frame, text="Days", font=lbl_font, fg="#020202", bg="#FFFFFF")
        day_lbl.place(x=320, y=62)

        self.day_var = tk.StringVar()
        self.day_var.set("Select Day \u25BE")
        self.day_dropdown = tk.OptionMenu(
            self.main_frame,
            self.day_var,
            *days_of_week
        )

        # Dropdown design
        self.day_dropdown.config(
            font=("Lexend Deca", 5, "bold"),
            bg="#FFFFFF",
            fg="#020202",
            activebackground="#E0E0E0",
            activeforeground="#020202",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#020202",
            bd=1,
            padx=18,
        )

        menu = self.day_dropdown["menu"]
        menu.config(
            font=entry_font,
            bg="#FFFFFF",
            fg="#020202",
            activebackground="#8D0404",
            activeforeground="#FFFFFF",
            bd=0,
            tearoff=0
        )
        self.day_dropdown.place(x=370, y=66)

        # Time
        schedule_times = self.main.admin_model.get_schedule_times()
        time_lbl = tk.Label(self.main_frame, text="Time", font=lbl_font, fg="#020202", bg="#FFFFFF")
        time_lbl.place(x=320, y=106)

        self.time_var = tk.StringVar()
        self.time_var.set("Select Time \u25BE")
        self.time_dropdown = tk.OptionMenu(
            self.main_frame,
            self.time_var,
            *schedule_times
        )

        # Dropdown design
        self.time_dropdown.config(
            font=("Lexend Deca", 5, "bold"),
            bg="#FFFFFF",
            fg="#020202",
            activebackground="#E0E0E0",
            activeforeground="#020202",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#020202",
            bd=1,
            padx=16,
        )

        menu = self.time_dropdown["menu"]
        menu.config(
            font=entry_font,
            bg="#FFFFFF",
            fg="#020202",
            activebackground="#8D0404",
            activeforeground="#FFFFFF",
            bd=0,
            tearoff=0
        )
        self.time_dropdown.place(x=370, y=110)

        # Add Course Button
        self.add_course_btn = tk.Button(
            self.main_frame,
            width=14,
            text="Add Course",
            bg="#8D0404",
            fg="#FFFFFF",
            font=("Lexend Deca", 8, "bold"),
            activebackground="#6C0303",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.validate_add_course # NOTE: Bookmark
        )
        self.add_course_btn.place(x=374, y=150)
        self.add_course_btn.bind("<Enter>", lambda e: self.add_course_btn_hover_effect(e, True))
        self.add_course_btn.bind("<Leave>", lambda e: self.add_course_btn_hover_effect(e, False))

        # Close Button
        self.close_btn = tk.Button(
            self.main_frame,
            width=14,
            text="Close",
            bg="#8D0404",
            fg="#FFFFFF",
            font=("Lexend Deca", 8, "bold"),
            activebackground="#6C0303",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.close
        )
        self.close_btn.place(x=250, y=150)
        self.close_btn.bind("<Enter>", lambda e: self.close_btn_hover_effect(e, True))
        self.close_btn.bind("<Leave>", lambda e: self.close_btn_hover_effect(e, False))

    def close_btn_hover_effect(self, event, hover_in):
        new_color = "#B30505" if hover_in else "#8D0404"
        self.close_btn.config(background=new_color)

    def add_course_btn_hover_effect(self, event, hover_in):
        new_color = "#B30505" if hover_in else "#8D0404"
        self.add_course_btn.config(background=new_color)

    def validate_add_course(self):
        course_name = self.course_name.get().strip()
        faculty_name = self.professor_var.get()
        selected_day = self.day_var.get()
        selected_time = self.time_var.get()

        errors = []

        # Course name validation
        if not course_name:
            errors.append("Course name is required.")
        elif len(course_name) > 100:
            errors.append("Course name must not exceed 100 characters.")

        # Professor selection validation
        if faculty_name == "Select Professor \u25BE":
            errors.append("Please select a professor.")

        # Day selection validation
        if selected_day == "Select Day \u25BE":
            errors.append("Please select a day.")

        # Time selection validation
        if selected_time == "Select Time \u25BE":
            errors.append("Please select a time.")
        else:
            try:
                time_start, time_end = [t.strip() for t in selected_time.split('-')]
                if self.main.admin_model.is_schedule_taken(selected_day, time_start, time_end):
                    errors.append("Selected schedule is already taken.")
            except ValueError:
                errors.append("Invalid time format. Please select a valid time range.")

        # If no errors, proceed to add course
        if not errors:
            faculty_id = self.main.admin_model.get_faculty_id_by_name(faculty_name)
            schedule_id = self.main.admin_model.get_schedule_id(selected_day, time_start, time_end)

            if not schedule_id:
                messagebox.showerror("Error", "Schedule ID could not be found for the selected day and time.")
                return

            self.main.admin_model.add_course(course_name, faculty_id, schedule_id)
            messagebox.showinfo("Success", "Course added successfully!")
            self.clear_fields()
            self.refresh_course_list()
        else:
            messagebox.showerror("Validation Error", "\n".join(errors))


    def refresh_course_list(self):
        course_list = self.admin_courses.course_list
        for row in course_list.get_children():
            course_list.delete(row)
        self.admin_courses.display_courses()

    def clear_fields(self):
        self.course_name.delete(0, tk.END)
        self.professor_var.set("Select Professor \u25BE")
        self.day_var.set("Select Day \u25BE")
        self.time_var.set("Select Time \u25BE")

    def close(self):
        self.destroy()

