import datetime
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox, font, filedialog

from PIL import Image, ImageTk, ImageDraw
from tkcalendar import DateEntry


class ViewStudentProfile(tk.Toplevel):
    def __init__(self, admin_dashboard, parent, main, student_data): # parent is the AdminDashboard
        super().__init__(parent)
        self.main = main
        self.admin_dashboard = admin_dashboard
        self.student_data = student_data
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.title("Student Profile")
        self.geometry("650x480+360+100")
        self.resizable(False, False)

        # Paths
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
        IMAGES_DIR = BASE_DIR / "static/images"
        self.PFP_DIR = ROOT_DIR / "shared_assets/profile_pictures"

        # Main Frame
        self.main_frame = tk.Frame(self, bg="#FFFFFF")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.pack_propagate(False)

        # Header
        header_frame = tk.Frame(self.main_frame, bg="#8D0404", width=700, height=40)
        header_frame.place(x=0, y=0)
        header_frame.pack_propagate(False)
        tk.Label(header_frame, text="Student Profile", font=("Lexend Deca", 16, "bold"), fg="#FFFFFF",
                 bg="#8D0404", anchor="w").pack(fill="x", expand=True, padx=30)

        # Canvas
        self.canvas = tk.Canvas(self.main_frame, bd=0, highlightthickness=0, bg="#FFFFFF", width=700, height=162)
        self.canvas.place(x=0, y=40)

        # Student PFP
        pfp_path = self.get_pfp_path(self.student_data["stu_id"])
        self.pfp = self.make_pfp_circle(pfp_path)
        self.canvas.create_image(30, 20, anchor=tk.NW, image=self.pfp)

        # Upload Button
        upload_path = IMAGES_DIR / "UploadButton.png"
        upload_icon = Image.open(upload_path)
        upload_icon = upload_icon.resize((26, 26), Image.Resampling.LANCZOS)
        self.upload_icon = ImageTk.PhotoImage(upload_icon)
        self.upload_btn = self.canvas.create_image(150, 140, image=self.upload_icon)
        self.canvas.tag_bind(self.upload_btn, "<ButtonRelease-1>", self.upload_pfp)

        # Full Name
        self.canvas.create_text(180, 80, text=self.student_data["stu_full_name"], fill="#8D0404",font=("Lexend Deca", 20, "bold"), anchor="w")

        # ID
        self.canvas.create_text(180, 110, text=f"AU{self.student_data["stu_id"]}", fill="#020202",font=("Lexend Deca", 14, "bold"), anchor="w")

        # Expel Button
        self.expel_btn = tk.Button(
            self.canvas,
            width=14,
            text="Expel Student",
            bg="#8D0404",
            fg="#FFFFFF",
            font=("Lexend Deca", 6, "bold"),
            activebackground="#6C0303",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.expel_student
        )
        self.canvas.create_window(554, 110, window=self.expel_btn)
        self.expel_btn.bind("<Enter>", lambda e: self.expel_btn_hover_effect(e, True))
        self.expel_btn.bind("<Leave>", lambda e: self.expel_btn_hover_effect(e, False))

        # Line
        self.canvas.create_line(180, 134, 594, 134, fill="#D9D9D9", width=2)

        # Fonts
        lbl_font = font.Font(family="Lexend Deca", size=10, weight="bold")
        entry_font = font.Font(family="Lexend Deca", size=8)

        # Username
        tk.Label(self.main_frame, text="Username:", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=20, y=210)
        self.username = tk.Entry(
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
        self.username.place(x=110, y=213)

        # Password
        tk.Label(self.main_frame, text="Password:", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=20, y=253)
        self.password = tk.Entry(
            self,
            width=24,
            bg="#FFFFFF",
            fg="#020202",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#020202",
            highlightcolor="#8D0404",
            insertbackground="#020202",
            font=entry_font,
        )
        self.password.place(x=110, y=256)

        # Birthdate
        tk.Label(self.main_frame, text="Birthdate:", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=20, y=296)
        self.birthdate = DateEntry(
            self.main_frame,
            width=10,
            background="#8D0404",
            foreground="#FFFFFF",
            borderwidth=0,
            date_pattern="yyyy-mm-dd",
            headersbackground="#8D0404",
            headersforeground="#FFFFFF",
            selectbackground="#8D0404",
            selectforeground="#FFFFFF",
            normalbackground="#FFFFFF",
            normalforeground="#333333",
            weekendbackground="#F5F5F5",
            weekendforeground="#8D0404",
            font=("Lexend Deca", 8),
        )
        self.birthdate.place(x=110, y=299)
        self.birthdate.delete(0, tk.END) # NOTE: Initially insert the student's data

        # Phone Number
        tk.Label(self.main_frame, text="Phone Num:", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=20, y=339)
        self.phone = tk.Entry(
            self,
            width=24,
            bg="#FFFFFF",
            fg="#020202",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#020202",
            highlightcolor="#8D0404",
            insertbackground="#020202",
            font=entry_font,
        )
        self.phone.place(x=110, y=342)

        # Email Address
        tk.Label(self.main_frame, text="Email:", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=20, y=382)
        self.email = tk.Entry(
            self,
            width=24,
            bg="#FFFFFF",
            fg="#020202",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#020202",
            highlightcolor="#8D0404",
            insertbackground="#020202",
            font=entry_font,
        )
        self.email.place(x=110, y=385)

        # LRN
        tk.Label(self.main_frame, text="Student LRN:", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=320, y=210)
        self.lrn = tk.Entry(
            self,
            width=24,
            bg="#FFFFFF",
            fg="#020202",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#020202",
            highlightcolor="#8D0404",
            insertbackground="#020202",
            font=entry_font,
        )
        self.lrn.place(x=420, y=213)

        # Citizenship
        tk.Label(self.main_frame, text="Citizenship:", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=320, y=253)
        self.citizenship = tk.Entry(
            self,
            width=24,
            bg="#FFFFFF",
            fg="#020202",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#020202",
            highlightcolor="#8D0404",
            insertbackground="#020202",
            font=entry_font,
        )
        self.citizenship.place(x=420, y=256)

        # Religion
        tk.Label(self.main_frame, text="Religion:", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=320, y=296)
        self.religion = tk.Entry(
            self,
            width=24,
            bg="#FFFFFF",
            fg="#020202",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#020202",
            highlightcolor="#8D0404",
            insertbackground="#020202",
            font=entry_font,
        )
        self.religion.place(x=420, y=299)

        # Sex
        tk.Label(self.main_frame, text="Sex:", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=320, y=339)
        self.sex = ttk.Combobox(self.main_frame, values=["Female", "Male"], width=25)
        self.sex.place(x=420, y=342)

        # Address
        tk.Label(self.main_frame, text="Address:", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=320, y=382)
        self.address = tk.Text(
            self.main_frame,
            width=24,
            height=2,
            bg="#FFFFFF",
            fg="#020202",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#020202",
            highlightcolor="#8D0404",
            insertbackground="#020202",
            font=entry_font
        )
        self.address.place(x=420, y=385)

        # Update Profile Button
        self.update_btn = tk.Button(
            self.main_frame,
            width=14,
            text="Update Profile",
            bg="#8D0404",
            fg="#FFFFFF",
            font=("Lexend Deca", 8, "bold"),
            activebackground="#6C0303",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.toggle_update_btn
        )
        self.update_btn.place(x=486, y=440)
        self.update_btn.bind("<Enter>", lambda e: self.update_btn_hover_effect(e, True))
        self.update_btn.bind("<Leave>", lambda e: self.update_btn_hover_effect(e, False))

        # Mode Variable
        self.is_update_mode = False

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
            command=self.close # NOTE: Change this
        )
        self.close_btn.place(x=360, y=440)
        self.close_btn.bind("<Enter>", lambda e: self.close_btn_hover_effect(e, True))
        self.close_btn.bind("<Leave>", lambda e: self.close_btn_hover_effect(e, False))

        self.load_student_data()

    def expel_btn_hover_effect(self, event, hover_in):
        new_color = "#B30505" if hover_in else "#8D0404"
        self.expel_btn.config(background=new_color)

    def update_btn_hover_effect(self, event, hover_in):
        new_color = "#B30505" if hover_in else "#8D0404"
        self.update_btn.config(background=new_color)

    def close_btn_hover_effect(self, event, hover_in):
        new_color = "#B30505" if hover_in else "#8D0404"
        self.close_btn.config(background=new_color)

    def get_pfp_path(self, stu_id):
        pfp_path = self.PFP_DIR / f"student_{stu_id}.png"
        default_pfp = self.PFP_DIR / "student_default.png"
        return pfp_path if pfp_path.exists() else default_pfp # Checks if the file actually exists in the directory, otherwise it will return None

    def make_pfp_circle(self, pfp_path):
        size = (140, 140)
        pfp = Image.open(pfp_path).convert("RGBA")
        pfp = pfp.resize(size, Image.Resampling.LANCZOS)  # Open image and ensure transparency support

        # Create circular mask
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((1, 1, size[0] - 1, size[1] - 1), fill=255)  # Draw a filled circle

        # Apply the mask
        circular_pfp = Image.new("RGBA", size, (0, 0, 0, 0))  # Transparent BG
        circular_pfp.paste(pfp, (0, 0), mask)

        border_draw = ImageDraw.Draw(circular_pfp)
        border_draw.ellipse((1, 1, size[0] - 1, size[1] - 1), outline="#8D0404", width=3)

        return ImageTk.PhotoImage(circular_pfp)

    def upload_pfp(self, event):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")]
        )

        if not file_path:
            return  # User canceled file selection

        # Validate file extension
        valid_extensions = (".jpg", ".jpeg", ".png")
        if not file_path.lower().endswith(valid_extensions):
            messagebox.showerror("Invalid File", "Please upload a valid image file (.jpg, .jpeg, .png).")
            return

        try:
            # Define new filename and path
            new_filename = f"student_{self.student_data['stu_id']}.png"
            new_filepath = self.PFP_DIR / new_filename

            # Convert and save image as PNG
            img = Image.open(file_path).convert("RGBA")
            img.save(new_filepath, "PNG")

            # Update database with new profile picture filename
            self.main.admin_model.update_student_pfp(self.student_data["stu_id"], new_filename)

            # Reload the updated image
            self.pfp = self.make_pfp_circle(new_filepath)
            self.canvas.create_image(30, 20, anchor=tk.NW, image=self.pfp)
            self.canvas.tag_raise(self.upload_btn)
            self.canvas.image = self.pfp  # Keep reference to prevent garbage collection

            messagebox.showinfo("Success", "Profile picture updated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload profile picture: {e}")

    def load_student_data(self):
        # Map student_data keys to their corresponding widget variables
        self.field_widgets = {
            'stu_birthdate': self.birthdate,
            'stu_sex': self.sex,  # Combobox
            'stu_username': self.username,
            'stu_password': self.password,
            'stu_phone_number': self.phone,
            'stu_lrn': self.lrn,
            'stu_citizenship': self.citizenship,
            'stu_emailadd': self.email,
            'stu_religion': self.religion,
            'stu_address': self.address,  # Text widget
        }

        for key, widget in self.field_widgets.items():
            value = self.student_data.get(key, "")


            if key == 'stu_birthdate' and isinstance(value, (str, int, float)) is False:
                value = str(value)

            if isinstance(widget, tk.Entry):
                widget.insert(0, value)
                widget.config(state='disabled')  # Disable the entry

            elif isinstance(widget, tk.Text):
                widget.insert("1.0", value)
                widget.config(state='disabled')  # Disable the text widget

            elif isinstance(widget, ttk.Combobox):
                widget.set(value)
                widget.state(['disabled'])  # Disable the combobox

    def expel_student(self):
        confirm = messagebox.askyesno("Expel Student?", f"Are you sure you want to expel {self.student_data["stu_full_name"]}?")
        if confirm:
            self.main.admin_model.expel_student(self.student_data["stu_id"])
            self.admin_dashboard.display_students()
            search_bar = self.admin_dashboard.search
            if search_bar.get():
                search_bar.delete("0", tk.END)
                search_bar.focus_set()
            self.destroy()
            messagebox.showinfo("Expel Student", f"{self.student_data["stu_full_name"]} has been expelled.")

    def toggle_update_btn(self):
        if not self.is_update_mode:
            self.is_update_mode = True
            self.update_btn.config(text="Save")
            for entry in self.field_widgets.values():
                entry.config(state=tk.NORMAL)

        else:  # Save
            updated_data = self.get_fields_values()

            # Validate inputs before saving
            if self.validate_update(self.field_widgets):
                self.is_update_mode = False
                self.update_btn.config(text="Update Profile")
                self.save_changes(updated_data)

                # Disable entries
                for entry in self.field_widgets.values():
                    entry.config(state=tk.DISABLED)

                messagebox.showinfo("Student Updated", "Student Profile Updated")

    def get_fields_values(self):
        updated_data = {}

        for key, widget in self.field_widgets.items():
            if isinstance(widget, tk.Entry) or isinstance(widget, ttk.Combobox):
                updated_data[key] = widget.get()
            elif isinstance(widget, tk.Text):
                updated_data[key] = widget.get("1.0", "end-1c").strip()  # strip to remove trailing newline

        return updated_data

    def validate_update(self, fields):
        error = []

        for key, widget in fields.items():
            if isinstance(widget, tk.Text):
                value = widget.get("1.0", tk.END).strip()
            else:
                value = widget.get().strip()
            if not value:
                messagebox.showerror("Validation Error", "All fields can't be empty.")
                return None

        updated_data = {}
        for key, widget in fields.items():
            if isinstance(widget, tk.Text):
                updated_data[key] = widget.get("1.0", tk.END).strip()
            else:
                updated_data[key] = widget.get().strip()

        fields_max_length = {
            "username": 50,
            "password": 10,
            "birthdate": 10,  # Format: YYYY-MM-DD
            "phone": 11,
            "email": 50,
            "address": 150,
            "lrn": 12,
            "citizenship": 30,
            "religion": 70,
            "sex": 6,
        }

        # if self.main.admin_model.is_student_username_taken(updated_data["stu_username"]):
        #     error.append("Username is already taken.")

        if not updated_data["stu_phone_number"].isdigit() or len(updated_data["stu_phone_number"]) != 11:
            error.append("Phone must be exactly 11 digits.")

        if not any(updated_data["stu_emailadd"].endswith(domain) for domain in
                   ["@email.com", "@gmail.com", "@yahoo.com", "@mail.com"]):
            error.append("Email must end with a valid domain (@email.com, @gmail.com, etc.).")

        if not updated_data["stu_lrn"].isdigit() or len(updated_data["stu_lrn"]) != 12:
            error.append("LRN must be exactly 12 digits.")

        if updated_data["stu_sex"] not in ["Male", "Female"]:
            error.append("Sex must be either 'Male' or 'Female'.")

        for field, max_len in fields_max_length.items():
            value = updated_data.get(field, "")
            if len(value) > max_len:
                error.append(f"{field.capitalize()} exceeds max length of {max_len} characters.")

        try:
            birthdate = datetime.datetime.strptime(updated_data["stu_birthdate"], "%Y-%m-%d").date()
            today = datetime.date.today()
            age = (today - birthdate).days // 365
            if age < 18:
                error.append("Student must be at least 18 years old.")
        except ValueError:
            error.append("Birthdate must be in YYYY-MM-DD format.")

        if error:
            messagebox.showerror("Validation Error", "\n".join(error))
            return None

        return True

    def save_changes(self, updated_data):
        self.main.admin_model.update_student_profile(
            self.student_data["stu_id"],
            updated_data["stu_username"],
            updated_data["stu_password"],
            updated_data["stu_birthdate"],
            updated_data["stu_phone_number"],
            updated_data["stu_emailadd"],
            updated_data["stu_address"],
            updated_data["stu_lrn"],
            updated_data["stu_citizenship"],
            updated_data["stu_religion"],
            updated_data["stu_sex"]

        )

    def close(self):
        if self.is_update_mode:
            response = messagebox.askyesno("Unsaved Changes", "Do you want to save your changes before closing?")
            if response:
                updated_data = self.get_fields_values()
                if self.validate_update(self.field_widgets):
                    self.save_changes(updated_data)
                    messagebox.showinfo("Saved", "Changes have been saved.")
                    self.destroy()
                else:
                    return
        self.destroy()






