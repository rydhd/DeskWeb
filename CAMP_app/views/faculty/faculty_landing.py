import tkinter as tk
from pathlib import Path
from tkinter import font, messagebox
from PIL import Image, ImageTk

# Views
from CAMP_app.views.faculty.faculty_evaluation import FacultyEvaluation
from CAMP_app.views.faculty.faculty_students import FacultyStudents


class FacultyLanding(tk.Toplevel):
    def __init__(self, main, faculty_session):
        super().__init__()
        self.main = main
        self.faculty_session = faculty_session
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.title("Faculty")
        self.geometry("1000x600+120+20")
        self.resizable(False, False)

        # Paths
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        self.IMAGES_DIR = BASE_DIR / "static/images"
        icon_path = self.IMAGES_DIR / "CAMPLogoWhiteIcon.ico"
        self.iconbitmap(default=icon_path)

        # Main Frame
        self.main_frame = tk.Frame(self)
        self.main_frame.columnconfigure(0, minsize=140)
        self.main_frame.columnconfigure(1, weight=440)
        self.main_frame.rowconfigure(0, minsize=1000)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.dict_frames = {}
        self.content_frames = (FacultyStudents, FacultyEvaluation)

        for CF in self.content_frames:
            frame = CF(self.main_frame, self.main, self)
            self.dict_frames[CF.__name__] = frame
            frame.grid(row=0, column=1, sticky=tk.NSEW)

        # Sidebar Frame
        self.sidebar = tk.Frame(self.main_frame, width=140, height=1000)
        self.sidebar.grid(row=0, column=0, sticky=tk.NSEW)
        self.sidebar.pack_propagate(False)

        # Canvas for sidebar
        self.sidebar_canvas = tk.Canvas(self.sidebar, bg="#8D0404", bd=0, highlightthickness=0)
        self.sidebar_canvas.pack(fill=tk.BOTH, expand=True)

        # CAMP Logo
        camp_logo_path = self.IMAGES_DIR / "CAMPLogoWhiteTypography.png"
        camp_logo = Image.open(camp_logo_path)
        camp_logo = camp_logo.resize((100, 35), Image.Resampling.LANCZOS)
        self.camp_logo = ImageTk.PhotoImage(camp_logo)
        self.sidebar_canvas.create_image(20, 20, image=self.camp_logo, anchor=tk.NW)

        # Faculty username
        icon_faculty_path = self.IMAGES_DIR / "ProfileIcon.png"
        icon_faculty = Image.open(icon_faculty_path)
        icon_faculty = icon_faculty.resize((50, 50), Image.Resampling.LANCZOS)
        self.icon_faculty = ImageTk.PhotoImage(icon_faculty)
        self.sidebar_canvas.create_image(45, 90, image=self.icon_faculty, anchor=tk.NW)
        self.sidebar_canvas.create_text(55, 145, text=self.faculty_session["fac_username"], font=("Lexend Deca", 10, "bold"),
                                        fill="#FFFFFF", anchor=tk.NW)
        self.sidebar_canvas.create_text(50, 167, text="FACULTY", font=("Lexend Deca", 6), fill="#FFFFFF", anchor=tk.NW)

        # Button images dictionary
        self.button_images = {
            'FacultyStudents': {
                'active': self.load_image("StudentsButtonActive.png"),
                'inactive': self.load_image("StudentsButton.png")
            },
            'FacultyEvaluation': {
                'active': self.load_image("EvaluationButtonActive.png"),
                'inactive': self.load_image("EvaluationButton.png")
            }
        }

        # Students button tab
        self.students_btn = tk.Button(self.sidebar, width=138, height=70, borderwidth=0,
                                      image=self.button_images['FacultyStudents']['active'],
                                      command=lambda: self.display_frame("FacultyStudents"))
        self.students_btn.place(x=0, y=200)

        # Evaluation button tab
        self.evaluation_btn = tk.Button(self.sidebar, width=138, height=70, borderwidth=0,
                                        image=self.button_images['FacultyEvaluation']['inactive'],
                                        command=lambda: self.display_frame("FacultyEvaluation"))
        self.evaluation_btn.place(x=0, y=270)

        # Logout button
        logout_path = self.IMAGES_DIR / "LogOutButton.png"
        logout_img = Image.open(logout_path)
        logout_img = logout_img.resize((138, 23), Image.Resampling.LANCZOS)
        self.logout_img = ImageTk.PhotoImage(logout_img)
        self.logout_btn = tk.Button(self.sidebar, width=134, height=21, borderwidth=0, image=self.logout_img,
                                    command=self.log_out)
        self.logout_btn.place(x=2, y=550)

        self.display_frame("FacultyStudents") # NOTE:Take this back

    def load_image(self, filename):
        path = self.IMAGES_DIR / filename
        image = Image.open(path)
        image = image.resize((140, 72), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def on_close(self):
        confirm = messagebox.askyesno("Exit", "Are you sure you want to close the application? You will be logged out.")
        if confirm:
            self.main.clear_user_session("Faculty")
            self.destroy()
            self.main.destroy()

    def display_frame(self, frame_name):
        # Reset all buttons to inactive
        self.students_btn.config(image=self.button_images['FacultyStudents']['inactive'])
        self.evaluation_btn.config(image=self.button_images['FacultyEvaluation']['inactive'])

        # Set active image for the selected frame
        if frame_name == 'FacultyStudents':
            self.students_btn.config(image=self.button_images['FacultyStudents']['active'])
        elif frame_name == 'FacultyEvaluation':
            self.evaluation_btn.config(image=self.button_images['FacultyEvaluation']['active'])

        frame = self.dict_frames[frame_name]
        frame.lift()

    def log_out(self):
        confirm = messagebox.askyesno("Log Out", "Are you sure you want to log out?")
        if confirm:
            self.main.clear_user_session("Faculty")
            self.destroy()
            self.main.deiconify()