import os
import shutil
import zipfile
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog, messagebox

# --- Custom Paths ---
BASE_DIR = r"C:\Users\liamo\OneDrive\Desktop\daily_work"
SHARED_STORAGE = r"C:\Users\liamo\OneDrive\Desktop\shared_storage"

# Ensure directories exist
os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs(SHARED_STORAGE, exist_ok=True)

# --- Helper Functions ---
def create_today_folder():
    today = datetime.now().strftime('%Y-%m-%d')
    today_folder = os.path.join(BASE_DIR, today)
    if not os.path.exists(today_folder):
        os.makedirs(today_folder)
        messagebox.showinfo("Success", f"Today's folder created: {today_folder}")
    else:
        messagebox.showwarning("Warning", "Today's folder already exists.")
    return today_folder

def zip_and_upload():
    today = datetime.now().strftime('%Y-%m-%d')
    today_folder = os.path.join(BASE_DIR, today)
    if not os.path.exists(today_folder):
        messagebox.showerror("Error", "Today's folder does not exist!")
        return
    
    zip_path = os.path.join(SHARED_STORAGE, f"{today}.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        files = []
        for root, dirs, files_in_folder in os.walk(today_folder):
            for file in files_in_folder:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, today_folder))
                files.append(file_path)
    
    # Simulate upload (this part is just a placeholder)
    messagebox.showinfo("Success", f"Folder zipped and uploaded to: {zip_path}")

def browse_folder():
    folder_path = filedialog.askdirectory(initialdir=BASE_DIR, title="Select Folder")
    messagebox.showinfo("Folder Selected", f"Selected: {folder_path}")

def delete_file():
    file_path = filedialog.askopenfilename(initialdir=BASE_DIR, title="Select File")
    if file_path:
        os.remove(file_path)
        messagebox.showinfo("Success", f"Deleted file: {file_path}")

def add_file():
    file_path = filedialog.askopenfilename(title="Select File to Add")
    if file_path:
        today_folder = create_today_folder()
        shutil.copy(file_path, today_folder)
        messagebox.showinfo("Success", f"Copied file to {today_folder}")

# --- Tkinter UI ---
def create_ui():
    global app  # Make sure 'app' is accessible in other functions
    
    app = ctk.CTk()
    app.geometry("500x400")
    app.title("Daily File Logger - Test UI")

    # Create a container frame for sections
    frame = ctk.CTkFrame(app)
    frame.pack(padx=20, pady=20, expand=True, fill="both")

    # --- Folder Management Section ---
    folder_section = ctk.CTkLabel(frame, text="Folder Management", font=("Arial", 16))
    folder_section.grid(row=0, column=0, columnspan=2, pady=10)
    
    ctk.CTkButton(frame, text="Create Today's Folder", command=create_today_folder).grid(row=1, column=0, pady=5)
    ctk.CTkButton(frame, text="Browse Folders", command=browse_folder).grid(row=1, column=1, pady=5)

    # --- File Management Section ---
    file_section = ctk.CTkLabel(frame, text="File Management", font=("Arial", 16))
    file_section.grid(row=2, column=0, columnspan=2, pady=10)
    
    ctk.CTkButton(frame, text="Add File to Today's Folder", command=add_file).grid(row=3, column=0, pady=5)
    ctk.CTkButton(frame, text="Delete File", command=delete_file).grid(row=3, column=1, pady=5)

    # --- Upload Section ---
    upload_section = ctk.CTkLabel(frame, text="Zip and Upload", font=("Arial", 16))
    upload_section.grid(row=4, column=0, columnspan=2, pady=10)
    
    ctk.CTkButton(frame, text="Zip and Upload", command=zip_and_upload).grid(row=5, column=0, columnspan=2, pady=20)
    
    ctk.CTkButton(frame, text="Exit", command=app.quit).grid(row=6, column=0, columnspan=2, pady=20)

    app.mainloop()

if __name__ == "__main__":
    create_ui()
