import tkinter as tk
from tkinter import messagebox, font
from tkcalendar import DateEntry
from datetime import datetime



class AdmitStudent(tk.Toplevel):
    def __init__(self, main, parent):
        super().__init__(parent)
        self.main = main
        self.admin_dashboard = parent

        self.title("Admit Student")
        self.geometry("932x320+155+180")
        self.resizable(False, False)

        self.main_frame = tk.Frame(self, bg="#FFFFFF")
        self.main_frame.pack(fill="both", expand=True)

        self.fields_max_length = {
            "First Name": 50,
            "Middle Name": 20,
            "Last Name": 50,
            "Username": 50,
            "Password": 10,
            "Phone": 11,
            "LRN": 12,
            "Citizenship": 30,
            "Email": 50,
            "Religion": 70,
            "Address": 150,
        }
        
        lbl_font = font.Font(family="Lexend Deca", size=10, weight="bold")
        entry_font = font.Font(family="Lexend Deca", size=8)

        # Header
        tk.Label(self.main_frame, text="Student Admission Form", font=("Lexend Deca", 20, "bold"), fg="#FFFFFF", bg="#8D0404").pack(fill="x", expand=True, anchor="nw")


        # First name
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

        # Religion
        tk.Label(self.main_frame, text="Religion", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=20, y=214)
        self.religion = tk.Entry(
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
        self.religion.place(x=20, y=238)

        # Citizenship
        tk.Label(self.main_frame, text="Citizenship", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=250, y=55)
        self.citizenship = tk.Entry(
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
        self.citizenship.place(x=252, y=78)

        # LRN
        tk.Label(self.main_frame, text="LRN", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=250, y=108)
        self.lrn = tk.Entry(
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
        self.lrn.place(x=252, y=131)

        # Phone
        tk.Label(self.main_frame, text="Phone Number", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=250, y=161)
        self.phone = tk.Entry(
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
        self.phone.place(x=252, y=184)

        # Email
        tk.Label(self.main_frame, text="Email", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=250, y=214)
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
        self.email.place(x=252, y=237)

        # Sex
        sex_lbl = tk.Label(self.main_frame, text="Sex", font=lbl_font, fg="#020202", bg="#FFFFFF")
        sex_lbl.place(x=480, y=55)
        sex_lbl.lower()
        self.sex_var = tk.StringVar()
        self.sex_var.set("Select \u25BE")
        self.sex_dropdown = tk.OptionMenu(self.main_frame, self.sex_var, "Female", "Male")

        # Dropdown design
        self.sex_dropdown.config(
            font=("Lexend Deca", 5, "bold"),
            bg="#FFFFFF",
            fg="#020202",
            activebackground="#E0E0E0",
            activeforeground="#020202",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#020202",
            bd=1,
            padx=72,
        )

        menu = self.sex_dropdown["menu"]
        menu.config(
            font=entry_font,
            bg="#FFFFFF",
            fg="#020202",
            activebackground="#8D0404",
            activeforeground="#FFFFFF",
            bd=0,
            tearoff=0
        )
        self.sex_dropdown.place(x=482, y=78)
        self.sex_dropdown.lift()

        # Birthdate
        tk.Label(self.main_frame, text="Birthdate", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=710, y=55)
        self.birthdate = DateEntry(
            self.main_frame,
            width=25,
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
        self.birthdate.place(x=712, y=78)
        self.birthdate.delete(0, tk.END)

        # Username
        tk.Label(self.main_frame, text="Username", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=480, y=108)
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
        self.username.place(x=482, y=131)

        # Password
        tk.Label(self.main_frame, text="Password", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=710, y=108)
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
        self.password.place(x=712, y=131)

        # Address
        tk.Label(self.main_frame, text="Address", font=lbl_font, fg="#020202", bg="#FFFFFF").place(x=480, y=161)
        self.address = tk.Text(
            self.main_frame,
            width=61,
            height=4.48,
            bg="#FFFFFF",
            fg="#020202",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#020202",
            highlightcolor="#8D0404",
            insertbackground="#020202",
            font=entry_font
        )
        self.address.place(x=482, y=184)

        # Admit Button
        self.admit_btn = tk.Button(
            self.main_frame,
            width=14,
            text="Admit Student",
            bg="#8D0404",
            fg="#FFFFFF",
            font=("Lexend Deca", 8, "bold"),
            activebackground="#6C0303",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.validate_student_admission
        )
        self.admit_btn.place(x=810, y=274)
        self.admit_btn.bind("<Enter>", lambda e: self.admit_btn_hover_effect(e, True))
        self.admit_btn.bind("<Leave>", lambda e: self.admit_btn_hover_effect(e, False))

        # Close Button
        self.close_btn = tk.Button(
            self.main_frame,
            width= 14,
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
        self.close_btn.place(x=675, y=274)
        self.close_btn.bind("<Enter>", lambda e: self.close_btn_hover_effect(e, True))
        self.close_btn.bind("<Leave>", lambda e: self.close_btn_hover_effect(e, False))

    def close_btn_hover_effect(self, event, hover_in):
        new_color = "#B30505" if hover_in else "#8D0404"
        self.close_btn.config(background=new_color)

    def admit_btn_hover_effect(self, event, hover_in):
        new_color = "#B30505" if hover_in else "#8D0404"
        self.admit_btn.config(background=new_color)

    def validate_student_admission(self):
        errors = []
        email_domains = ("@email.com", "@gmail.com", "@yahoo.com", "@mail.com")

        # Collect all field values into a dictionary
        data = {
            "First Name": self.first_name.get().strip(),
            "Middle Name": self.middle_name.get().strip(),  # Optional
            "Last Name": self.last_name.get().strip(),
            "Sex": self.sex_var.get(),
            "Address": self.address.get("1.0", tk.END).strip(),
            "Citizenship": self.citizenship.get().strip(),
            "LRN": self.lrn.get().strip(),
            "Phone": self.phone.get().strip(),
            "Email": self.email.get().strip(),
            "Birthdate": self.birthdate.get().strip(),
            "Religion": self.religion.get().strip(),
            "Username": self.username.get().strip(),
            "Password": self.password.get().strip()
        }

        # Check if all fields except Middle Name are empty
        if all(not value for key, value in data.items() if key != "Middle Name"):
            messagebox.showerror("Input Error", "All fields can't be empty (Except Middle Name)")
            return

        # Check if any required field is empty (excluding Middle Name)
        if any(not value for key, value in data.items() if key != "Middle Name"):
            messagebox.showerror("Input Error", "Fields cannot be empty (Except Middle Name)")
            return

        # Check for max length violations
        for field, value in data.items():
            if field in self.fields_max_length and len(value) > self.fields_max_length[field]:
                errors.append(f"{field} exceeds {self.fields_max_length[field]} characters.")

        # Specific validations
        lrn = data["LRN"]
        if lrn and (not lrn.isdigit() or len(lrn) != 12):
            errors.append("LRN must be exactly 12 digits and contain only numbers.")

        phone = data["Phone"]
        if phone and (not phone.isdigit() or len(phone) != 11):
            errors.append("Phone must be exactly 11 digits and contain only numbers.")

        email = data["Email"]
        if email and not any(email.endswith(domain) for domain in email_domains):
            errors.append(f"Email must end with {', '.join(email_domains)}")

        password = data["Password"]
        if len(password) < 8:
            errors.append("Password must be at least 8 characters.")

        if data["Sex"] == "Select ▾":
            errors.append("Sex field is required.")

        # Username uniqueness check
        if self.main.admin_model.is_student_username_taken(data["Username"]):
            errors.append("Username is already taken.")

        # Birthdate age check (must be 18+)
        try:
            birth_date = datetime.strptime(data["Birthdate"], "%Y-%m-%d")
            today = datetime.today()
            age = (today - birth_date).days // 365
            if age < 18:
                errors.append("Student must be at least 18 years old.")
        except ValueError:
            errors.append("Invalid birthdate format. Use YYYY-MM-DD.")

        # Show errors or continue with admission
        if errors:
            messagebox.showerror("Input Error", "\n".join(errors))
        else:
            self.admit_student(
                data["First Name"],
                data["Middle Name"],
                data["Last Name"],
                data["Birthdate"],
                data["Sex"],
                data["Username"],
                data["Password"],
                data["Phone"],
                data["LRN"],
                data["Citizenship"],
                data["Email"],
                data["Religion"],
                data["Address"],
            )
            messagebox.showinfo("Success", "Student admitted successfully!")
            self.clear_fields()

    def admit_student(self, first_name, middle_name, last_name, birth_date, sex, username, password, phone_number, lrn, citizenship, email, religion, address):
        self.main.admin_model.admit_student(first_name, middle_name, last_name, birth_date, sex, username, password, phone_number, lrn, citizenship, email, religion, address)
        self.admin_dashboard.display_students()

    def clear_fields(self):
        self.first_name.delete(0, tk.END)
        self.middle_name.delete(0, tk.END)
        self.last_name.delete(0, tk.END)
        self.sex_var.set("Select ▾")  # Reset to default option
        self.address.delete("1.0", tk.END)
        self.citizenship.delete(0, tk.END)
        self.lrn.delete(0, tk.END)
        self.phone.delete(0, tk.END)
        self.email.delete(0, tk.END)
        self.birthdate.delete(0, tk.END)
        self.religion.delete(0, tk.END)
        self.username.delete(0, tk.END)
        self.password.delete(0, tk.END)

    def close(self):
        self.destroy()