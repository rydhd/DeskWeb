import ctypes
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from tkinter import font, messagebox
from PIL import Image, ImageTk, ImageDraw


class FacultyStudents(tk.Frame):
    def __init__(self, parent, main, faculty_landing):
        super().__init__(parent)
        self.main = main
        self.faculty_landing = faculty_landing

        # Paths
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
        self.IMAGES_DIR = BASE_DIR / "static/images"
        self.PFP_DIR = BASE_DIR / "static/student_pfps"

        self.students_canvas = tk.Canvas(self, bg="#D9D9D9", bd=0, highlightthickness=0)
        self.students_canvas.pack(fill=tk.BOTH, expand=True)

        # Headings
        self.fac_id = self.faculty_landing.faculty_session["fac_id"]
        result = self.main.faculty_model.get_faculty_course(self.fac_id)
        self.cou_id = result["cou_id"]
        fac_course = result["cou_name"]
        self.students_canvas.create_text(20, 20, text=fac_course, font=("Lexend Deca", 20, "bold"), fill="#8D0404", anchor=tk.NW)

        self.create_student_list()

    def create_student_list(self):
        self.student_list_frame = tk.Frame(self, width=500, height=520, bd=0, highlightthickness=0)
        self.student_list_frame.place(x=20, y=60)
        self.student_list_frame.pack_propagate(False)

        # Fonts
        header_font = font.Font(family="Lexend Deca", size=8, weight="bold")
        row_font = font.Font(family="Lexend Deca", size=8)

        # Fake styled header (red background, white text)
        header_frame = tk.Frame(self.student_list_frame, bg="#8D0404")
        header_frame.pack(fill="x")

        tk.Label(header_frame, text="#", fg="#FFFFFF", bg="#8D0404",
                 font=header_font, width=5, anchor="center").pack(side="left", padx= 25)
        tk.Label(header_frame, text="Student Name", fg="#FFFFFF", bg="#8D0404",
                 font=header_font, width=25, anchor="center").pack(side="left", padx= 30)
        tk.Label(header_frame, text="Student ID", fg="#FFFFFF", bg="#8D0404",
                 font=header_font, width=15, anchor="center").pack(side="left", padx= 30)

        self.student_list = ttk.Treeview(
            self.student_list_frame,
            columns=("index", "stu_full_name", "stu_id"),
            show="headings",
            height=15
        )

        # Dummy headings to satisfy Treeview internals
        self.student_list.heading("index", text="")
        self.student_list.heading("stu_full_name", text="")
        self.student_list.heading("stu_id", text="")

        # Define column widths and alignments
        self.student_list.column("index", anchor="center", width=40)
        self.student_list.column("stu_full_name", anchor="center", width=200)
        self.student_list.column("stu_id", anchor="center", width=120)

        # Tag style for row font
        self.student_list.tag_configure("row", font=row_font)

        self.student_list.pack(fill=tk.BOTH, expand=True)
        self.student_list.bind("<ButtonRelease-1>", self.view_stu_profile)

        self.display_students()

    def display_students(self):
        students = self.main.faculty_model.get_students(self.fac_id)
        i = 0
        for student in students:
            i+=1
            stu_full_name = f"{student["stu_last_name"]}, {student["stu_first_name"]} {student["stu_middle_name"]}"
            self.student_list.insert("", "end", values=(i, stu_full_name, f"AU{student["stu_id"]}"), tags=("row",))

    def view_stu_profile(self, event):
        selected_row = self.student_list.identify_row(event.y)
        values = self.student_list.item(selected_row, "values")

        if values:
            stu_id = values[2][2:]  # Adjust index based on your data structure
            student_data = self.main.faculty_model.get_student_profile(stu_id)

            self.create_stu_profile_card(self.PFP_DIR, student_data)


    def create_stu_profile_card(self, PFP_DIR, student_data):
        if hasattr(self, 'stu_profile_card'):
            self.stu_profile_card.destroy()

        stu_pfp = student_data["profile_picture"]
        stu_full_name = student_data["stu_full_name"]
        stu_id = student_data["stu_id"]
        stu_phone_num = student_data["stu_phone_number"]
        stu_email = student_data["stu_emailadd"]
        stu_address = student_data["stu_address"]

        # Card
        self.stu_profile_card = tk.Frame(self, bg="#FFFFFF",width=300, height=280)
        self.stu_profile_card.place(x=540, y=60)
        self.stu_profile_card.pack_propagate(False)

        # Header and Close Button
        header_close_frame = tk.Frame(self.stu_profile_card, bg="#8D0404", height=24)
        header_close_frame.pack(fill="x", expand=True)

        tk.Label(header_close_frame, text="Student Profile", fg="#FFFFFF", bg="#8D0404", font=("Lexend Deca", 8, "bold")).place(x=105)

        self.close_profile_btn = tk.Button(
            header_close_frame,
            text="X",
            bg="#8D0404",
            fg="#FFFFFF",
            font=("Lexend Deca", 7, "bold"),
            activebackground="#6C0303",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.close_stu_profile
        )
        self.close_profile_btn.bind("<Enter>", lambda e: self.close_profile_btn_hover_effect(e, True))
        self.close_profile_btn.bind("<Leave>", lambda e: self.close_profile_btn_hover_effect(e, False))
        self.close_profile_btn.place(x=280)

        self.stu_profile_card_canvas = tk.Canvas(self.stu_profile_card, bg="#FFFFFF", bd=0, highlightthickness=0)
        self.stu_profile_card_canvas.pack(fill=tk.BOTH, expand=True)

        # Student PFP
        pfp_path = self.get_pfp_path(PFP_DIR, stu_id)
        self.pfp = self.make_pfp_circle(pfp_path)
        self.stu_profile_card_canvas.create_image(100, 15, anchor=tk.NW, image=self.pfp)

        # Student Full Name
        self.stu_profile_card_canvas.create_text(
            150,
            112,
            text=stu_full_name,
            fill="#020202",
            font=("Lexend Deca", 12, "bold"),
            anchor="n"
        )

        # Student ID
        self.stu_profile_card_canvas.create_text(
            150,
            130,
            text=f"AU{stu_id}",
            fill="#020202",
            font=("Lexend Deca", 10, "bold"),
            anchor="n"
        )

        # Details Frame
        details_frame = tk.Frame(self.stu_profile_card, bg="#FFFFFF", width=250, height=100, bd=0, highlightthickness=0)
        details_frame.pack_propagate(False)
        self.stu_profile_card_canvas.create_window(170, 210, window=details_frame)

        details_frame_canvas = tk.Canvas(details_frame, bg="#FFFFFF", bd=0, highlightthickness=0)
        details_frame_canvas.pack(fill=tk.BOTH, expand=True)

        # Student Phone Number
        phone_path = self.IMAGES_DIR / "PhoneIcon.png"
        phone_icon = Image.open(phone_path)
        phone_icon = phone_icon.resize((16, 16), Image.Resampling.LANCZOS)
        self.phone_icon = ImageTk.PhotoImage(phone_icon)
        details_frame_canvas.create_image(4, 4, image=self.phone_icon, anchor=tk.NW)
        details_frame_canvas.create_text(
            24,
            10,
            text=stu_phone_num,
            fill="#020202",
            font=("Lexend Deca", 8, "bold"),
            anchor="w"
        )

        # Student Email Address
        email_path = self.IMAGES_DIR / "EmailIcon.png"
        email_icon = Image.open(email_path)
        email_icon = email_icon.resize((16, 16), Image.Resampling.LANCZOS)
        self.email_icon = ImageTk.PhotoImage(email_icon)
        details_frame_canvas.create_image(4, 29, image=self.email_icon, anchor=tk.NW)
        details_frame_canvas.create_text(
            24,
            36,
            text=stu_email,
            fill="#020202",
            font=("Lexend Deca", 7, "bold"),
            anchor="w"
        )

        # Student Address
        address_path = self.IMAGES_DIR / "AddressIcon.png"
        address_icon = Image.open(address_path)
        address_icon = address_icon.resize((14, 12), Image.Resampling.LANCZOS)
        self.address_icon = ImageTk.PhotoImage(address_icon)
        details_frame_canvas.create_image(4, 54, image=self.address_icon, anchor=tk.NW)
        details_frame_canvas.create_text(
            24,
            60,
            text=stu_address,
            fill="#020202",
            font=("Lexend Deca", 7, "bold"),
            anchor="w"
        )

        self.create_stu_scores_and_grades_card(self.cou_id, stu_id)

    def close_stu_profile(self):
        if hasattr(self, 'stu_profile_card'):
            self.stu_profile_card.destroy()

        if hasattr(self, 'stu_grades_card'):
            self.stu_grades_card.destroy()

    def create_stu_scores_and_grades_card(self, cou_id, stu_id):
        if hasattr(self, 'stu_grades_card'):
            self.stu_grades_card.destroy()

        self.stu_grades_card = tk.Frame(self, width=300, height=230, bg="#FFFFFF", bd=0, highlightthickness=0)
        self.stu_grades_card.place(x=540, y=350)
        self.stu_grades_card.grid_propagate(False)

        title_font = font.Font(family="Lexend Deca", size=8, weight="bold")
        label_font = font.Font(family="Lexend Deca", size=6)
        entry_font = font.Font(family="Lexend Deca", size=6)

        # Header
        self.grades_header = tk.Label(self.stu_grades_card, text="Student Grades", fg="#FFFFFF", bg="#8D0404", font=title_font, width=42)
        self.grades_header.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Common padding values for centering
        label_padx = (40, 5)
        entry_padx = (15, 30)

        # Written Works
        tk.Label(self.stu_grades_card, text="Written Works (200):", bg="#FFFFFF", font=label_font).grid(
            row=1, column=0, sticky="e", padx=label_padx, pady=3
        )
        self.written_works = tk.Entry(
            self.stu_grades_card,
            width=18,
            bg="#F0F0F0",
            fg="#020202",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#020202",
            highlightcolor="#8D0404",
            insertbackground="#020202",
            font=entry_font
        )
        self.written_works.grid(row=1, column=1, padx=entry_padx, pady=3)

        # Final Project
        tk.Label(self.stu_grades_card, text="Final Project (100):", bg="#FFFFFF", font=label_font).grid(
            row=2, column=0, sticky="e", padx=label_padx, pady=3
        )
        self.final_project = tk.Entry(
            self.stu_grades_card,
            width=18,
            bg="#F0F0F0",
            fg="#020202",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#020202",
            highlightcolor="#8D0404",
            insertbackground="#020202",
            font=entry_font
        )
        self.final_project.grid(row=2, column=1, padx=entry_padx, pady=3)

        # Examination
        tk.Label(self.stu_grades_card, text="Examinations (150):", bg="#FFFFFF", font=label_font).grid(
            row=3, column=0, sticky="e", padx=label_padx, pady=3
        )
        self.examination = tk.Entry(
            self.stu_grades_card,
            width=18,
            bg="#F0F0F0",
            fg="#020202",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#020202",
            highlightcolor="#8D0404",
            insertbackground="#020202",
            font=entry_font
        )
        self.examination.grid(row=3, column=1, padx=entry_padx, pady=3)

        # Raw Grade
        tk.Label(self.stu_grades_card, text="Raw Grade:", bg="#FFFFFF", font=label_font).grid(
            row=4, column=0, sticky="e", padx=label_padx, pady=(8, 2)
        )
        self.raw_grade = tk.Label(self.stu_grades_card, text="-", bg="#FFFFFF", font=label_font)
        self.raw_grade.grid(row=4, column=1, sticky="w", padx=entry_padx, pady=(8, 2))

        # Final Grade
        tk.Label(self.stu_grades_card, text="Final Grade:", bg="#FFFFFF", font=label_font).grid(
            row=5, column=0, sticky="e", padx=label_padx, pady=2
        )
        self.final_grade = tk.Label(self.stu_grades_card, text="-", bg="#FFFFFF", font=label_font)
        self.final_grade.grid(row=5, column=1, sticky="w", padx=entry_padx, pady=2)

        # Submit Button
        self.submit_btn = tk.Button(
            self.stu_grades_card,
            text="Submit",
            bg="#8D0404",
            fg="#FFFFFF",
            font=label_font,
            activebackground="#6C0303",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=lambda: self.submit_scores(cou_id, stu_id)
        )
        self.submit_btn.grid(row=6, column=0, columnspan=2, pady=(15, 10), ipadx=10, ipady=3)
        self.submit_btn.bind("<Enter>", lambda e: self.submit_btn_hover_effect(e, True))
        self.submit_btn.bind("<Leave>", lambda e: self.submit_btn_hover_effect(e, False))

        self.display_stu_score(cou_id, stu_id)

    def submit_btn_hover_effect(self, event, hover_in):
        new_color = "#B30505" if hover_in else "#8D0404"
        self.submit_btn.config(background=new_color)

    def close_profile_btn_hover_effect(self, event, hover_in):
        new_color = "#B30505" if hover_in else "#8D0404"
        self.close_profile_btn.config(background=new_color)

    def display_stu_score(self, cou_id, stu_id):
        # Fetch student's scores
        stu_scores = self.main.faculty_model.get_student_scores(cou_id, stu_id)
        stu_written_score = stu_scores["score_written"]
        stu_final_project_score = stu_scores["score_project"]
        stu_examination_score = stu_scores["score_exam"]

        # Display fetched scores in entry fields
        self.written_works.insert(0, stu_written_score)
        self.final_project.insert(0, stu_final_project_score)
        self.examination.insert(0, stu_examination_score)

        self.display_stu_grades(cou_id, stu_id)

    def submit_scores(self, cou_id, stu_id):
        if self.validate_grades_submission():
            written_works = self.written_works.get().strip()
            final_project = self.final_project.get().strip()
            examination = self.examination.get().strip()

            # Convert valid inputs to integers, leave None if empty
            written_works = int(written_works) if written_works else None
            final_project = int(final_project) if final_project else None
            examination = int(examination) if examination else None

            raw_grade = self.calculate_raw_grade(written_works, final_project, examination)
            final_grade = self.calculate_final_grade(raw_grade)

            # Insert scores and update grades
            add_scores = self.main.faculty_model.submit_scores(cou_id, stu_id, written_works, final_project, examination)
            update_grades = self.main.faculty_model.update_grades(cou_id, stu_id, raw_grade, final_grade)
            if add_scores and update_grades:
                messagebox.showinfo("Success", "Scores submitted successfully")
                self.display_stu_grades(cou_id, stu_id)
            else:
                messagebox.showerror("Failed", "Failed to submit scores")

    def validate_grades_submission(self):
        try:
            # Get and strip input values
            written_works = self.written_works.get().strip()
            final_project = self.final_project.get().strip()
            examination = self.examination.get().strip()

            # Ensure no field is empty
            if not written_works or not final_project or not examination:
                messagebox.showwarning("Input Error", "All fields must be filled.")
                return False

                # Ensure all fields contain only digits
            if not written_works.isdigit() or not final_project.isdigit() or not examination.isdigit():
                messagebox.showwarning("Input Error", "Only numeric values are allowed.")
                return False

                # Convert to integers
            written_works = int(written_works)
            final_project = int(final_project)
            examination = int(examination)

            # Validate ranges
            if not (0 <= written_works <= 200):
                messagebox.showwarning("Input Error", "Written Works must be between 0 and 100.")
                return False
            if not (0 <= final_project <= 100):
                messagebox.showwarning("Input Error", "Final Project must be between 0 and 100.")
                return False
            if not (0 <= examination <= 150):
                messagebox.showwarning("Input Error", "Examination must be between 0 and 150.")
                return False

            return True  # Validation successful
        except Exception as e:
            messagebox.showerror("Validation Error", f"An error occurred: {e}")
            return False

    def calculate_raw_grade(self, written_works, final_project, examination):
        try:
            written_works = int(written_works)
            final_project = int(final_project)
            examination = int(examination)
        except ValueError:
            return "Submit all scores to generate"

        # raw_grade = (written_works + final_project + (examination / 150 * 100)) / 3
        raw_grade = ((written_works / 200) * 50) + ((final_project / 100) * 30) + ((examination / 150) * 20)
        return round(raw_grade, 2)

    def calculate_final_grade(self, raw_grade):
        # Determine final grade based on raw grade
        if raw_grade >= 98:
            return 1.00
        elif raw_grade >= 91:
            return 1.25
        elif raw_grade >= 85:
            return 1.50
        elif raw_grade >= 79:
            return 1.75
        elif raw_grade >= 73:
            return 2.00
        elif raw_grade >= 67:
            return 2.25
        elif raw_grade >= 61:
            return 2.50
        elif raw_grade >= 55:
            return 2.75
        elif raw_grade >= 50:
            return 3.00
        else:
            return 5.00

    def display_stu_grades(self, cou_id, stu_id):
        grades = self.main.faculty_model.get_student_grades(cou_id, stu_id)
        if grades:
            raw_grade = grades["raw_grade"]
            final_grade = grades["final_grade"]

            self.raw_grade.configure(text=raw_grade)
            self.final_grade.configure(text=final_grade)

    def get_pfp_path(self, PFP_DIR, stu_id):
        pfp_path = PFP_DIR / f"student_{stu_id}.png"
        default_pfp = PFP_DIR / "student_default.png"
        return pfp_path if pfp_path.exists() else default_pfp

    def make_pfp_circle(self, pfp_path):
        size = (100, 100)
        pfp = Image.open(pfp_path).convert("RGBA")
        pfp = pfp.resize(size, Image.Resampling.LANCZOS) # Open image and ensure transparency support

        # Create circular mask
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((1, 1, size[0] - 1, size[1] - 1), fill=255)  # Draw a filled circle

        # Apply the mask
        circular_pfp = Image.new("RGBA", size, (0, 0, 0, 0)) # Transparent BG
        circular_pfp.paste(pfp, (0, 0), mask)

        border_draw = ImageDraw.Draw(circular_pfp)
        border_draw.ellipse((1, 1, size[0] - 1, size[1] - 1), outline="#8D0404", width=3)

        return ImageTk.PhotoImage(circular_pfp)