import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json
import subprocess

class SetupWizard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Daily File Logger Setup Wizard")
        self.geometry("500x200")
        self.resizable(False, False)

        self.local_storage_path = ""
        self.shared_storage_path = ""
        self.install_path = ""

        self.current_step = 0
        self.steps = [self.create_intro_page, self.create_local_storage_page, self.create_shared_storage_page,
                      self.create_install_path_page, self.create_finish_page]
        
        self.create_intro_page()

    def create_intro_page(self):
        """Introduction page"""
        self.clear_page()
        
        tk.Label(self, text="Welcome to the Daily File Logger Setup Wizard", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(self, text="Click 'Next' to begin the setup process").pack(pady=10)
        
        self.next_button = tk.Button(self, text="Next", command=self.next_step)
        self.next_button.pack(pady=20)

    def create_local_storage_page(self):
        """Local Storage Path page"""
        self.clear_page()

        tk.Label(self, text="Select the Local Storage folder where your files will be stored.", font=("Arial", 10)).pack(pady=10)
        self.local_storage_button = tk.Button(self, text="Browse", command=self.select_local_storage)
        self.local_storage_button.pack()

        self.local_storage_label = tk.Label(self, text="No path selected", font=("Arial", 9))
        self.local_storage_label.pack(pady=5)

        self.back_button = tk.Button(self, text="Back", command=self.previous_step)
        self.back_button.pack(side=tk.LEFT, padx=20, pady=20)
        
        self.next_button = tk.Button(self, text="Next", state=tk.DISABLED, command=self.next_step)
        self.next_button.pack(side=tk.RIGHT, padx=20, pady=20)

    def create_shared_storage_page(self):
        """Shared Storage Path page"""
        self.clear_page()

        tk.Label(self, text="Select the Shared Storage folder where shared files will be kept.", font=("Arial", 10)).pack(pady=10)
        self.shared_storage_button = tk.Button(self, text="Browse", command=self.select_shared_storage)
        self.shared_storage_button.pack()

        self.shared_storage_label = tk.Label(self, text="No path selected", font=("Arial", 9))
        self.shared_storage_label.pack(pady=5)

        self.back_button = tk.Button(self, text="Back", command=self.previous_step)
        self.back_button.pack(side=tk.LEFT, padx=20, pady=20)
        
        self.next_button = tk.Button(self, text="Next", state=tk.DISABLED, command=self.next_step)
        self.next_button.pack(side=tk.RIGHT, padx=20, pady=20)

    def create_install_path_page(self):
        """Installation Path page"""
        self.clear_page()

        tk.Label(self, text="Select the installation folder where the app will be installed.", font=("Arial", 10)).pack(pady=10)
        self.install_button = tk.Button(self, text="Browse", command=self.select_install_path)
        self.install_button.pack()

        self.install_label = tk.Label(self, text="No path selected", font=("Arial", 9))
        self.install_label.pack(pady=5)

        self.back_button = tk.Button(self, text="Back", command=self.previous_step)
        self.back_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.next_button = tk.Button(self, text="Next", state=tk.DISABLED, command=self.next_step)
        self.next_button.pack(side=tk.RIGHT, padx=20, pady=20)

    def create_finish_page(self):
        """Finish page"""
        self.clear_page()

        tk.Label(self, text="Setup Complete!", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(self, text="Click 'Finish' to save and build the application").pack(pady=10)

        self.back_button = tk.Button(self, text="Back", command=self.previous_step)
        self.back_button.pack(side=tk.LEFT, padx=20, pady=20)
        
        self.finish_button = tk.Button(self, text="Finish", command=self.finish_setup)
        self.finish_button.pack(side=tk.RIGHT, padx=20, pady=20)

    def clear_page(self):
        """Clear the current page's widgets"""
        for widget in self.winfo_children():
            widget.destroy()

    def next_step(self):
        """Navigate to the next step"""
        self.current_step += 1
        self.steps[self.current_step]()

    def previous_step(self):
        """Navigate to the previous step"""
        self.current_step -= 1
        self.steps[self.current_step]()

    def select_local_storage(self):
        """Select the local storage path"""
        self.local_storage_path = filedialog.askdirectory(title="Select Local Storage Folder")
        if self.local_storage_path:
            self.local_storage_label.config(text=self.local_storage_path)
            self.next_button.config(state=tk.NORMAL)

    def select_shared_storage(self):
        """Select the shared storage path"""
        self.shared_storage_path = filedialog.askdirectory(title="Select Shared Storage Folder")
        if self.shared_storage_path:
            self.shared_storage_label.config(text=self.shared_storage_path)  # Update the label with selected path
            self.next_button.config(state=tk.NORMAL)

    def select_install_path(self):
        """Select the installation path"""
        self.install_path = filedialog.askdirectory(title="Select Installation Folder")
        if self.install_path:
            self.install_label.config(text=self.install_path)  # Update the label with selected path
            self.next_button.config(state=tk.NORMAL)

    def finish_setup(self):
        """Finish setup and save paths"""
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
        """Build the .exe using PyInstaller"""
        template_path = os.path.join(os.path.dirname(__file__), "template_script.py")  # Correct path
        with open(template_path, "r") as template_file:
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
            "--noconsole",  # Hide the terminal window
            "--icon=assets/1-92dc4e47.ico",  # Use actual icon path here
            "--distpath", os.path.join(config["install_path"], "dist"),  # Output folder for the .exe
            "--workpath", os.path.join(config["install_path"], "build"),  # Temporary files folder for PyInstaller
            output_script
        ])

        messagebox.showinfo("Build Complete", "The application has been built and installed!")

if __name__ == "__main__":
    wizard = SetupWizard()
    wizard.mainloop()
