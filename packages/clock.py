import tkinter as tk
from datetime import datetime


class ClockApp:
    NAME = "Clock"
    ICON = "🕐"
    APP_ID = "clock"

    def __init__(self, desktop):
        self.desktop = desktop

    def launch(self):

        window = tk.Toplevel(self.desktop)   # ← فقط این خط تغییر کرد
        window.title("🕐 Clock")
        window.geometry("500x280")
        window.resizable(False, False)

        time_label = tk.Label(
            window,
            font=("Consolas", 42, "bold")
        )

        time_label.pack(pady=45)

        date_label = tk.Label(
            window,
            font=("Segoe UI", 16)
        )

        date_label.pack()

        def update():

            if not window.winfo_exists():
                return

            now = datetime.now()

            time_label.config(
                text=now.strftime("%H:%M:%S")
            )

            date_label.config(
                text=now.strftime("%Y-%m-%d")
            )

            window.after(500, update)

        update()

        return window


APP_CLASS = ClockApp
