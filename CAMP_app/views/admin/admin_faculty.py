import tkinter as tk
from tkinter import font, ttk

from CAMP_app.views.admin.add_faculty import AddFaculty
from CAMP_app.views.admin.view_fac_students import ViewFacultyStudents


class AdminFaculty(tk.Frame):
    def __init__(self, parent, main, admin_landing):
        super().__init__(parent)
        self.main = main
        self.admin_landing = admin_landing

        # Canvas
        self.faculty_canvas = tk.Canvas(self, bg="#D9D9D9", bd=0, highlightthickness=0)
        self.faculty_canvas.pack(fill=tk.BOTH, expand=True)

        # Header
        self.faculty_canvas.create_text(30, 20, text="FACULTY MEMBERS", font=("Lexend Deca", 20, "bold"), fill="#8D0404",
                                         anchor=tk.NW)

        header_font = font.Font(family="Lexend Deca", size=10, weight="bold")
        row_font = font.Font(family="Lexend Deca", size=10)

        # Faculty List
        self.faculty_list = ttk.Treeview(
            self,
            columns=("fac_full_name", "fac_id", "course", "view_student"),
            show="headings",
            height=22
        )

        # Headings
        self.faculty_list.heading("fac_full_name", text="")
        self.faculty_list.heading("fac_id", text="")
        self.faculty_list.heading("course", text="")
        self.faculty_list.heading("view_student", text="")

        # Columns widths
        col_width_name = 250
        col_width_id = 100
        col_width_course = 250
        col_width_view = 198

        # Columns
        self.faculty_list.column("fac_full_name", anchor="w", width=col_width_name)
        self.faculty_list.column("fac_id", anchor="center", width=col_width_id)
        self.faculty_list.column("course", anchor="w", width=col_width_course)
        self.faculty_list.column("view_student", anchor="center", width=col_width_view)

        # self.faculty_list.tag_configure("row", font=row_font)

        # Configure alternating row background colors
        self.faculty_list.tag_configure("oddrow", background="#FFFFFF", font=row_font)
        self.faculty_list.tag_configure("evenrow", background="#E2E1E1", font=row_font)

        # Fake Header
        faculty_header_height = 30
        faculty_header_frame = tk.Frame(
            self,
            bg="#8D0404",
            width=800,
            height=faculty_header_height
        )
        faculty_header_frame.pack_propagate(False)

        tk.Label(faculty_header_frame, text="Faculty Name", fg="#FFFFFF", bg="#8D0404",
                 font=header_font, width=28, anchor="center").pack(side="left", padx=0)
        tk.Label(faculty_header_frame, text="Faculty ID", fg="#FFFFFF", bg="#8D0404",
                 font=header_font, width=10, anchor="center").pack(side="left", padx=0)
        tk.Label(faculty_header_frame, text="Course", fg="#FFFFFF", bg="#8D0404",
                 font=header_font, width=28, anchor="center").pack(side="left", padx=0)
        tk.Label(faculty_header_frame, text="", fg="#FFFFFF", bg="#8D0404",
                 font=header_font, width=20, anchor="center").pack(side="left", padx=0)

        header_x = 30
        header_y = 60
        faculty_header_frame.place(x=header_x, y=header_y)

        tree_x = header_x
        tree_y = header_y + 8
        self.faculty_list.place(x=tree_x, y=tree_y)
        self.faculty_list.bind("<ButtonRelease-1>", self.view_student)
        faculty_header_frame.lift()

        # Add Faculty Button
        self.add_fac_btn = tk.Button(
            self,
            width=14,
            text="+ Add Faculty",
            bg="#8D0404",
            fg="#FFFFFF",
            font=("Lexend Deca", 10, "bold"),
            activebackground="#6C0303",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.add_faculty
        )
        self.add_fac_btn.place(x=696, y=550)
        self.add_fac_btn.bind("<Enter>", lambda e: self.add_fac_btn_hover_effect(e, True))
        self.add_fac_btn.bind("<Leave>", lambda e: self.add_fac_btn_hover_effect(e, False))

        self.display_faculties()

    def add_fac_btn_hover_effect(self, event, hover_in):
        new_color = "#B30505" if hover_in else "#8D0404"
        self.add_fac_btn.config(background=new_color)

    def display_faculties(self):
        faculties = self.main.admin_model.get_faculties()
        # for faculty in faculties:
        #     self.faculty_list.insert("", "end", values=(f"    {faculty["fac_full_name"]}",
        #                                                 f"AU{faculty["fac_id"]}",
        #                                                 faculty["course_name"],
        #                                                 "View Students"), tags=("row",))

        for index, faculty in enumerate(faculties):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.faculty_list.insert(
                "",
                "end",
                values=(f"    {faculty["fac_full_name"]}",
                        f"AU{faculty["fac_id"]}",
                        faculty["course_name"],
                        "View Students"),
                tags=(tag,)
            )

    def view_student(self, event):
        selected_row = self.faculty_list.identify_row(event.y)
        column_id = self.faculty_list.identify_column(event.x)

        VIEW_STUDENT_COLUMN_INDEX = 4

        if int(column_id[1:]) == VIEW_STUDENT_COLUMN_INDEX:
            values = self.faculty_list.item(selected_row, "values")
            print(values)

            if values:
                fac_full_name = values[0][4:]
                fac_assigned_course = values[2]
                fac_id = values[1][2:]
                fac_students = self.main.admin_model.get_faculty_students(fac_id)

                self.admin_landing.attributes("-disabled", True)
                self.admin_landing.wait_window(
                    ViewFacultyStudents(self.admin_landing, self.main, fac_full_name, fac_assigned_course, fac_students, fac_id))
                self.admin_landing.attributes("-disabled", False)
                self.admin_landing.focus_force()

    def add_faculty(self):
        self.admin_landing.attributes("-disabled", True)
        self.admin_landing.wait_window(AddFaculty(self.admin_landing, self.main))
        self.admin_landing.attributes("-disabled", False)
        self.admin_landing.focus_force()