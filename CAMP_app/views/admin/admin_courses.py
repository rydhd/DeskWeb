import tkinter as tk
from tkinter import font, ttk, messagebox

from CAMP_app.views.admin.add_course import AddCourse

class AdminCourses(tk.Frame):
    def __init__(self, parent, main, admin_landing, admin_faculty):
        super().__init__(parent)
        self.main = main
        self.admin_landing = admin_landing
        self.admin_faculty = admin_faculty

        # Canvas
        self.courses_canvas = tk.Canvas(self, bg="#D9D9D9", bd=0, highlightthickness=0)
        self.courses_canvas.pack(fill=tk.BOTH, expand=True)

        # Course Header
        self.courses_canvas.create_text(30, 20, text="COURSES", font=("Lexend Deca", 20, "bold"), fill="#8D0404",
                                        anchor=tk.NW)

        # Course List Frame
        header_font = font.Font(family="Lexend Deca", size=10, weight="bold")
        row_font = font.Font(family="Lexend Deca", size=10)

        # Course List
        self.course_list = ttk.Treeview(
            self,  # Parent is course_list_frame
            columns=("course_name", "day", "time", "faculty"),
            show="headings",
            height=22
        )

        # Headings
        self.course_list.heading("course_name", text="")
        self.course_list.heading("day", text="")
        self.course_list.heading("time", text="")
        self.course_list.heading("faculty", text="")

        # Column Widths
        col_width_cname = 250
        col_width_day = 150
        col_width_time = 150
        col_width_faculty = 248

        # Columns
        self.course_list.column("course_name", anchor="w", width=col_width_cname)
        self.course_list.column("day", anchor="w", width=col_width_day)
        self.course_list.column("time", anchor="center", width=col_width_time)
        self.course_list.column("faculty", anchor="w", width=col_width_faculty)
        # self.course_list.tag_configure("row", font=row_font)

        # Configure alternating row background colors
        self.course_list.tag_configure("oddrow", background="#FFFFFF", font=row_font)
        self.course_list.tag_configure("evenrow", background="#E2E1E1", font=row_font)

        # Fake header
        course_header_height = 30
        course_header_frame = tk.Frame(
            self,
            bg="#8D0404",
            width=800,
            height=course_header_height
        )
        course_header_frame.pack_propagate(False)

        tk.Label(course_header_frame, text="Course Name", fg="#FFFFFF", bg="#8D0404",
                 font=header_font, width=24, anchor="center").pack(side="left", padx=0)
        tk.Label(course_header_frame, text="Day", fg="#FFFFFF", bg="#8D0404",
                 font=header_font, width=16, anchor="center").pack(side="left", padx=0)
        tk.Label(course_header_frame, text="Time", fg="#FFFFFF", bg="#8D0404",
                 font=header_font, width=22, anchor="center").pack(side="left", padx=0)
        tk.Label(course_header_frame, text="Assigned Professor", fg="#FFFFFF", bg="#8D0404",
                 font=header_font, width=20, anchor="center").pack(side="left", padx=0)

        course_header_x = 30
        course_header_y = 60
        course_header_frame.place(x=course_header_x, y=course_header_y)

        course_tree_x = course_header_x
        course_tree_y = course_header_y + 8
        self.course_list.place(x=course_tree_x, y=course_tree_y)
        course_header_frame.lift()

        # Add Course Button
        self.add_course_btn = tk.Button(
            self,
            width=14,
            text="+ Add Course",
            bg="#8D0404",
            fg="#FFFFFF",
            font=("Lexend Deca", 10, "bold"),
            activebackground="#6C0303",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.add_course
        )
        self.add_course_btn.place(x=696, y=550)
        self.add_course_btn.bind("<Enter>", lambda e: self.add_course_btn_hover_effect(e, True))
        self.add_course_btn.bind("<Leave>", lambda e: self.add_course_btn_hover_effect(e, False))

        self.display_courses()

    def add_course_btn_hover_effect(self, event, hover_in):
        new_color = "#B30505" if hover_in else "#8D0404"
        self.add_course_btn.config(background=new_color)

    def display_courses(self):
        courses = self.main.admin_model.get_courses()
        # for course in courses:
        #     self.course_list.insert("", "end", values=(
        #         f"    {course["course_name"]}",
        #         f"    {course["day_of_week"]}",
        #         f"{course["time_start"]}-{course["time_end"]}",
        #         f"        {course["faculty_name"]}"
        #     ), tags=("row",))

        for index, course in enumerate(courses):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.course_list.insert(
                "",
                "end",
                values=(
                    f"    {course["course_name"]}",
                    f"    {course["day_of_week"]}",
                    f"{course["time_start"]}-{course["time_end"]}",
                    f"        {course["faculty_name"]}"
                ),
                tags=(tag,)
            )

    def add_course(self):
        prof_names = self.main.admin_model.get_unassigned_faculties()
        if not prof_names:
            messagebox.showinfo("No Professors", "No available professors at the moment.")
            return
        self.admin_landing.attributes("-disabled", True)
        self.admin_landing.wait_window(AddCourse(self.admin_landing, self.main, self))
        self.admin_landing.attributes("-disabled", False)
        self.admin_landing.focus_force()

