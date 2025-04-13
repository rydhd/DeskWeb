import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from collections import defaultdict
import customtkinter as ctk
from customtkinter import *



class StudentScheduleTab(tk.Frame):
    def __init__(self, parent, main, student_landing):
        super().__init__(parent)
        self.main = main
        self.student_landing = student_landing
        self.student_session = student_landing.student_session
        self.config(bd=0, highlightthickness=0)

        self.grid(row=0, column=0, sticky="nsew",ipady=30,ipadx=30)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Calendar Widget
        self.calendar = Calendar(self, selectmode='day', year=2025, month=4, day=8,
            headersforeground="#8D0404",background="#FFFFFF",foreground="black",font=("Lexend Deca", 9, "normal"))
        self.calendar.place(x=600, y=57,width=248,height=200)

        self.display_schedule(self.student_session["stu_id"])

    def format_time(self, time_value):
        if isinstance(time_value, str):
            return time_value
        elif isinstance(time_value, int):
            hours = time_value // 100
            minutes = time_value % 100
            return f"{hours:02}:{minutes:02}"
        elif hasattr(time_value, 'seconds'):
            hours, remainder = divmod(time_value.seconds, 3600)
            minutes = remainder // 60
            return f"{hours:02}:{minutes:02}"
        else:
            return str(time_value)

    def display_schedule(self, stu_id):
        for widget in self.winfo_children():
            if widget != self.calendar:  # Keep the calendar
                widget.destroy()

        self.lbl = ctk.CTkLabel(self, text="SCHEDULE", font=("Lexend Deca", 30, "bold"), text_color="#8D0404")
        self.lbl.grid(row=0, column=0, sticky="nsew", padx=10)

        student_sched = self.main.student_model.get_sched(stu_id)

        if not student_sched:
            no_courses_lbl = ctk.CTkLabel(
                self,
                text="You currently don't have any enrolled courses.",
                font=("Lexend Deca", 16, "bold"),
                text_color="#8B0000"
            )
            no_courses_lbl.grid(row=1, column=0, columnspan=3, pady=20, padx=10, sticky="nsew")
            return

        day_order = {
            "MONDAY": 1,
            "TUESDAY": 2,
            "WEDNESDAY": 3,
            "THURSDAY": 4,
            "FRIDAY": 5,
            "SATURDAY": 6,
            "SUNDAY": 7,
        }

        schedule_by_day = defaultdict(list)
        for sched in student_sched:
            schedule_by_day[sched["day_of_week"].upper()].append(sched)

        sorted_days = sorted(schedule_by_day.keys(), key=lambda day: day_order[day])

        row = 5
        for day in sorted_days:
            day_courses = schedule_by_day[day]

            tk.Label(self, text=day.upper(), fg='white', bg="#8B0000", font=("Lexend Deca", 14, "bold")) \
                .grid(row=row, column=0, sticky="nsew", pady=8, padx=10)

            for sched in day_courses:
                tk.Label(self, text=sched["course_name"][:20], bg="#E5E5E5", font=("Lexend Deca", 14), anchor="w") \
                    .grid(row=row, column=1, sticky="nsew", padx=10, pady=8)

                time_start = self.format_time(sched["time_start"])
                time_end = self.format_time(sched["time_end"])
                tk.Label(self, text=f"{time_start} - {time_end}", bg="#E5E5E5", font=("Lexend Deca", 14), anchor="e") \
                    .grid(row=row, column=2, sticky="nsew", pady=8)

                row += 2

