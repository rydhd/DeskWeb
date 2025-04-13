import ctypes
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from tkinter import messagebox, font
from PIL import Image, ImageTk
import customtkinter as ctk
from customtkinter import CTkImage


# Content Frames
from CAMP_app.views.student.student_courses import StudentCoursesTab
from CAMP_app.views.student.student_profile import StudentProfileTab
from CAMP_app.views.student.student_schedule import StudentScheduleTab


class StudentLanding(tk.Toplevel):
    def __init__(self, main, student_session):
        super().__init__()
        self.main = main
        self.student_session = student_session
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.title("Student Landing")
        self.geometry("1000x600+120+20")
        self.resizable(False, False)
        self.config(bd=0, highlightthickness=0)
        self.style = ttk.Style()
        BASE_DIR = Path(__file__).resolve().parent.parent.parent

        # Images directory
        self.IMAGES_DIR = BASE_DIR / "static/images"

        icon_path = self.IMAGES_DIR / "CAMPLogoWhiteIcon.ico"
        self.iconbitmap(default=icon_path)

        FONTS_DIR = BASE_DIR / "static/fonts"
        FONT_PATH = FONTS_DIR / "LexendDeca-Bold.ttf"

        # Main Frame
        self.main_frame = tk.Frame(self)
        self.main_frame.columnconfigure(0, minsize=140)
        self.main_frame.columnconfigure(1, weight=440)
        self.main_frame.rowconfigure(0, minsize=1000)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.dict_frames = {}
        self.content_frames = (StudentProfileTab, StudentCoursesTab, StudentScheduleTab)

        for CF in self.content_frames:
            frame = CF(self.main_frame, self.main, self)
            self.dict_frames[CF.__name__] = frame
            frame.grid(row=0, column=1, sticky=tk.NSEW)

            # 👇 Assign references for later use
            if CF.__name__ == "StudentCoursesTab":
                self.courses_tab = frame
            elif CF.__name__ == "StudentScheduleTab":
                self.schedule_tab = frame

        # Sidebar Frame
        self.sidebar = tk.Frame(self.main_frame, width=150, height=1000)
        self.sidebar.grid(row=0, column=0, sticky=tk.NSEW)
        self.sidebar.pack_propagate(False)

        # Canvas for sidebar
        self.sidebar_canvas = tk.Canvas(self.sidebar, bg="#8D0404",bd=0,highlightthickness=0)
        self.sidebar_canvas.pack(fill=tk.BOTH, expand=True)

        # CAMP Logo
        camp_logo_path = self.IMAGES_DIR / "CAMPLogoWhiteTypography.png"
        camp_logo = Image.open(camp_logo_path)
        camp_logo = camp_logo.resize((100, 35), Image.Resampling.LANCZOS)
        self.camp_logo = ImageTk.PhotoImage(camp_logo)
        self.sidebar_canvas.create_image(20, 20, image=self.camp_logo, anchor=tk.NW)

        # Student username
        icon_student_path = self.IMAGES_DIR / "ProfileIcon.png"
        icon_student = Image.open(icon_student_path)
        icon_student = icon_student.resize((50, 50), Image.Resampling.LANCZOS)
        self.icon_student = ImageTk.PhotoImage(icon_student)
        self.sidebar_canvas.create_image(45, 90, image=self.icon_student, anchor=tk.NW)
        self.sidebar_canvas.create_text(80, 150, text=self.student_session["stu_full_name"], font=("Lexend Deca",8),
                                        fill="#FFFFFF", anchor="center")
        self.sidebar_canvas.create_text(55, 159, text="Student", font=("Lexend Deca",6) , fill="#FFFFFF", anchor=tk.NW)

        self.button_images = {
            'StudentProfile': {
                'active': self.load_image("ProfileButtonActive.png", size=(145, 70)),
                'inactive': self.load_image("ProfileButton.png", size=(140, 70))
            },
            'StudentCourses': {
                'active': self.load_image("CoursesButtonActive.png", size=(145, 70)),
                'inactive': self.load_image("CoursesButton.png", size=(140, 70))
            },
            'StudentSchedule': {
                'active': self.load_image("ScheduleButtonActive.png", size=(145, 70)),
                'inactive': self.load_image("ScheduleButton.png", size=(140, 70))
            }
        }

        # Profile Button Tab
        self.profile_btn = ctk.CTkButton(
            self.sidebar, width=145, height=60, border_width=0, corner_radius=0, text="",
            image=self.button_images['StudentProfile']['inactive'],
            fg_color="#8D0404",
            hover=False,
            command=lambda: self.display_frame("StudentProfileTab")
        )
        self.profile_btn.place(x=0, y=180)

        # Course Button Tab
        self.course_btn = ctk.CTkButton(
            self.sidebar, width=145, height=60, border_width=0, corner_radius=0, text="",
            image=self.button_images['StudentCourses']['inactive'],
            fg_color="#8D0404",
            hover=False,
            command=lambda: self.display_frame("StudentCoursesTab")
        )
        self.course_btn.place(x=0, y=250)

        # Schedule Button Tab
        self.sched_btn = ctk.CTkButton(
            self.sidebar, width=145, height=60, border_width=0, corner_radius=0, text="",
            image=self.button_images['StudentSchedule']['inactive'],
            fg_color="#8D0404",
            hover=False,
            compound="left",
            command=lambda: self.display_frame("StudentScheduleTab")
        )
        self.sched_btn.place(x=0, y=320)

        logout_img = self.load_image("LogOutButton.png", size=(134, 20))
        self.logout_btn = ctk.CTkButton(
            self.sidebar,
            border_width=0,corner_radius=0,
            width=125,
            hover = False,
            image=logout_img,
            anchor="center",
            text="",
            fg_color="#8D0404",
            command=self.log_out
        )

        self.logout_btn.place(x=3, y=550)

        # Show the profile tab by default when logging in
        self.display_frame("StudentProfileTab")

    def display_frame(self, frame_name):
        # Reset all buttons to inactive images
        self.profile_btn.configure(image=self.button_images['StudentProfile']['inactive'])
        self.course_btn.configure(image=self.button_images['StudentCourses']['inactive'])
        self.sched_btn.configure(image=self.button_images['StudentSchedule']['inactive'])

        if frame_name and frame_name in self.dict_frames:
            # Activate the selected button
            if frame_name == "StudentProfileTab":
                self.profile_btn.configure(image=self.button_images['StudentProfile']['active'])
            elif frame_name == "StudentCoursesTab":
                self.course_btn.configure(image=self.button_images['StudentCourses']['active'])
            elif frame_name == "StudentScheduleTab":
                self.sched_btn.configure(image=self.button_images['StudentSchedule']['active'])

            # Show the selected frame
            self.dict_frames[frame_name].lift()

    def on_close(self):
        confirm = messagebox.askyesno("Exit", "Are you sure you want to close the application? You will be logged out.")

        if confirm:
            self.main.clear_user_session("Student")  # Log out the user
            self.destroy()  # Close the dashboard
            self.main.destroy()  # Stop the entire application

    def log_out(self):
        confirm = messagebox.askyesno("Log Out", "Are you sure you want to log out?")

        if confirm:
            self.main.clear_user_session("Student") # Clear the admin session
            self.destroy() # Close the dashboard
            self.main.deiconify() # Display the home screen

    def load_image(self, filename, size=(130, 60)):
        """Helper method to load and resize images."""
        path = self.IMAGES_DIR / filename
        image = Image.open(path).resize(size, Image.Resampling.LANCZOS)
        return CTkImage(light_image=image, dark_image=image, size=size)


