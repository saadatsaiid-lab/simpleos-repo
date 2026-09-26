# SimpleOS Clock
# Compatible with SimpleOS 7.0 / 7.1
# No external dependencies

import tkinter as tk
from datetime import datetime


class ClockApp:
    NAME = "Clock"
    ICON = "🕐"
    APP_ID = "clock"

    def __init__(self, desktop):
        self.desktop = desktop
        self.window = None
        self.running = False

    def launch(self):
        # جلوگیری از باز شدن چند پنجره
        if self.window is not None:
            try:
                if self.window.winfo_exists():
                    self.window.deiconify()
                    self.window.lift()
                    self.window.focus_force()
                    return self.window
            except Exception:
                pass

        self.window = tk.Toplevel(self.desktop.root)

        self.window.title("🕐 Clock")
        self.window.geometry("500x300")
        self.window.minsize(400, 250)

        self.window.configure(
            bg="#111827"
        )

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

        self._build()

        self.running = True
        self._update_clock()

        return self.window

    def _build(self):
        # Main container
        main = tk.Frame(
            self.window,
            bg="#111827"
        )

        main.pack(
            fill="both",
            expand=True
        )

        # Title
        title = tk.Label(
            main,
            text="SIMPLEOS CLOCK",
            font=("Segoe UI", 14, "bold"),
            bg="#111827",
            fg="#60a5fa"
        )

        title.pack(
            pady=(25, 5)
        )

        # Time
        self.time_label = tk.Label(
            main,
            text="00:00:00",
            font=("Consolas", 48, "bold"),
            bg="#111827",
            fg="#ffffff"
        )

        self.time_label.pack(
            pady=10
        )

        # Date
        self.date_label = tk.Label(
            main,
            text="",
            font=("Segoe UI", 16),
            bg="#111827",
            fg="#d1d5db"
        )

        self.date_label.pack(
            pady=5
        )

        # Status
        self.status_label = tk.Label(
            main,
            text="SimpleOS System Clock",
            font=("Segoe UI", 10),
            bg="#111827",
            fg="#6b7280"
        )

        self.status_label.pack(
            side="bottom",
            pady=15
        )

    def _update_clock(self):
        if not self.running:
            return

        if self.window is None:
            return

        try:
            if not self.window.winfo_exists():
                return
        except Exception:
            return

        now = datetime.now()

        self.time_label.config(
            text=now.strftime("%H:%M:%S")
        )

        self.date_label.config(
            text=now.strftime("%Y-%m-%d")
        )

        self.window.after(
            500,
            self._update_clock
        )

    def close(self):
        self.running = False

        if self.window is not None:
            try:
                self.window.destroy()
            except Exception:
                pass

            self.window = None


# ---------------------------------------------------------
# SimpleOS Package Loader
# ---------------------------------------------------------

APP_CLASS = ClockApp
APP = ClockApp
