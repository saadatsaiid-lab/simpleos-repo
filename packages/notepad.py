import tkinter as tk
from tkinter import filedialog, messagebox
import os


class NotepadApp:
    NAME = "Notepad Pro"
    ICON = "📝"
    APP_ID = "notepad"

    def __init__(self, desktop):
        self.desktop = desktop
        self.window = None
        self.current_file = None
        self.modified = False
        self.font_size = 12
        self.is_dark = True

    def launch(self):
        if self.window and self.window.winfo_exists():
            self.window.deiconify()
            self.window.lift()
            self.window.focus_force()
            return self.window

        self.window = tk.Toplevel(self.desktop)
        self.window.title("📝 Notepad Pro - Untitled")
        self.window.geometry("800x600")
        self.window.minsize(500, 400)
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.build_menu()
        self.build_toolbar()
        self.build_editor()
        self.build_statusbar()
        self.apply_theme()
        self.bind_shortcuts()

        return self.window

    # ---------------- MENU ----------------

    def build_menu(self):
        menubar = tk.Menu(self.window)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New    Ctrl+N", command=self.new_file)
        file_menu.add_command(label="Open   Ctrl+O", command=self.open_file)
        file_menu.add_command(label="Save   Ctrl+S", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_close)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo Ctrl+Z", command=self.undo)
        edit_menu.add_command(label="Redo Ctrl+Y", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self.text.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.text.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.text.event_generate("<<Paste>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
        view_menu.add_command(label="Zoom In", command=lambda: self.zoom(1))
        view_menu.add_command(label="Zoom Out", command=lambda: self.zoom(-1))
        menubar.add_cascade(label="View", menu=view_menu)

        self.window.config(menu=menubar)

    # ---------------- TOOLBAR ----------------

    def build_toolbar(self):
        self.toolbar = tk.Frame(self.window, height=40)
        self.toolbar.pack(fill="x")

        buttons = [
            ("📄", self.new_file),
            ("📂", self.open_file),
            ("💾", self.save_file),
            ("↩", self.undo),
            ("↪", self.redo),
            ("🌓", self.toggle_theme),
        ]

        for icon, cmd in buttons:
            tk.Button(
                self.toolbar,
                text=icon,
                command=cmd,
                relief="flat",
                font=("Segoe UI Emoji", 12),
                width=3,
                cursor="hand2"
            ).pack(side="left", padx=2, pady=4)

    # ---------------- EDITOR ----------------

    def build_editor(self):
        container = tk.Frame(self.window)
        container.pack(fill="both", expand=True, padx=8, pady=(0, 4))

        self.scrollbar = tk.Scrollbar(container, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.text = tk.Text(
            container,
            wrap="word",
            undo=True,
            font=("Consolas", self.font_size),
            relief="flat",
            padx=10,
            pady=8,
            yscrollcommand=self.scrollbar.set
        )
        self.text.pack(fill="both", expand=True)
        self.scrollbar.config(command=self.text.yview)

        self.text.bind("<KeyRelease>", self.update_status)
        self.text.bind("<ButtonRelease>", self.update_status)
        self.text.bind("<<Modified>>", self.on_modified)
        self.text.edit_modified(False)

    # ---------------- STATUS BAR ----------------

    def build_statusbar(self):
        self.statusbar = tk.Frame(self.window, height=24)
        self.statusbar.pack(fill="x", side="bottom")

        self.status_label = tk.Label(
            self.statusbar,
            text="Ln 1, Col 1  |  Words: 0",
            font=("Segoe UI", 9),
            anchor="w"
        )
        self.status_label.pack(side="left", padx=10)

        self.file_label = tk.Label(
            self.statusbar,
            text="Untitled",
            font=("Segoe UI", 9),
            anchor="e"
        )
        self.file_label.pack(side="right", padx=10)

    # ---------------- THEME ----------------

    def apply_theme(self):
        if self.is_dark:
            bg, text_bg, text_fg, toolbar, status = "#111827", "#020617", "#e2e8f0", "#1e293b", "#0f172a"
        else:
            bg, text_bg, text_fg, toolbar, status = "#f1f5f9", "#ffffff", "#0f172a", "#e2e8f0", "#cbd5e1"

        self.window.configure(bg=bg)
        self.toolbar.configure(bg=toolbar)
        self.statusbar.configure(bg=status)
        self.status_label.configure(bg=status, fg=text_fg)
        self.file_label.configure(bg=status, fg=text_fg)

        for child in self.toolbar.winfo_children():
            if isinstance(child, tk.Button):
                child.configure(
                    bg=toolbar,
                    fg=text_fg,
                    activebackground=bg,
                    activeforeground=text_fg
                )

        self.text.configure(
            bg=text_bg,
            fg=text_fg,
            insertbackground=text_fg
        )

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.apply_theme()

    # ---------------- FILE OPS ----------------

    def new_file(self):
        if not self.confirm_save():
            return
        self.text.delete("1.0", "end")
        self.current_file = None
        self.modified = False
        self.update_title()

    def open_file(self):
        if not self.confirm_save():
            return

        path = filedialog.askopenfilename(
            parent=self.window,
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not path:
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.text.delete("1.0", "end")
            self.text.insert("1.0", content)
            self.current_file = path
            self.modified = False
            self.update_title()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.window)

    def save_file(self):
        if not self.current_file:
            return self.save_as_file()
        try:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.text.get("1.0", "end-1c"))
            self.modified = False
            self.update_title()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.window)

    def save_as_file(self):
        path = filedialog.asksaveasfilename(
            parent=self.window,
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.text.get("1.0", "end-1c"))
            self.current_file = path
            self.modified = False
            self.update_title()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.window)

    def confirm_save(self):
        if not self.modified:
            return True
        answer = messagebox.askyesnocancel(
            "Unsaved Changes",
            "You have unsaved changes. Save them?",
            parent=self.window
        )
        if answer is None:
            return False
        if answer:
            self.save_file()
            return not self.modified
        return True

    # ---------------- EDIT OPS ----------------

    def undo(self):
        try:
            self.text.edit_undo()
        except tk.TclError:
            pass

    def redo(self):
        try:
            self.text.edit_redo()
        except tk.TclError:
            pass

    def select_all(self):
        self.text.tag_add("sel", "1.0", "end")
        return "break"

    def zoom(self, delta):
        self.font_size = max(8, min(40, self.font_size + delta))
        self.text.configure(font=("Consolas", self.font_size))

    # ---------------- SHORTCUTS ----------------

    def bind_shortcuts(self):
        self.window.bind("<Control-n>", lambda e: self.new_file())
        self.window.bind("<Control-o>", lambda e: self.open_file())
        self.window.bind("<Control-s>", lambda e: self.save_file())
        self.window.bind("<Control-z>", lambda e: self.undo())
        self.window.bind("<Control-y>", lambda e: self.redo())
        self.window.bind("<Control-a>", lambda e: self.select_all())

    # ---------------- STATUS ----------------

    def on_modified(self, event=None):
        if self.text.edit_modified():
            self.modified = True
            self.text.edit_modified(False)
            self.update_title()

    def update_status(self, event=None):
        try:
            cursor = self.text.index("insert")
            line, col = cursor.split(".")
            content = self.text.get("1.0", "end-1c")
            words = len(content.split())
            self.status_label.config(
                text=f"Ln {line}, Col {int(col) + 1}  |  Words: {words}"
            )
        except Exception:
            pass

    def update_title(self):
        name = os.path.basename(self.current_file) if self.current_file else "Untitled"
        star = " •" if self.modified else ""
        self.window.title(f"📝 Notepad Pro - {name}{star}")
        self.file_label.config(text=name)

    # ---------------- CLOSE ----------------

    def on_close(self):
        if not self.confirm_save():
            return
        try:
            self.window.destroy()
        except Exception:
            pass
        self.window = None


APP_CLASS = NotepadApp
