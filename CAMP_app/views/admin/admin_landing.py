import tkinter as tk
from pathlib import Path
from tkinter import font, messagebox
from PIL import Image, ImageTk

# Content Frames
from CAMP_app.views.admin.admin_dashboard import AdminDashboard
from CAMP_app.views.admin.admin_faculty import AdminFaculty
from CAMP_app.views.admin.admin_courses import AdminCourses

class AdminLanding(tk.Toplevel):
    def __init__(self, main, admin_session):
        super().__init__()
        self.main = main
        self.admin_session = admin_session
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.title("Admin Landing")
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

        # self.dict_frames = {}
        # self.content_frames = (AdminDashboard, AdminFaculty, AdminCourses)
        #
        # for CF in self.content_frames:
        #     frame = CF(self.main_frame, self.main, self)
        #     self.dict_frames[CF.__name__] = frame
        #     frame.grid(row=0, column=1, sticky=tk.NSEW)

        self.dict_frames = {}
        self.content_frames = (AdminDashboard, AdminFaculty, AdminCourses)

        # First, create a placeholder for AdminFaculty
        admin_faculty_frame = None

        for CF in self.content_frames:
            if CF.__name__ == "AdminFaculty":
                # Initialize AdminFaculty first
                frame = CF(self.main_frame, self.main, self)
                admin_faculty_frame = frame
            elif CF.__name__ == "AdminCourses":
                # Pass the AdminFaculty frame to AdminCourses
                frame = CF(self.main_frame, self.main, self, admin_faculty_frame)
            else:
                # Normal initialization
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
        camp_logo = camp_logo.resize((100,35), Image.Resampling.LANCZOS)
        self.camp_logo = ImageTk.PhotoImage(camp_logo)
        self.sidebar_canvas.create_image(20, 20, image=self.camp_logo, anchor=tk.NW)

        # Admin username
        icon_admin_path = self.IMAGES_DIR / "ProfileIcon.png"
        icon_admin = Image.open(icon_admin_path)
        icon_admin = icon_admin.resize((50,50), Image.Resampling.LANCZOS)
        self.icon_admin = ImageTk.PhotoImage(icon_admin)
        self.sidebar_canvas.create_image(45, 90, image=self.icon_admin, anchor=tk.NW)
        self.sidebar_canvas.create_text(36, 145, text=self.admin_session["adm_username"], font=("Lexend Deca", 10, "bold"), fill="#FFFFFF", anchor=tk.NW)
        self.sidebar_canvas.create_text(55, 167, text="ADMIN", font=("Lexend Deca", 6) , fill="#FFFFFF", anchor=tk.NW)

        # Button images dictionary
        self.button_images = {
            'AdminDashboard': {
                'active': self.load_image("DashboardButtonActive.png"),
                'inactive': self.load_image("DashboardButton.png")
            },
            'AdminFaculty': {
                'active': self.load_image("FacultyButtonActive.png"),
                'inactive': self.load_image("FacultyButton.png")
            },
            'AdminCourses': {
                'active': self.load_image("CoursesButtonActive.png"),
                'inactive': self.load_image("CoursesButton.png")
            }
        }

        # Dashboard button tab
        self.dashboard_btn = tk.Button(self.sidebar, width=137, height=70, borderwidth=0, image=self.button_images['AdminDashboard']['active'], command=lambda: self.display_frame("AdminDashboard"))
        self.dashboard_btn.place(x=1, y=200)

        # Faculty button tab
        self.faculty_btn = tk.Button(self.sidebar, width=137, height=70, borderwidth=0, image=self.button_images['AdminFaculty']['inactive'], command=lambda: self.display_frame("AdminFaculty"))
        self.faculty_btn.place(x=1, y=270)

        # Courses button tab
        self.courses_btn = tk.Button(self.sidebar, width=137, height=70, borderwidth=0, image=self.button_images['AdminCourses']['inactive'], command=lambda: self.display_frame("AdminCourses"))
        self.courses_btn.place(x=1, y=340)

        # Logout button
        logout_path = self.IMAGES_DIR / "LogOutButton.png"
        logout_img = Image.open(logout_path)
        logout_img = logout_img.resize((138, 23), Image.Resampling.LANCZOS)
        self.logout_img = ImageTk.PhotoImage(logout_img)
        self.logout_btn = tk.Button(self.sidebar, width=134, height=21, borderwidth=0, image=self.logout_img, command=self.log_out)
        self.logout_btn.place(x=2, y=550)

        self.display_frame("AdminDashboard") # NOTE: Take this back
        # self.display_frame("AdminCourses") # NOTE: Remove this

    def load_image(self, filename):
        path = self.IMAGES_DIR / filename
        image = Image.open(path)
        image = image.resize((141, 72), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def on_close(self):
        confirm = messagebox.askyesno("Exit", "Are you sure you want to close the application? You will be logged out.")
        if confirm:
            self.main.clear_user_session("Admin")
            self.destroy()
            self.main.destroy()

    def display_frame(self, frame_name):
        # Reset all buttons to inactive
        self.dashboard_btn.config(image=self.button_images['AdminDashboard']['inactive'])
        self.faculty_btn.config(image=self.button_images['AdminFaculty']['inactive'])
        self.courses_btn.config(image=self.button_images['AdminCourses']['inactive'])

        # Set active image for the selected frame
        if frame_name == 'AdminDashboard':
            self.dashboard_btn.config(image=self.button_images['AdminDashboard']['active'])
        elif frame_name == 'AdminFaculty':
            self.faculty_btn.config(image=self.button_images['AdminFaculty']['active'])
        elif frame_name == 'AdminCourses':
            self.courses_btn.config(image=self.button_images['AdminCourses']['active'])

        frame = self.dict_frames[frame_name]
        frame.lift()

    def log_out(self):
        confirm = messagebox.askyesno("Log Out", "Are you sure you want to log out?")
        if confirm:
            self.main.clear_user_session("Admin")
            self.destroy()
            self.main.deiconify()
