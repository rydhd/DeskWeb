import tkinter as tk
from pathlib import Path
import os


# Import different frames to display
from CAMP_app.views.home_screen import HomeScreen
from CAMP_app.views.admin.admin_log_in import AdminLogIn
from CAMP_app.views.faculty.faculty_log_in import FacultyLogIn
from CAMP_app.views.student.student_log_in import StudentLogIn

# Import different user landing
from CAMP_app.views.admin.admin_landing import AdminLanding
from CAMP_app.views.faculty.faculty_landing import FacultyLanding
from CAMP_app.views.student.student_landing import StudentLanding

# Import user models
from CAMP_app.models.admin_model import AdminModel
from CAMP_app.models.faculty_model import FacultyModel
from CAMP_app.models.student_model import StudentModel


class Main(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("CAMP")
        self.geometry("1000x600+120+20")
        self.resizable(False, False)
        self.config(bd=0, highlightthickness=0)

        BASE_DIR = Path(__file__).resolve().parent.parent.parent

        # Images directory
        self.IMAGES_DIR = BASE_DIR / "static/images"
        icon_path = os.path.join(os.path.dirname(__file__), "static", "images", "CAMPLogoWhiteIcon.ico")
        self.iconbitmap(icon_path)

        # For users authentication
        from CAMP_app.controllers.user_auth import UserAuth
        self.user_auth = UserAuth(self)

        # Centralized database connection
        from CAMP_app.models.database import Database
        self.db = Database()
        self.admin_model = AdminModel(self.db)
        self.faculty_model = FacultyModel(self.db)
        self.student_model = StudentModel(self.db)

        # Serves as the main container
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Dict to store frames and accessibility
        self.dict_frames = {}

        # Users session
        self.admin_session = None
        self.faculty_session = None
        self.student_session = None

        # Tuple to store frames
        self.home_screen_frames = (HomeScreen, AdminLogIn, FacultyLogIn, StudentLogIn)

        # Iterate tuple_frame
        for F in self.home_screen_frames:
            frame = F(self.main_frame, self) # Instantiate each class
            self.dict_frames[F.__name__] = frame # Store each instance
            #frame.grid(row=0, column=0, sticky="nsew") # Put each frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)


        # Initial landing page
        self.display_frame("HomeScreen")

    # To display different frames
    def display_frame(self, frame_name):
        frame = self.dict_frames[frame_name]
        frame.tkraise()

        # Autotmatically focus on the input field
        if frame_name == "AdminLogIn":
            frame.admin_username_entry.focus_set()
        elif frame_name == "FacultyLogIn":
            frame.faculty_username_entry.focus_set()
        elif frame_name == "StudentLogIn":
            frame.student_username_entry.focus_set()

    # Redirect user to their landing
    def open_user_landing(self, user, user_data):
        if user == "Admin":
            self.admin_session = user_data # Store user data in session
            AdminLanding(self, self.admin_session)
        elif user == "Faculty":
            self.faculty_session = user_data
            FacultyLanding(self, self.faculty_session)
        elif user == "Student":
            self.student_session = user_data
            StudentLanding(self, self.student_session)

    # Clear user's session after log out
    def clear_user_session(self, user):
        if user == "Admin":
            self.admin_session = None
        elif user == "Faculty":
            self.faculty_session = None
        elif user == "Student":
            self.student_session = None


# Runs the app
if __name__ == "__main__":
    camp = Main()
    camp.mainloop()