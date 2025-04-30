
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import json
from datetime import datetime
import os

class HistoryManager:
    def __init__(self, parent):
        self.parent = parent
        self.history_window = None
        self.scrollable_frame = None
        self.HISTORY_FILE = "search_history.json"

    def save_search(self, city, temperature, humidity):
        try:
            if os.path.exists(self.HISTORY_FILE):
                with open(self.HISTORY_FILE, "r") as file:
                    searches = json.load(file) or []
            else:
                searches = []
            
            searches.append({
                "city": city,
                "temperature": temperature,
                "humidity": humidity,
                "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            searches = searches[-20:]
            
            with open(self.HISTORY_FILE, "w") as file:
                json.dump(searches, file, indent=4)
                
            if self.history_window and self.history_window.winfo_exists():
                self.update_history_display()

        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Failed to save search history: {str(e)}",
                icon="cancel"
            )

    def show_history(self):
        if self.history_window and self.history_window.winfo_exists():
            self.update_history_display()
            self.history_window.lift()
            return

        self.history_window = ctk.CTkToplevel(self.parent)
        self.history_window.geometry("300x600")
        self.history_window.title("SEARCH HISTORY")

        main_frame = ctk.CTkFrame(self.history_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.scrollable_frame = ctk.CTkScrollableFrame(main_frame, width=280, height=500)
        self.scrollable_frame.pack(fill="both", expand=True, padx=5, pady=(5, 10))

        clear_btn = ctk.CTkButton(main_frame, text="Clear History", command=self.confirm_clear)
        clear_btn.pack(fill="x", pady=(5, 10))

        self.update_history_display()
        self.history_window.lift()

    def update_history_display(self):
        if not self.scrollable_frame:
            return

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            with open(self.HISTORY_FILE, "r") as file:
                searches = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            searches = []

        for entry in reversed(searches):
            lbl = ctk.CTkLabel(
                self.scrollable_frame,
                text=f"{entry['city']}\nTemp: {entry['temperature']}°C\n"
                     f"Humidity: {entry['humidity']}%\n{entry['datetime']}",
                font=("Arial", 14),
                justify="left"
            )
            lbl.pack(pady=5, padx=10, anchor="w", fill="x")

    def confirm_clear(self):
        msg = CTkMessagebox(
            title="Confirm Clear",
            message="Clear all history?",
            icon="question",
            option_1="Cancel",
            option_2="Clear"
        )
        if msg.get() == "Clear":
            self.clear_history()

    def clear_history(self):
        try:
            with open(self.HISTORY_FILE, "w") as file:
                json.dump([], file)
            self.update_history_display()
        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Failed to clear history: {str(e)}",
                icon="cancel"
            )