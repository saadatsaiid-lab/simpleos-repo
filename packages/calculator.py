import tkinter as tk


class CalculatorApp:
    NAME = "Calculator"
    ICON = "🧮"
    APP_ID = "calculator"

    def __init__(self, desktop):
        self.desktop = desktop

    def launch(self):
        window = tk.Toplevel(self.desktop.root)
        window.title("🧮 Calculator")
        window.geometry("360x500")
        window.resizable(False, False)

        display = tk.Entry(
            window,
            font=("Segoe UI", 24),
            justify="right"
        )
        display.pack(
            fill="x",
            padx=15,
            pady=15,
            ipady=10
        )

        def calculate():
            expression = display.get()

            expression = (
                expression
                .replace("×", "*")
                .replace("÷", "/")
                .replace("−", "-")
            )

            allowed = "0123456789+-*/().% "

            if not expression:
                return

            if len(expression) > 200:
                display.delete(0, "end")
                display.insert(0, "Too long")
                return

            if any(c not in allowed for c in expression):
                display.delete(0, "end")
                display.insert(0, "Error")
                return

            try:
                result = eval(
                    expression,
                    {"__builtins__": {}},
                    {}
                )

                display.delete(0, "end")
                display.insert(0, str(result))

            except Exception:
                display.delete(0, "end")
                display.insert(0, "Error")

        buttons = [
            ["C", "⌫", "(", ")"],
            ["7", "8", "9", "÷"],
            ["4", "5", "6", "×"],
            ["1", "2", "3", "−"],
            ["0", ".", "=", "+"]
        ]

        for row, values in enumerate(buttons):

            for col, value in enumerate(values):

                def command(v=value):

                    if v == "C":
                        display.delete(0, "end")

                    elif v == "⌫":
                        current = display.get()
                        display.delete(0, "end")
                        display.insert(0, current[:-1])

                    elif v == "=":
                        calculate()

                    else:
                        display.insert("end", v)

                button = tk.Button(
                    window,
                    text=value,
                    command=command,
                    font=("Segoe UI", 14)
                )

                button.place(
                    x=15 + col * 82,
                    y=100 + row * 65,
                    width=72,
                    height=55
                )

        return window


APP_CLASS = CalculatorApp
