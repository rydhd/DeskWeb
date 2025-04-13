import tkinter as tk
from tkinter import ttk, messagebox, font


class ViewFacultyStudents(tk.Toplevel):
    def __init__(self, admin_landing, main, fac_full_name, fac_assigned_course, fac_students, fac_id):
        super().__init__(admin_landing)
        self.main = main
        self.fac_full_name = fac_full_name
        if fac_assigned_course == "None":
            self.fac_assigned_course = "Not assigned"
        else:
            self.fac_assigned_course = fac_assigned_course
        self.fac_students = fac_students
        self.fac_id = fac_id
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.title("Faculty Students")
        self.geometry("600x500+350+80")
        self.resizable(False, False)

        # Main frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas
        self.canvas = tk.Canvas(self.main_frame, bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Faculty name & Course
        self.canvas.create_text(30, 20, text=self.fac_full_name, font=("Lexend Deca", 20, "bold"), fill="#8D0404",
                                        anchor=tk.NW)
        self.canvas.create_text(30, 50, text=self.fac_assigned_course, font=("Lexend Deca", 12, "bold"), fill="#020202",
                                        anchor=tk.NW)

        # Fonts
        header_font = font.Font(family="Lexend Deca", size=10, weight="bold")
        row_font = font.Font(family="Lexend Deca", size=10)

        # === Fake Header Frame ===
        fac_stu_header_height = 30
        self.fac_stu_header_frame = tk.Frame(
            self,
            bg="#8D0404",
            width=540,
            height=fac_stu_header_height
        )
        self.fac_stu_header_frame.pack_propagate(False)

        # === Custom Labels as Fake Headings ===
        tk.Label(self.fac_stu_header_frame, text="#", fg="#FFFFFF", bg="#8D0404",
                 font=header_font, width=5, anchor="center").pack(side="left", padx=0)
        tk.Label(self.fac_stu_header_frame, text="Student Name", fg="#FFFFFF", bg="#8D0404",
                 font=header_font, width=26, anchor="center").pack(side="left", padx=0)
        tk.Label(self.fac_stu_header_frame, text="Student ID", fg="#FFFFFF", bg="#8D0404",
                 font=header_font, width=16, anchor="center").pack(side="left", padx=0)
        tk.Label(self.fac_stu_header_frame, text="", fg="#FFFFFF", bg="#8D0404",
                 font=header_font, width=11, anchor="center").pack(side="left", padx=0)

        # === Place Header Frame ===
        header_x = 30
        header_y = 80
        self.fac_stu_header_frame.place(x=header_x, y=header_y)

        # === Treeview ===
        self.faculty_stu_list = ttk.Treeview(
            self,
            columns=("count", "stu_full_name", "stu_id", "remove"),
            show="headings",
            height=16
        )

        # Headings (keep them empty)
        self.faculty_stu_list.heading("count", text="")
        self.faculty_stu_list.heading("stu_full_name", text="")
        self.faculty_stu_list.heading("stu_id", text="")
        self.faculty_stu_list.heading("remove", text="")

        # Column widths (match fake header label widths)
        self.faculty_stu_list.column("count", anchor="center", width=50)
        self.faculty_stu_list.column("stu_full_name", anchor="w", width=250)
        self.faculty_stu_list.column("stu_id", anchor="center", width=128)
        self.faculty_stu_list.column("remove", anchor="center", width=110)

        self.faculty_stu_list.tag_configure("row", font=row_font)

        # Place Treeview under header
        tree_x = header_x
        tree_y = header_y + 8
        self.faculty_stu_list.place(x=tree_x, y=tree_y)
        self.faculty_stu_list.bind("<ButtonRelease-1>", self.remove_student)
        self.fac_stu_header_frame.lift()

        self.display_faculty_students(self.fac_students)

        # Close button
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
            command=self.close
        )
        self.close_btn.place(x=462, y=450)
        self.close_btn.bind("<Enter>", lambda e: self.close_btn_hover_effect(e, True))
        self.close_btn.bind("<Leave>", lambda e: self.close_btn_hover_effect(e, False))

    def close_btn_hover_effect(self, event, hover_in):
        new_color = "#B30505" if hover_in else "#8D0404"
        self.close_btn.config(background=new_color)

    def display_faculty_students(self, fac_students):
        if fac_students:
            i = 1
            for student in fac_students:
                self.faculty_stu_list.insert("", "end",
                                             values=(i, f"        {student["stu_full_name"]}", f"AU{student["stu_id"]}", "Remove"), tags="row")
                i += 1
        else:
            if hasattr(self, 'fac_stu_header_frame'):
                self.fac_stu_header_frame.destroy()

            if hasattr(self, 'faculty_stu_list'):
                self.faculty_stu_list.destroy()

            tk.Label(self, text="No student enrolled at the moment", font=("Lexend Deca", 10, "bold")).place(relx=0.5,rely=0.5, anchor="center")

    def remove_student(self, event):
        selected_row = self.faculty_stu_list.identify_row(event.y)
        column_id = self.faculty_stu_list.identify_column(event.x)

        REMOVE_COLUMN_INDEX = 4
        if int(column_id[1:]) == REMOVE_COLUMN_INDEX:
            values = self.faculty_stu_list.item(selected_row, "values")
            if values:
                stu_id = values[2][2:]  # Remove "AU" prefix
                confirm = messagebox.askyesno("Confirm", f"Are you sure you want to remove student {values[1]}?")

                if confirm:
                    cou_id = self.main.admin_model.get_course_id_by_faculty(self.fac_id)
                    result = self.main.admin_model.remove_faculty_student(cou_id, stu_id)
                    if result:
                        self.faculty_stu_list.delete(selected_row)
                        messagebox.showinfo("Success", "Student successfully removed.")
                        self.refresh_fac_stu_list()
                    else:
                        messagebox.showerror("Error", "Failed to remove student.")

    def refresh_fac_stu_list(self):
        updated_fac_student = self.main.admin_model.get_faculty_students(self.fac_id)
        for row in self.faculty_stu_list.get_children():
            self.faculty_stu_list.delete(row)
        self.display_faculty_students(updated_fac_student)

    def close(self):
        self.destroy()