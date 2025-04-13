import tkinter as tk
from tkinter import messagebox, font


class AddFaculty(tk.Toplevel):
    def __init__(self, parent, main):
        super().__init__(parent)
        self.main = main
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.title("Add Faculty")
        self.geometry("480x320+420+160")
        self.resizable(False, False)

        # Main frame
        self.main_frame = tk.Frame(self, bg="#FFFFFF")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.fields_max_length = {
            "First Name": 50,
            "Middle Name": 30,
            "Last Name": 50,
            "Username": 50,
            "Password": 10,
            "Phone": 11,
            "Email": 50,
        }

        # Header
        tk.Label(self.main_frame, text="Add Faculty", font=("Lexend Deca", 20, "bold"), fg="#FFFFFF", bg="#8D0404").pack(fill="x", expand=True, anchor="nw")

        lbl_font = font.Font(family="Lexend Deca", size=10, weight="bold")
        entry_font = font.Font(family="Lexend Deca", size=8)

        # First Name
        tk.Label(self.main_frame, text="First Name", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=20, y=55)
        self.first_name = tk.Entry(
            self,
            width=28,
            bg="#FFFFFF",
            fg="#020202",  # Black text
            relief="flat",  # Flat border for modern look
            highlightthickness=1,  # Thin outline
            highlightbackground="#020202",  # Border color (unfocused)
            highlightcolor="#8D0404",  # Border color (focused)
            insertbackground="#020202",  # Cursor color
            font=entry_font,
        )
        self.first_name.place(x=22, y=78)

        # Middle name
        tk.Label(self.main_frame, text="Middle Name", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=20, y=108)
        self.middle_name = tk.Entry(
            self,
            width=28,
            bg="#FFFFFF",
            fg="#020202",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#020202",
            highlightcolor="#8D0404",
            insertbackground="#020202",
            font=entry_font,
        )
        self.middle_name.place(x=22, y=131)

        # Last name
        tk.Label(self.main_frame, text="Last Name", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=20, y=161)
        self.last_name = tk.Entry(
            self,
            width=28,
            bg="#FFFFFF",
            fg="#020202",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#020202",
            highlightcolor="#8D0404",
            insertbackground="#020202",
            font=entry_font,
        )
        self.last_name.place(x=22, y=184)

        # Email
        tk.Label(self.main_frame, text="Email", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=20, y=214)
        self.email = tk.Entry(
            self,
            width=28,
            bg="#FFFFFF",
            fg="#020202",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#020202",
            highlightcolor="#8D0404",
            insertbackground="#020202",
            font=entry_font,
        )
        self.email.place(x=22, y=237)

        # Phone Number
        tk.Label(self.main_frame, text="Phone Number", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=250, y=55)
        self.phone_num = tk.Entry(
            self,
            width=28,
            bg="#FFFFFF",
            fg="#020202",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#020202",
            highlightcolor="#8D0404",
            insertbackground="#020202",
            font=entry_font,
        )
        self.phone_num.place(x=252, y=78)

        # LRN
        tk.Label(self.main_frame, text="Username", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=250, y=108)
        self.username = tk.Entry(
            self,
            width=28,
            bg="#FFFFFF",
            fg="#020202",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#020202",
            highlightcolor="#8D0404",
            insertbackground="#020202",
            font=entry_font,
        )
        self.username.place(x=252, y=131)

        # Password
        tk.Label(self.main_frame, text="Password", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=250, y=161)
        self.password = tk.Entry(
            self,
            width=28,
            bg="#FFFFFF",
            fg="#020202",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#020202",
            highlightcolor="#8D0404",
            insertbackground="#020202",
            font=entry_font,
        )
        self.password.place(x=252, y=184)

        # Confirm password
        tk.Label(self.main_frame, text="Confirm Password", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=250, y=214)
        self.confirm_password = tk.Entry(
            self,
            width=28,
            bg="#FFFFFF",
            fg="#020202",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#020202",
            highlightcolor="#8D0404",
            insertbackground="#020202",
            font=entry_font,
        )
        self.confirm_password.place(x=252, y=237)

        # Add Faculty Button
        self.add_faculty_btn = tk.Button(
            self.main_frame,
            width=12,
            text="Add Faculty",
            bg="#8D0404",
            fg="#FFFFFF",
            font=("Lexend Deca", 8, "bold"),
            activebackground="#6C0303",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.validate_add_faculty
        )
        self.add_faculty_btn.place(x=360, y=274)
        self.add_faculty_btn.bind("<Enter>", lambda e: self.add_fac_btn_hover_effect(e, True))
        self.add_faculty_btn.bind("<Leave>", lambda e: self.add_fac_btn_hover_effect(e, False))

        # Close Button
        self.close_btn = tk.Button(
            self.main_frame,
            width=12,
            text="Close",
            bg="#8D0404",
            fg="#FFFFFF",
            font=("Lexend Deca", 8, "bold"),
            activebackground="#6C0303",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.close
        )
        self.close_btn.place(x=252 , y=274)
        self.close_btn.bind("<Enter>", lambda e: self.close_btn_hover_effect(e, True))
        self.close_btn.bind("<Leave>", lambda e: self.close_btn_hover_effect(e, False))

    def close_btn_hover_effect(self, event, hover_in):
        new_color = "#B30505" if hover_in else "#8D0404"
        self.close_btn.config(background=new_color)

    def add_fac_btn_hover_effect(self, event, hover_in):
        new_color = "#B30505" if hover_in else "#8D0404"
        self.add_faculty_btn.config(background=new_color)

    def validate_add_faculty(self):
        errors = []
        email_domains = ("@email.com", "@gmail.com", "@yahoo.com", "@mail.com")

        data = {
            "First Name": self.first_name.get().strip(),
            "Middle Name": self.middle_name.get().strip(),
            "Last Name": self.last_name.get().strip(),
            "Username": self.username.get().strip(),
            "Password": self.password.get().strip(),
            "Confirm Password": self.confirm_password.get().strip(),
            "Phone": self.phone_num.get().strip(),
            "Email": self.email.get().strip(),
        }

        # Check if all fields except Middle Name are empty
        if all(not value for key, value in data.items() if key != "Middle Name"):
            messagebox.showerror("Input Error", "All fields can't be empty (Except Middle Name)")
            return

        # Check if any required field is empty (excluding Middle Name)
        if any(not value for key, value in data.items() if key != "Middle Name"):
            messagebox.showerror("Input Error", "Fields cannot be empty (Except Middle Name)")
            return

        # Max length validation
        for field, value in data.items():
            if field in self.fields_max_length and len(value) > self.fields_max_length[field]:
                errors.append(f"{field} exceeds {self.fields_max_length[field]} characters.")

        # Phone validation
        phone = data["Phone"]
        if not phone.isdigit() or len(phone) != 11:
            errors.append("Phone must be exactly 11 digits and contain only numbers.")

        # Email validation
        email = data["Email"]
        if not any(email.endswith(domain) for domain in email_domains):
            errors.append(f"Email must end with {', '.join(email_domains)}")

        # Password match and length check
        password = data["Password"]
        confirm_password = data["Confirm Password"]
        if password != confirm_password:
            errors.append("Passwords do not match.")
        elif len(password) < 8:
            errors.append("Password must be at least 8 characters.")

        # Check if username is already taken
        if self.main.admin_model.is_faculty_username_taken(data["Username"]):
            errors.append("Username is already taken.")

        # Show error messages or proceed
        if errors:
            messagebox.showerror("Input Error", "\n".join(errors))
        else:
            result = self.main.admin_model.add_faculty(
                data["Username"],
                data["Password"],
                data["First Name"],
                data["Middle Name"],
                data["Last Name"],
                data["Email"],
                data["Phone"]
            )
            if result:
                messagebox.showinfo("Success", "Faculty added successfully!")
                self.clear_fields()
            else:
                messagebox.showerror("Error", "Failed to add faculty. Please try again.")

    def add_faculty(self):
        # Validate Fields
        validation_result = self.validate_fields()
        if validation_result is not True:
            messagebox.showerror("Validation Error", validation_result)
            return

        # Extract data from the fields and apply transformations
        first_name = self.first_name.get().strip().capitalize()
        middle_name = self.middle_name.get().strip() or None
        last_name = self.last_name.get().strip().capitalize()
        username = self.username.get().strip()
        password = self.password.get().strip()
        email = self.email.get().strip()
        phone_number = self.phone_num.get().strip()

        # Call the admin model to add faculty
        try:
            result = self.main.admin_model.add_faculty(username, password, first_name, middle_name, last_name, email,
                                                       phone_number)
            if result:
                messagebox.showinfo("Success", "Faculty added successfully!")
                self.clear_fields()
            else:
                messagebox.showerror("Error", "Failed to add faculty. Please try again.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def clear_fields(self):
        self.first_name.delete(0, 'end')
        self.middle_name.delete(0, 'end')
        self.last_name.delete(0, 'end')
        self.username.delete(0, 'end')
        self.password.delete(0, 'end')
        self.confirm_password.delete(0, 'end')
        self.email.delete(0, 'end')
        self.phone_num.delete(0, 'end')

    def validate_fields(self):
        # Field values
        fields = {
            "First Name": (self.first_name.get(), 50),
            "Middle Name": (self.middle_name.get(), 30),
            "Last Name": (self.last_name.get(), 50),
            "Username": (self.username.get(), 50),
            "Password": (self.password.get(), 10),
            "Email": (self.email.get(), 50),
            "Phone Number": (self.phone_num.get(), 11),
        }

        # Check for empty fields (except middle name)
        for field_name, (value, max_length) in fields.items():
            if field_name != "Middle Name" and not value.strip():
                return f"{field_name} cannot be empty."

            # Check for max length
            if len(value.strip()) > max_length:
                return f"{field_name} exceeds max length of {max_length} characters."

        # Email Validation
        email = self.email.get().strip()
        valid_domains = ("@email.com", "@gmail.com", "@yahoo.com", "@mail.com")
        if not any(email.endswith(domain) for domain in valid_domains):
            return "Email must end with '@email.com', '@gmail.com', '@yahoo.com', or '@mail.com'."

        # Phone Number Validation (Only Digits)
        phone_number = self.phone_num.get().strip()
        if not phone_number.isdigit():
            return "Phone Number should contain only digits."
        elif len(phone_number) != 11:
            return "Phone Number must be exactly 11 digits."

        # All validations passed
        return True

    def close(self):
        self.destroy()
