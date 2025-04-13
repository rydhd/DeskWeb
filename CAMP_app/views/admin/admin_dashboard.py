import tkinter as tk
from tkinter import ttk
from pathlib import Path
from tkinter import font, messagebox
from PIL import Image, ImageTk

from CAMP_app.views.admin.admit_student import AdmitStudent
from CAMP_app.views.admin.view_student_profile import ViewStudentProfile


class AdminDashboard(tk.Frame):
    def __init__(self, parent, main, admin_landing):
        super().__init__(parent)
        self.main = main
        self.admin_landing = admin_landing

        # Pathing
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        IMAGES_DIR = BASE_DIR / "static/images"

        self.dashboard_canvas = tk.Canvas(self, bg="#D9D9D9", bd=0, highlightthickness=0)
        self.dashboard_canvas.pack(fill=tk.BOTH, expand=True)

        student_card_path = IMAGES_DIR / "StudentQuantityCard.png"
        student_card = Image.open(student_card_path)
        student_card = student_card.resize((350, 200), Image.Resampling.LANCZOS)
        self.student_card = ImageTk.PhotoImage(student_card)
        self.dashboard_canvas.create_image(30, 30, image=self.student_card, anchor=tk.NW)

        faculty_card_path = IMAGES_DIR / "FacultyQuantityCard.png"
        faculty_card = Image.open(faculty_card_path)
        faculty_card = faculty_card.resize((350, 200), Image.Resampling.LANCZOS)
        self.faculty_card = ImageTk.PhotoImage(faculty_card)
        self.dashboard_canvas.create_image(440, 30, image=self.faculty_card, anchor=tk.NW)

        # Student count
        self.dashboard_canvas.create_text(235,55, text=self.display_student_count(), font=("Lexend Deca", 40, "bold") ,fill="#000000",  anchor=tk.NW)

        # Female count
        self.dashboard_canvas.create_text(120, 180, text=self.display_female_count(), font=("Lexend Deca", 18, "bold") ,fill="#000000", anchor=tk.NW)

        # Male count
        self.dashboard_canvas.create_text(280, 180, text=self.display_male_count(), font=("Lexend Deca", 18, "bold") ,fill="#000000", anchor=tk.NW)

        # Faculty count
        self.dashboard_canvas.create_text(645, 100, text=self.display_faculty_count(), font=("Lexend Deca", 40, "bold"),fill="#000000", anchor=tk.NW)

        # Admit student button
        self.admit_btn = tk.Button(
            self,
            width=14,
            text="+ Admit Student",
            bg="#8D0404",
            fg="#FFFFFF",
            font=("Lexend Deca", 8, "bold"),
            activebackground="#6C0303",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=lambda: self.admit_student()
        )
        self.admit_btn.place(x=444, y=250)
        self.admit_btn.bind("<Enter>", lambda e: self.admit_btn_hover_effect(e, True))
        self.admit_btn.bind("<Leave>", lambda e: self.admit_btn_hover_effect(e, False))

        # Search bar
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            self,
            textvariable=self.search_var,
            width=27,
            bg="#f0f0f0",
            fg="#020202",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#8D0404",
            highlightcolor="#020202",
            insertbackground="#020202",
            font=("Lexend Deca", 8)
        )
        self.search_entry.place(x=556,y=250, anchor=tk.NW, height=30)

        # Search Icon
        search_path = IMAGES_DIR / "SearchIcon.png"
        search_icon = Image.open(search_path)
        search_icon = search_icon.resize((30, 30), Image.Resampling.LANCZOS)
        self.search_icon = ImageTk.PhotoImage(search_icon)
        self.dashboard_canvas.create_image(754, 250, image=self.search_icon, anchor=tk.NW)

        self.search_entry.insert(0, " Search by Name or ID")  # Initial as placeholder
        # Handle focus for placeholder
        self.search_entry.bind("<FocusIn>", self.toggle_placeholder)
        self.search_entry.bind("<FocusOut>", self.toggle_placeholder)
        self.search_entry.bind("<KeyRelease>", self.filter_students)  # Filter students for live searching

        # Student list
        self.dashboard_canvas.create_text(30, 246, text="STUDENT LIST", font=("Lexend Deca", 20, "bold"),
                                          fill="#8D0404", anchor=tk.NW)

        header_font = font.Font(family="Lexend Deca", size=10, weight="bold")
        row_font = font.Font(family="Lexend Deca", size=10)

        # Fake styled header (red background, white text)
        header_frame = tk.Frame(self, bg="#8D0404", width=756, height=30)
        header_frame.place(x=30,y=290)
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text="Student Name", fg="#FFFFFF", bg="#8D0404",
                 font=header_font, width=34, anchor="center").pack(side="left", padx=0)
        tk.Label(header_frame, text="Student ID", fg="#FFFFFF", bg="#8D0404",
                 font=header_font, width=20, anchor="center").pack(side="left", padx=0)
        tk.Label(header_frame, text="", fg="#FFFFFF", bg="#8D0404",
                 font=header_font, width=28, anchor="center").pack(side="left", padx=0)

        self.student_list = ttk.Treeview(
            self,
            columns=("stu_full_name", "stu_id", "view_profile"),
            show="headings",
            height=13
        )

        # Dummy headings
        self.student_list.heading("stu_full_name", text="" )
        self.student_list.heading("stu_id", text="")
        self.student_list.heading("view_profile", text="")

        # Define columns
        self.student_list.column("stu_full_name", anchor="w", width=300)
        self.student_list.column("stu_id", anchor="center", width=204)
        self.student_list.column("view_profile", anchor="center", width=250)

        # self.student_list.tag_configure("font_row", font=row_font)

        # Configure alternating row background colors
        self.student_list.tag_configure("oddrow", background="#FFFFFF", font=row_font)
        self.student_list.tag_configure("evenrow", background="#E2E1E1", font=row_font)

        self.student_list.place(x=30,y=300)
        header_frame.lift()
        self.student_list.bind("<ButtonRelease-1>", self.view_profile)  # When the user clicked the "View Profile"

        self.display_students()
        self.display_data()


    def display_data(self):
        self.display_student_count()
        self.display_female_count()
        self.display_male_count()
        self.display_faculty_count()
        self.display_students()

    def display_student_count(self):
        student_count = self.main.admin_model.get_student_count()

        return student_count

    def display_female_count(self):
        female_count = self.main.admin_model.get_female_count()

        return female_count

    def display_male_count(self):
        male_count = self.main.admin_model.get_male_count()

        return male_count

    def display_faculty_count(self):
        faculty_count = self.main.admin_model.get_faculty_count()

        return faculty_count
    def admit_student(self):
        # self.admin_landing.sidebar_canvas.create_rectangle(0, 0, 400, 300, fill="black", stipple="gray50", outline="")
        # canvas.create_rectangle(0, 0, 400, 300, fill="black", stipple="gray50", outline="")
        self.admin_landing.attributes("-disabled", True) # Disable the interaction
        self.admin_landing.wait_window(AdmitStudent(self.main, self)) # Wait for the popup
        self.admin_landing.attributes("-disabled", False) # Re-enable the interaction
        self.admin_landing.focus_force() # Regain focus on the parent window

    def admit_btn_hover_effect(self, event, hover_in):
        new_color = "#B30505" if hover_in else "#8D0404"
        self.admit_btn.config(background=new_color)

    def display_students(self):
        self.all_students = self.main.admin_model.get_students() # Get and store the students
        self.update_treeview(self.all_students) # Pass the students

    def update_treeview(self, students):
        # Clear and display
        self.student_list.delete(*self.student_list.get_children())
        # for student in students:
        #     self.student_list.insert("", "end", values=(f"    {student["stu_full_name"]}", f"AU{student["stu_id"]}", "View Profile"), tags=("font_row",))

        for index, student in enumerate(students):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.student_list.insert(
                "",
                "end",
                values=(f"    {student['stu_full_name']}", f"AU{student['stu_id']}", "View Profile"),
                tags=(tag,)
            )

    def filter_students(self, event=None):
        search_text = self.search_var.get().lower() # Get the user input
        # Manipulate the studentlist for filtering
        filtered_students = [
            s for s in self.all_students
            if search_text in s["stu_full_name"].lower() or search_text in str(s["stu_id"])
        ]
        self.update_treeview(filtered_students) # Update the student list with filtered students

    def toggle_placeholder(self, event):
        if event.type == "9":  # FocusIn
            if self.search_entry.get() == " Search by Name or ID":
                self.search_entry.delete(0, tk.END)
                self.search_entry.config(fg="gray")
        elif event.type == "10":  # FocusOut
            if not self.search_entry.get():
                self.search_entry.insert(0, " Search by Name or ID")
                self.search_entry.config(fg="gray")

    def view_profile(self, event):
        # Get the selected row
        selected_row = self.student_list.identify_row(event.y)

        # Get the clicked column
        column_id = self.student_list.identify_column(event.x) # OUtput #3

        # Define the column index
        VIEW_PROFILE_COLUMN_INDEX = 3

        # Convert column_id (e.g., "#3") to integer and check if it matches the 'View Profile' column
        if int(column_id[1:]) == VIEW_PROFILE_COLUMN_INDEX:
            values = self.student_list.item(selected_row, "values")

            if values:
                stu_id = values[1][2:]  # Adjust index based on your data structure
                student_data = self.main.admin_model.get_student_profile(stu_id)

                # Open Student Profile
                self.admin_landing.attributes("-disabled", True)  # Disable the interaction
                self.admin_landing.wait_window(ViewStudentProfile(self, self.admin_landing, self.main, student_data))  # Wait for the popup
                self.admin_landing.attributes("-disabled", False)  # Re-enable the interaction
                self.admin_landing.focus_force()  # Regain focus on the parent window