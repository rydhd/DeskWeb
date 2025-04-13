import ctypes
import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog
import customtkinter as ctk
from pathlib import Path
from PIL import ImageTk, Image, ImageDraw
from customtkinter import *
import re
from datetime import datetime

class StudentProfileTab(tk.Frame,):
    def __init__(self, parent, main, student_landing):
        super().__init__(parent)
        self.main = main
        self.student_landing = student_landing
        self.student_session = student_landing.student_session

        self.config(bd=0, highlightthickness=0)

        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent

        # Images directory
        self.IMAGES_DIR = BASE_DIR / "static/images"

        self.fields = [
            ("First Name", "stu_first_name"),
            ("Middle Name", "stu_middle_name"),
            ("Last Name", "stu_last_name"),
            ("Birth Date", "stu_birthdate"),
            ("Gender", "stu_sex"),
            ("Cellphone No", "stu_phone_number"),
            ("Email Address", "stu_emailadd"),
            ("Address", "stu_address"),
            ("Username", "stu_username"),
            ("Password", "stu_password"),
            ("LRN", "stu_lrn"),
            ("Citizenship", "stu_citizenship"),
            ("Religion", "stu_religion"),
        ]
        # Student pfp directory
        PFP_DIR = ROOT_DIR / "shared_assets/profile_pictures"

        FONT_DIR = BASE_DIR / "static/fonts"

        self.full_name = ttk.Label(self, text=self.student_session["stu_full_name"],foreground="#8D0404",font=("Lexend Deca",30,"bold"))
        self.full_name.place(x=200, y=105)

        self.student_id = ttk.Label(self, text=f"AU{self.student_session["stu_id"]}", foreground="#8D0404",
                                    font=("Lexend Deca",20,"bold"))
        self.student_id.place(x=200, y=158)

        self.widgets = {}
        self.edit_mode = False
        self.image_data = self.student_session.get("profile_picture", None)
        self.create_profile_view()

        # CAMP Logo
        red_bar_path = self.IMAGES_DIR / "HorizontalRedBar.png"
        red_bar = Image.open(red_bar_path)
        red_bar = red_bar.resize((1000, 120), Image.Resampling.LANCZOS)
        self.red_bar = ImageTk.PhotoImage(red_bar)


        # Red bar at the center top of the window
        self.red_bar_label = tk.Label(self, image=self.red_bar, bg="white")
        self.red_bar_label.place(x=0, y=0,width=1000, height=120)

        # Student pfp
        pfp_path = self.get_pfp_path(PFP_DIR, self.student_session["stu_id"])  # Get student pfp
        self.pfp = self.make_pfp_circle(pfp_path)
        # self.header_frame_canvas.create_image(50, 20, anchor=tk.NW, image=self.pfp)
        self.pfp_label = tk.Label(self, image=self.pfp, bg="#FFFFFF", borderwidth=0)
        self.pfp_label.image = self.pfp
        self.pfp_label.place(x=50, y=20)  # Adjust x, y for centering and floating effect

        # Create an upload button to trigger image upload
        upload_image = self.load_image("UploadButton.png",size=(20,30))
        self.upload_button = ctk.CTkButton(
            self, text="", image=upload_image,
            width=10, height=0, border_width=0, corner_radius=0,
            fg_color="#8D0404",
            hover=False,
            command=lambda: self.upload_pfp(PFP_DIR)
        )
        self.upload_button.place(x=170, y=120)

        self.update_profile_btn = ctk.CTkButton(
            self, text="UPDATE PROFILE", command=self.toggle_edit_mode,
            corner_radius=5, fg_color="#D92424", text_color="white",font=("Lexend Deca", 12,"normal")
        )
        self.update_profile_btn.place(x=700, y=550)


    def create_profile_view(self):
        ctk.CTkLabel(self, text="My Information", font=("Lexend Deca", 18, "bold"), text_color="#8D0404").place(x=45, y=200)

        for i, (label_text, key) in enumerate(self.fields):
            if i < 7:
                x_offset = 50
                label_x_gap = 150
            else:
                x_offset = 420 + 10  # ⬅️ Add 10 pixels to the right column
                label_x_gap = 130  # ⬅️ Slightly tighter gap between label and value

            y_offset = 250 + (i % 7) * 40

            ttk.Label(self, text=f"{label_text}:", font=("Lexend Deca", 12, "bold"), foreground="#9AA6B2").place(
                x=x_offset, y=y_offset
            )

            value = self.student_session.get(key, 'N/A')
            self.widgets[key] = ttk.Label(self, text=value, font=("Lexend Deca", 12), foreground="#8D0404")
            self.widgets[key].place(x=x_offset + label_x_gap, y=y_offset)

    def toggle_edit_mode(self):
        if not self.edit_mode:
            self.enable_edit_mode()
        else:
            updated_data = {
                key: (
                    widget.get() if isinstance(widget, (tk.Entry, ttk.Combobox)) else self.student_session.get(key, ''))
                for key, widget in self.widgets.items()
            }

            # Check if data has changed
            changes_made = any(
                str(updated_data[key]).strip() != str(self.student_session.get(key, '')).strip()
                for key in updated_data
            )

            if not changes_made:
                messagebox.showinfo("No Changes", "No changes were made.")
                self.disable_edit_mode()
                return

            messagebox.showinfo("Saved Changes", "The changes were saved successfully.")
            self.save_updates()

    def enable_edit_mode(self):
        for key, widget in self.widgets.items():
            widget.destroy()
        self.widgets.clear()

        for i, (label_text, key) in enumerate(self.fields):
            if i < 7:
                x_offset = 50
                label_x_gap = 150
            else:
                x_offset = 420 + 10
                label_x_gap = 130

            y_offset = 250 + (i % 7) * 40

            ttk.Label(self, text=f"{label_text}:", font=("Lexend Deca", 12, "bold"), foreground="#9AA6B2").place(
                x=x_offset, y=y_offset
            )

            if key == "stu_sex":
                gender_options = ["Male", "Female"]
                combobox = ttk.Combobox(self, values=gender_options, state="readonly")
                combobox.set(self.student_session.get(key, "Male"))
                combobox.place(x=x_offset + label_x_gap, y=y_offset)
                self.widgets[key] = combobox
            elif key in ["stu_first_name", "stu_middle_name", "stu_last_name"]:
                entry = tk.Entry(self)
                entry.insert(0, self.student_session.get(key, ''))
                entry.place(x=x_offset + label_x_gap, y=y_offset)
                self.widgets[key] = entry
                entry.bind("<KeyRelease>", self.update_full_name)
            else:
                entry = tk.Entry(self)
                entry.insert(0, self.student_session.get(key, ''))
                entry.place(x=x_offset + label_x_gap, y=y_offset)
                self.widgets[key] = entry

        self.update_profile_btn.configure(text="Save")
        self.edit_mode = True

        self.update_profile_btn.configure(text="Save")
        self.edit_mode = True

    def save_updates(self):
        updated_data = {
            key: (widget.get() if isinstance(widget, (tk.Entry, ttk.Combobox)) else self.student_session.get(key, ''))
            for key, widget in self.widgets.items()
        }

        # Validate Birthdate (Not in the future)
        birthdate_str = updated_data.get("stu_birthdate", "")
        if birthdate_str:
            try:
                birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")  # Ensure date format is YYYY-MM-DD
                today = datetime.today()
                if birthdate > today:
                    messagebox.showerror("Invalid Birthdate", "Birthdate cannot be in the future.")
                    return  # Stop saving process if invalid
            except ValueError:
                messagebox.showerror("Invalid Format", "Birthdate must be in YYYY-MM-DD format.")
                return

        # Validate Cellphone Number (11 digits, numbers only)
        phone_number = updated_data.get("stu_phone_number", "")
        if not re.fullmatch(r"\d{11}", phone_number):  # Must be exactly 11 digits
            messagebox.showerror("Invalid Phone Number",
                                 "Cellphone number must be exactly 11 digits and contain only numbers.")
            return

        # Validate Email Address (must end with @gmail.com)
        email = updated_data.get("stu_emailadd", "")
        if not re.fullmatch(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", email):
            messagebox.showerror("Invalid Email", "Email must be a valid address and end with '@gmail.com'.")
            return

        # Validate LRN (12 digits only)
        lrn = updated_data.get("stu_lrn", "")
        if not re.fullmatch(r"\d{12}", lrn):  # Must be exactly 12 digits
            messagebox.showerror("Invalid LRN", "LRN must be exactly 12 digits and contain only numbers.")
            return

        # If all validations pass, update the session data
        self.student_session.update(updated_data)

        # Destroy all widgets to ensure they are replaced
        for widget in self.widgets.values():
            widget.destroy()
        self.widgets.clear()

        self.create_profile_view()  # Recreate labels instead of input fields

        self.update_profile_btn.configure(text="UPDATE PROFILE")
        self.main.student_model.update_student_info(updated_data, self.student_session.get("stu_id"))

        self.edit_mode = False

    def get_pfp_path(self, PFP_DIR, stu_id):
        pfp_path = PFP_DIR / f"student_{stu_id}.png"
        default_pfp = PFP_DIR / "student_default.png"
        return pfp_path if pfp_path.exists() else default_pfp # Checks if the file actually exists in the directory, otherwise it will return None

    def make_pfp_circle(self, pfp_path):
        size = (150, 150)
        pfp = Image.open(pfp_path).convert("RGBA")
        pfp = pfp.resize(size, Image.Resampling.LANCZOS)  # Open image and ensure transparency support

        # Create a new image with transparency for the final result
        final_image = Image.new("RGBA", size, (255, 255, 255, 0))  # Transparent background

        # Create a red
        draw = ImageDraw.Draw(final_image)

        # Draw the red portion
        draw.polygon([(0, 0), (size[0], 0), (size[0], size[1] * 2 // 3), (0, size[1] * 2 // 3)], fill="#D21313")

        # Draw the white portion
        draw.polygon([(0, size[1] * 2 // 3), (size[0], size[1] * 2 // 3), (size[0], size[1]), (0, size[1])],
                     fill=(255, 255, 255, 255))

        # Create a circular mask for the image itself
        mask = Image.new("L", size, 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((1, 1, size[0] - 1, size[1] - 1), fill=255)

        # Paste the profile picture inside the circle (using the mask)
        final_image.paste(pfp, (0, 0), mask)

        return ImageTk.PhotoImage(final_image)

    def upload_pfp(self, PFP_DIR):
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
            new_filename = f"student_{self.student_session['stu_id']}.png"
            new_filepath = PFP_DIR / new_filename

            # Convert and save image as PNG
            img = Image.open(file_path).convert("RGBA")
            img.save(new_filepath, "PNG")

            # Update database with new profile picture filename
            self.main.student_model.update_student_pfp(self.student_session["stu_id"], new_filename)

            # Reload the updated image
            self.pfp = self.make_pfp_circle(new_filepath)
            self.pfp_label.configure(image=self.pfp)
            self.pfp_label.image = self.pfp  # Keep reference to prevent garbage collection

            messagebox.showinfo("Success", "Profile picture updated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload profile picture: {e}")

    def load_image(self, filename, size=(50, 50)):
        """Helper method to load and resize images."""
        path = self.IMAGES_DIR / filename
        image = Image.open(path).resize(size, Image.Resampling.LANCZOS)
        return CTkImage(light_image=image, dark_image=image, size=size)

    def update_full_name(self, event):
        # Get current values of the first, middle, and last names
        first_name = self.widgets["stu_first_name"].get()
        middle_name = self.widgets["stu_middle_name"].get()
        last_name = self.widgets["stu_last_name"].get()

        # Update the full name label with the concatenated names
        full_name = f"{first_name} {middle_name} {last_name}".strip()
        self.full_name.config(text=full_name)

    def disable_edit_mode(self):
        for widget in self.widgets.values():
            widget.destroy()
        self.widgets.clear()

        self.create_profile_view()
        self.update_profile_btn.configure(text="UPDATE PROFILE")
        self.edit_mode = False



