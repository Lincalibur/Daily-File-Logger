import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json
import subprocess

class SetupWizard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Daily File Logger Setup Wizard")
        self.geometry("500x400")

        self.local_storage_path = ""
        self.shared_storage_path = ""
        self.install_path = ""

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Welcome to the Daily File Logger Setup Wizard", font=("Arial", 14)).pack(pady=10)

        # Local Storage Path
        tk.Label(self, text="Select Local Storage Path:").pack(pady=5)
        self.local_storage_button = tk.Button(self, text="Browse", command=self.select_local_storage)
        self.local_storage_button.pack()

        # Shared Storage Path
        tk.Label(self, text="Select Shared Storage Path:").pack(pady=5)
        self.shared_storage_button = tk.Button(self, text="Browse", command=self.select_shared_storage)
        self.shared_storage_button.pack()

        # Install Path
        tk.Label(self, text="Select App Installation Path:").pack(pady=5)
        self.install_button = tk.Button(self, text="Browse", command=self.select_install_path)
        self.install_button.pack()

        # Finish Setup
        self.finish_button = tk.Button(self, text="Finish Setup", command=self.finish_setup)
        self.finish_button.pack(pady=20)

    def select_local_storage(self):
        self.local_storage_path = filedialog.askdirectory(title="Select Local Storage Folder")
        if self.local_storage_path:
            messagebox.showinfo("Path Selected", f"Local Storage: {self.local_storage_path}")

    def select_shared_storage(self):
        self.shared_storage_path = filedialog.askdirectory(title="Select Shared Storage Folder")
        if self.shared_storage_path:
            messagebox.showinfo("Path Selected", f"Shared Storage: {self.shared_storage_path}")

    def select_install_path(self):
        self.install_path = filedialog.askdirectory(title="Select Installation Folder")
        if self.install_path:
            messagebox.showinfo("Path Selected", f"Install Path: {self.install_path}")

    def finish_setup(self):
        if not self.local_storage_path or not self.shared_storage_path or not self.install_path:
            messagebox.showerror("Error", "Please select all paths!")
            return

        # Save configuration
        config = {
            "local_storage": self.local_storage_path,
            "shared_storage": self.shared_storage_path,
            "install_path": self.install_path,
        }

        config_path = os.path.join(self.install_path, "config.json")
        with open(config_path, "w") as f:
            json.dump(config, f)

        messagebox.showinfo("Setup Complete", "Paths saved! Building the application...")
        self.build_application(config)

    def build_application(self, config):
        # Replace paths in the template script
        with open("template_script.py", "r") as template_file:
            script_content = template_file.read()

        script_content = script_content.replace("{LOCAL_STORAGE}", config["local_storage"])
        script_content = script_content.replace("{SHARED_STORAGE}", config["shared_storage"])

        output_script = os.path.join(config["install_path"], "daily_file_logger.py")
        with open(output_script, "w") as output_file:
            output_file.write(script_content)

        # Build the .exe using PyInstaller
        subprocess.run([
            "pyinstaller",
            "--onefile",
            "--icon=your_icon.ico",
            output_script
        ])

        messagebox.showinfo("Build Complete", "The application has been built and installed!")

if __name__ == "__main__":
    wizard = SetupWizard()
    wizard.mainloop()
