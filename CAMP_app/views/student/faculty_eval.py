import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from pathlib import Path
from PIL import ImageTk, Image, ImageDraw
from PIL.ImageOps import expand


class FacultyEvalView(tk.Toplevel):
    def __init__(self, parent, main, student_data, stu_id, faculty_id,faculty_name,course_name,on_submit=None):
        super().__init__(parent)
        self.main = main
        self.student_data = student_data
        self.stu_id = stu_id
        self.faculty_id = faculty_id
        self.faculty_name_text = faculty_name
        self.course_name_text = course_name
        self.on_submit = on_submit

        self.geometry("400x355")
        self.title("Faculty Eval")
        self.resizable(False, False)
        self.config(bd=0, highlightthickness=0)

        # Make this window modal
        self.grab_set()  # Prevents interaction with other windows
        self.transient(parent)  # Associates this window with the parent
        self.wait_visibility()  # Ensures the window is fully drawn before proceeding

        # Define the Labels
        self.faculty_name_label = ctk.CTkLabel(self, text=self.faculty_name_text,
                                               font=("Lexend Deca", 20, "bold"),
                                               text_color="#8D0404")
        self.faculty_name_label.pack(pady=3,padx=5)

        self.course_name_label = ctk.CTkLabel(self, text=self.course_name_text,
                                              font=("Lexend Deca", 14, "normal"),
                                              text_color="#9AA6B2")
        self.course_name_label.pack(pady=1,padx=5)

        self.create_widgets()

    def create_widgets(self):
        """Creates form fields for faculty evaluation input."""
        ctk.CTkLabel(self, text="Overall Performance",
                     font=("Lexend Deca", 14, "normal"),
                     text_color="#8D0404").place(x=5,y=60)

        self.rating_frame = tk.Frame(self)
        self.rating_frame.pack(pady=15)

        self.rating = tk.IntVar(value=0)
        self.stars = []
        self.rating_labels = []

        rating_texts = ["Poor", "Fair", "Good", "Excellent", "Superb"]

        for i in range(5):
            star_col = tk.Frame(self.rating_frame, width=20)
            star_col.grid(row=1, column=i, padx=5, sticky="n")

            label = tk.Label(star_col,
                             text=rating_texts[i],
                             font=("Lexend Deca", 8),
                             fg="black",
                             foreground="#8D0404",
                             justify="center",
                             wraplength=70,
                             width=8)
            label.pack(pady=(0, 4))
            self.rating_labels.append(label)

            star_btn = ctk.CTkButton(star_col,
                                     text="☆",
                                     font=("Arial", 18),
                                     fg_color="#FFFFFF",
                                     text_color="#FFD700",
                                     hover_color="#E6E6E6",
                                     width=36, height=36,
                                     corner_radius=6,
                                     command=lambda i=i + 1: self.set_rating(i))
            star_btn.pack()
            self.stars.append(star_btn)

        # Comment Field
        self.comment_entry = ctk.CTkTextbox(self, width=328, height=80,
                                            fg_color="#D3D3D3", text_color="gray")
        self.comment_entry.pack(pady=5)
        self.placeholder = "Enter your comment here..."
        self.comment_entry.insert("1.0", self.placeholder)
        self.comment_entry.bind("<FocusIn>", self.clear_placeholder)
        self.comment_entry.bind("<FocusOut>", self.add_placeholder)

        submit_button = ctk.CTkButton(self, text="Submit",
                                      command=self.add_eval, fg_color="#8D0404")
        submit_button.pack(pady=10)

    def set_rating(self, value):
        """Updates the star rating display and rating label highlight."""
        self.rating.set(value)

        for i in range(5):
            if i < value:
                self.stars[i].configure(text="★", fg_color="#FFFFFF")
                self.rating_labels[i].config(fg="#8D0404", font=("Lexend Deca", 9, "bold"))
            else:
                self.stars[i].configure(text="☆", fg_color="#FFFFFF")
                self.rating_labels[i].config(fg="black", font=("Lexend Deca", 8))

    def add_eval(self):
        """Collects input and submits the evaluation."""
        student_id = self.stu_id
        faculty_id = self.faculty_id
        eval_rating = self.rating.get()
        eval_comment = self.comment_entry.get("1.0", tk.END).strip()

        # Validate comment
        if not eval_comment or eval_comment == self.placeholder:
            messagebox.showerror("Error", "Please enter a comment before submitting.")
            return

        try:
            eval_rating = float(eval_rating)
            if eval_rating < 1 or eval_rating > 5:
                messagebox.showerror("Error", "Rating must be between 1 and 5.")
                return
        except ValueError:
            messagebox.showerror("Error", "Rating must be a number.")
            return

        print(
            f"Adding evaluation: student_id={student_id}, faculty_id={faculty_id}, rating={eval_rating}, comment={eval_comment}")

        insert_eval = self.main.student_model.add_eval(student_id, faculty_id, eval_rating, eval_comment)

        if insert_eval:
            messagebox.showinfo("Success", f"Successfully evaluated {self.faculty_name_text}")
            if self.on_submit:
                self.on_submit()
            self.destroy()
        else:
            messagebox.showerror("Error", f"{self.faculty_name_text} already evaluated")
            self.destroy()

    def clear_placeholder(self, event):
        """Clears the placeholder when the user clicks inside the textbox."""
        if self.comment_entry.get("1.0", "end").strip() == self.placeholder:
            self.comment_entry.delete("1.0", "end")
            self.comment_entry.configure(text_color="#8D0404")

    def add_placeholder(self, event):
        """Restores the placeholder if the textbox is empty when losing focus."""
        if not self.comment_entry.get("1.0", "end").strip():
            self.comment_entry.insert("1.0", self.placeholder)
            self.comment_entry.configure(text_color="gray")
