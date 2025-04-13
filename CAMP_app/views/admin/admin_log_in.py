import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from PIL import Image, ImageTk


class AdminLogIn(tk.Frame):
    def __init__(self, parent, main): # parent is a container and the controller is referenced to the main for frame switching
        super().__init__(parent) # pass the parent parameter as container
        self.main = main

        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Paths
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        IMAGES_DIR = BASE_DIR / "static/images"

        # Background
        bg_path = IMAGES_DIR / "UserLoginBG.png"  # Get the path of a specific image
        bg = Image.open(bg_path)  # Load the img file
        bg = bg.resize((1050, 650), Image.Resampling.LANCZOS)  # Resize the img
        self.bg = ImageTk.PhotoImage(bg)  # Convert into Python Object
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg)  # Put the widget

        # CAMP Red Typography
        camp_typography = IMAGES_DIR / "CAMPRedTypography.png"
        camp_typography = Image.open(camp_typography)
        camp_typography = camp_typography.resize((600, 600), Image.Resampling.LANCZOS)
        self.camp_typography = ImageTk.PhotoImage(camp_typography)
        self.canvas.create_image(0, 0, image=self.camp_typography, anchor=tk.NW)

        # Frame
        input_frame = IMAGES_DIR/ "InputFrame.png"
        input_frame = Image.open(input_frame)
        input_frame = input_frame.resize((480, 450), Image.Resampling.LANCZOS)
        self.input_frame = ImageTk.PhotoImage(input_frame)
        self.canvas.create_image(500, 120, image=self.input_frame, anchor=tk.NW)

        # CAMP Logo
        camp_logo = IMAGES_DIR / "CAMPLogoRed.png"
        camp_logo = Image.open(camp_logo)
        camp_logo = camp_logo.resize((150, 150), Image.Resampling.LANCZOS)
        self.camp_logo = ImageTk.PhotoImage(camp_logo)
        self.canvas.create_image(670, 85, image=self.camp_logo, anchor=tk.NW)


        self.canvas.create_text(600,250, anchor=tk.NW, text="Admin Username:", font=("Lexend Deca", 12, "bold"), fill="#FFFFFF")

        self.admin_username_entry = ttk.Entry(self) # pass self
        self.admin_username_entry.place(anchor=tk.NW, x=600, y=280, width=300, height=35)
        self.admin_username_entry.bind("<Return>", self.log_in)

        self.canvas.create_text(600,320, anchor=tk.NW, text="Password:", font=("Lexend Deca", 12, "bold"), fill="#FFFFFF")

        self.admin_password_entry = ttk.Entry(self, show="*") # pass self
        self.admin_password_entry.place(anchor=tk.NW, x=600, y=350, width=300, height=35)
        self.admin_password_entry.bind("<Return>", self.log_in)

        style = ttk.Style()

        style.configure(
            'btnStyle.TButton',
            font=("Lexend Deca", 12, "bold"),
            relief="solid",
            borderwidth=5,
            background="#7B1818",
            foreground="#7B1818",
            justify=tk.CENTER,
        )

        style.map(
            "btnStyle.TButton",
            background=[("active", "#5A1313"), ("pressed", "#3E0E0E"), ("!disabled", "#7B1818")],
            foreground=[("active", "#5A1313"), ("pressed", "#3E0E0E")]
        )


        self.log_in_btn = ttk.Button(self, text="Log In" , command=self.log_in, style='btnStyle.TButton')
        self.log_in_btn.place(anchor=tk.NW, x=600, y=420, width=300, height=35)
        self.log_in_btn.bind("<Return>", self.log_in)

        self.back_btn = ttk.Button(self, text="◀", command=self.back, style='btnStyle.TButton')
        self.back_btn.place(anchor=tk.NW, x=900 , y=30, width=50, height=50)

        # self.short_cut() # NOTE: Remove this

    def log_in(self, event=None):
        admin_username = self.admin_username_entry.get().strip()
        admin_password = self.admin_password_entry.get().strip()

        # If the input fields are empty
        if not admin_username or not admin_password:
            messagebox.showwarning("Login Failed", "Please make sure that Username and Password are not empty")
            return

        # Authenticate
        result = self.main.user_auth.authenticate_admin(admin_username, admin_password)

        # Successful authentication
        if result:
            # Store admin's data as session
            admin_data = {
                "adm_id": result["adm_id"],
                "adm_username": result["adm_username"],
            }
            # self.main.set_admin_session(admin_data) # Set session

            # Clear input fields
            self.admin_username_entry.delete(0, tk.END)
            self.admin_password_entry.delete(0, tk.END)

            self.main.withdraw()

            self.main.open_user_landing("Admin", admin_data)

        # Authentication failed
        else:
            messagebox.showwarning("Login Failed", "Username or Password is invalid")
            self.admin_password_entry.delete(0, tk.END)
            self.admin_password_entry.focus_set()

    def back(self):
        self.main.display_frame("HomeScreen")

        self.admin_username_entry.delete(0, tk.END)
        self.admin_password_entry.delete(0, tk.END)

    def short_cut(self): # NOTE: Remove this
        self.admin_username_entry.insert("", "emmantest")
        self.admin_password_entry.insert("", "emman123")
        self.log_in()
