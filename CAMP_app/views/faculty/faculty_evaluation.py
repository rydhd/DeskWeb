import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw


class FacultyEvaluation(tk.Frame):
    def __init__(self, parent, main, faculty_landing):
        super().__init__(parent)
        self.main = main
        self.faculty_landing = faculty_landing

        # Paths
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        self.IMAGES_DIR = BASE_DIR / "static/images"
        self.PFP_DIR = BASE_DIR / "static/student_pfps"

        self.evaluation_canvas = tk.Canvas(self, bg="#D9D9D9", bd=0, highlightthickness=0)
        self.evaluation_canvas.pack(fill=tk.BOTH, expand=True)

        # Header
        self.evaluation_canvas.create_text(20, 20, text="Evaluations", font=("Lexend Deca", 20, "bold"), fill="#8D0404", anchor=tk.NW)

        # Star
        star_path = self.IMAGES_DIR / "Star.png"
        star = Image.open(star_path)
        # Big star
        big_star = star.resize((26, 26), Image.Resampling.LANCZOS)
        self.big_star = ImageTk.PhotoImage(big_star)
        # Small start
        star = star.resize((12, 12), Image.Resampling.LANCZOS)
        self.star = ImageTk.PhotoImage(star)

        self.create_evaluation_analytics()
        self.display_evaluation_list()

    def create_evaluation_analytics(self):
        if hasattr(self, 'overall_eval_frame'):
            self.overall_eval_frame.destroy()

        if hasattr(self, 'analytics_frame'):
            self.analytics_frame.destroy()


        # Average eval rating
        fac_id = self.faculty_landing.faculty_session["fac_id"]
        avg_eval_rating = self.main.faculty_model.get_average_rating(fac_id)
        total_evaluations = self.main.faculty_model.get_total_evaluations(fac_id)

        self.overall_eval_frame = tk.Frame(self, width=140, height=90, bd=0, relief="flat")
        self.overall_eval_frame.place(x=20, y=60)
        self.overall_eval_frame.pack_propagate(False)

        self.overall_eval_canvas = tk.Canvas(self.overall_eval_frame, bg="#8D0404", bd=0, highlightthickness=0)
        self.overall_eval_canvas.pack(fill="both", expand=True)

        # Overall Label
        self.overall_eval_canvas.create_text(40, 5, text="OVERALL",
                                     font=("Lexend Deca", 10, "bold"),
                                     fill="#FFFFFF", anchor=tk.NW)

        # Evaluation Rating
        self.overall_eval_canvas.create_text(30, 30, text=avg_eval_rating,
                                             font=("Lexend Deca", 16, "bold"),
                                             fill="#FFFFFF", anchor=tk.NW)

        # Star
        self.overall_eval_canvas.create_image(80, 30, image=self.big_star, anchor=tk.NW)

        # Total eval
        self.overall_eval_canvas.create_text(36, 70, text=f"{total_evaluations} EVALUATIONS",
                                             font=("Lexend Deca", 6, "bold"),
                                             fill="#FFFFFF", anchor=tk.NW)

        self.analytics_frame = tk.Frame(self, width=140, height=140, bg="#FFFFFF", bd=0, relief="flat")
        self.analytics_frame.place(x=20, y=150)
        self.analytics_frame.pack_propagate(False)

        self.render_rating_analytics()


    # Evaluations list
    def display_evaluation_list(self):
        # Main frame container
        self.evaluation_list = tk.Frame(self, width=640, height=520, bg="#D9D9D9")
        self.evaluation_list.place(x=200, y=60)
        self.evaluation_list.pack_propagate(False)

        # Create a canvas with scrollbar
        canvas = tk.Canvas(self.evaluation_list, bg="#D9D9D9", bd=0, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.evaluation_list, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#D9D9D9")

        # Configure scrolling
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Create window in canvas that will be scrollable
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Get evaluations data
        fac_id = self.faculty_landing.faculty_session["fac_id"]
        evaluations = self.main.faculty_model.get_evaluations(fac_id)

        self.pfp_images = []  # Store references to prevent garbage collection

        # Load Trash Button image
        trash_path = self.IMAGES_DIR / "TrashButton.png"
        trash = Image.open(trash_path)
        trash = trash.resize((48, 92), Image.Resampling.LANCZOS)
        self.trash = ImageTk.PhotoImage(trash)

        if evaluations:
            for index, evaluation in enumerate(evaluations):
                eval_card = tk.Frame(scrollable_frame, height=80, width=620, bg="#FFFFFF", bd=0, relief="flat")
                eval_card.pack(fill="x", pady=2)
                eval_card.pack_propagate(False)

                eval_card_canvas = tk.Canvas(eval_card, bg="#FFFFFF", bd=0, highlightthickness=0)
                eval_card_canvas.pack(fill=tk.BOTH, expand=True)

                eval_card_canvas.create_line(0, 0, 0, 80, fill="#8D0404", width=8)

                # Student profile picture
                pfp_path = self.get_pfp_path(self.PFP_DIR, evaluation["stu_id_fk"])
                pfp = self.make_pfp_circle(pfp_path)
                self.pfp_images.append(pfp)  # Store reference
                eval_card_canvas.create_image(10, 16, image=pfp, anchor=tk.NW)

                # Student's Full Name
                eval_card_canvas.create_text(70, 8, text=evaluation["stu_full_name"],
                                             font=("Lexend Deca", 12, "bold"),
                                             fill="#020202", anchor=tk.NW)

                # Comment
                eval_card_canvas.create_text(70, 34, text=evaluation["eval_comment"],
                                             font=("Lexend Deca", 8),
                                             fill="#000000", anchor=tk.NW)

                # Rating
                eval_card_canvas.create_text(556, 8, text=evaluation['eval_rating'],
                                             font=("Lexend Deca", 12),
                                             fill="#020202", anchor=tk.NW)
                eval_card_canvas.create_image(564, 15, image=self.star, anchor=tk.NW)

                # Date & Time
                eval_card_canvas.create_text(490, 50, text=evaluation['eval_date'],
                                             font=("Lexend Deca", 6),
                                             fill="gray", anchor=tk.NW)

                # Delete Button
                delete_btn = tk.Button(eval_card, width=34, height=78, borderwidth=0,
                                       image=self.trash,
                                       command=lambda eval_id=evaluation["eval_id"],
                                                      card=eval_card: self.delete_evaluation(eval_id, card))
                delete_btn.place(x=584, y=0)  # Adjusted x position to fit within card
        else:
            empty_lbl = tk.Label(scrollable_frame, text="No evaluations yet.",
                                 font=("Lexend Deca", 12, "italic"),
                                 bg="#D9D9D9")
            empty_lbl.pack(pady=20)

        # Unbind mouse wheel when leaving the canvas area
        def _leave_canvas(event):
            canvas.unbind_all("<MouseWheel>")

        # Rebind mouse wheel when entering the canvas area
        def _enter_canvas(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        canvas.bind("<Enter>", _enter_canvas)
        canvas.bind("<Leave>", _leave_canvas)

    def get_pfp_path(self, PFP_DIR, stu_id):
        pfp_path = PFP_DIR / f"student_{stu_id}.png"
        default_pfp = PFP_DIR / "student_default.png"
        return pfp_path if pfp_path.exists() else default_pfp

    def make_pfp_circle(self, pfp_path):
        size = (100, 100)  # Keep a high-resolution version
        display_size = (50, 50)  # Displayed size in UI

        pfp = Image.open(pfp_path).convert("RGBA")
        pfp = pfp.resize(size, Image.Resampling.LANCZOS)

        # Create circular mask
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((1, 1, size[0] - 1, size[1] - 1), fill=255)

        # Apply the mask
        circular_pfp = Image.new("RGBA", size, (0, 0, 0, 0))
        circular_pfp.paste(pfp, (0, 0), mask)

        # Resize final image to display size
        circular_pfp = circular_pfp.resize(display_size, Image.Resampling.LANCZOS)

        return ImageTk.PhotoImage(circular_pfp)

    def delete_evaluation(self, eval_id, card_widget):
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this evaluation?")
        if confirm:
            result = self.main.faculty_model.delete_evaluation(eval_id)
            self.create_evaluation_analytics()
            if result:
                card_widget.destroy()
                messagebox.showinfo("Deleted", "Evaluation deleted successfully.")
            else:
                messagebox.showerror("Error", "Failed to delete the evaluation.")

    def render_rating_analytics(self):
        fac_id = self.faculty_landing.faculty_session["fac_id"]
        ratings = self.main.faculty_model.get_faculty_ratings(fac_id)
        if not ratings:
            return  # Optionally show a message

        max_width = 60
        max_count = max(ratings.values()) if ratings else 1
        canvas_height = 140
        canvas_width = 140

        canvas = tk.Canvas(self.analytics_frame, width=canvas_width, height=canvas_height, bg="#FFFFFF", bd=0, highlightthickness=0)
        canvas.pack()

        y_offset = 10
        for rating in range(5, 0, -1):  # 5★ to 1★
            count = ratings[rating]
            bar_width = (count / max_count) * max_width if max_count > 0 else 0

            # Star label
            canvas.create_text(10, y_offset + 7, text=f"{rating}★", anchor="w", font=("Lexend Deca", 9, "bold"), fill="#000000")

            # Gray background bar
            canvas.create_rectangle(40, y_offset, 40 + max_width, y_offset + 10, fill="#E0E0E0", outline="")

            # Yellow fill
            canvas.create_rectangle(40, y_offset, 40 + bar_width, y_offset + 10, fill="#FFD700", outline="")

            # Count label
            canvas.create_text(120, y_offset + 5, text=str(count), anchor="w", font=("Lexend Deca", 9), fill="#000000")

            y_offset += 25
