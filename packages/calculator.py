# SimpleOS Calculator
# Compatible with SimpleOS 7.0 / 7.1
# No external dependencies

import tkinter as tk


class CalculatorApp:
    NAME = "Calculator"
    ICON = "🧮"
    APP_ID = "calculator"

    def __init__(self, desktop):
        self.desktop = desktop
        self.window = None
        self.expression = ""

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
        self.window.title("🧮 Calculator")
        self.window.geometry("360x500")
        self.window.minsize(320, 420)

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

        self._build()

        return self.window

    def _build(self):
        # ---------- Main ----------
        main = tk.Frame(
            self.window,
            bg="#151922"
        )
        main.pack(
            fill="both",
            expand=True
        )

        # ---------- Display ----------
        display_frame = tk.Frame(
            main,
            bg="#151922"
        )
        display_frame.pack(
            fill="x",
            padx=15,
            pady=(15, 10)
        )

        self.display = tk.Entry(
            display_frame,
            font=("Segoe UI", 24),
            bg="#0d1117",
            fg="#ffffff",
            insertbackground="#ffffff",
            justify="right",
            relief="flat",
            bd=0
        )

        self.display.pack(
            fill="x",
            ipady=15
        )

        # ---------- Buttons ----------
        buttons = [
            ["C", "⌫", "(", ")"],
            ["7", "8", "9", "÷"],
            ["4", "5", "6", "×"],
            ["1", "2", "3", "−"],
            ["0", ".", "=", "+"]
        ]

        button_frame = tk.Frame(
            main,
            bg="#151922"
        )
        button_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        for row in range(len(buttons)):
            button_frame.rowconfigure(
                row,
                weight=1
            )

        for column in range(4):
            button_frame.columnconfigure(
                column,
                weight=1
            )

        for row, button_row in enumerate(buttons):
            for column, text in enumerate(button_row):

                button = tk.Button(
                    button_frame,
                    text=text,
                    font=("Segoe UI", 16),
                    relief="flat",
                    bd=0,
                    bg=self._button_color(text),
                    fg="#ffffff",
                    activebackground="#3a4354",
                    activeforeground="#ffffff",
                    command=lambda value=text:
                        self._button_click(value)
                )

                button.grid(
                    row=row,
                    column=column,
                    sticky="nsew",
                    padx=4,
                    pady=4
                )

        # ---------- Keyboard ----------
        self.window.bind(
            "<Key>",
            self._keyboard
        )

        self.display.focus_set()

    def _button_color(self, text):
        if text == "=":
            return "#2563eb"

        if text in ("+", "−", "×", "÷"):
            return "#374151"

        if text in ("C", "⌫"):
            return "#7f1d1d"

        return "#252b36"

    def _button_click(self, value):
        if value == "C":
            self.clear()

        elif value == "⌫":
            self.backspace()

        elif value == "=":
            self.calculate()

        else:
            self.insert(value)

    def insert(self, value):
        self.display.insert(
            tk.END,
            value
        )

    def clear(self):
        self.display.delete(
            0,
            tk.END
        )

    def backspace(self):
        current = self.display.get()

        if current:
            self.display.delete(
                len(current) - 1,
                tk.END
            )

    def calculate(self):
        expression = self.display.get().strip()

        if not expression:
            return

        try:
            # تبدیل نمادهای نمایشی به Python
            expression = expression.replace(
                "×",
                "*"
            )

            expression = expression.replace(
                "÷",
                "/"
            )

            expression = expression.replace(
                "−",
                "-"
            )

            # فقط اجازه کاراکترهای ریاضی ساده
            allowed = set(
                "0123456789+-*/().% "
            )

            if any(
                character not in allowed
                for character in expression
            ):
                raise ValueError(
                    "Invalid characters"
                )

            # محدود کردن طول عبارت
            if len(expression) > 200:
                raise ValueError(
                    "Expression too long"
                )

            # eval با builtins غیرفعال
            result = eval(
                expression,
                {
                    "__builtins__": {}
                },
                {}
            )

            # جلوگیری از نمایش بعضی نتایج نامناسب
            if isinstance(
                result,
                complex
            ):
                raise ValueError(
                    "Complex result"
                )

            self.display.delete(
                0,
                tk.END
            )

            self.display.insert(
                0,
                self._format_result(result)
            )

        except ZeroDivisionError:
            self._show_error(
                "Division by zero"
            )

        except Exception:
            self._show_error(
                "Invalid expression"
            )

    def _format_result(self, result):
        if isinstance(
            result,
            float
        ):
            if result.is_integer():
                return str(
                    int(result)
                )

            return f"{result:.12g}"

        return str(result)

    def _show_error(self, message):
        self.display.delete(
            0,
            tk.END
        )

        self.display.insert(
            0,
            message
        )

    def _keyboard(self, event):
        key = event.keysym

        if event.char in "0123456789.+-*/()%":
            self.insert(event.char)
            return "break"

        if event.char == "=":
            self.calculate()
            return "break"

        if key in (
            "Return",
            "KP_Enter"
        ):
            self.calculate()
            return "break"

        if key == "BackSpace":
            self.backspace()
            return "break"

        if key == "Escape":
            self.clear()
            return "break"

    def close(self):
        if self.window is not None:
            try:
                self.window.destroy()
            except Exception:
                pass

            self.window = None


# ---------------------------------------------------------
# SimpleOS Package Loader
# ---------------------------------------------------------

APP_CLASS = CalculatorApp
APP = CalculatorApp
