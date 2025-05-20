# Daily File Logger
<img src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHh2a3FxaXptYzdiamd4bnQ2bjI1bW04c2IybGk1ZGZkbnNtN3BsdCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/rqgeA1ckKGdlevO5pg/giphy.gif" alt="Glitch Banner" style="width: 100%; max-height: 400px; object-fit: cover; display: block; margin-bottom: 24px;" />

## Overview
**Daily File Logger** is a Python-based automation tool designed to simplify your daily file management workflow. It creates daily folders with the current date, copies files from the previous day's folder, and zips the folder at the end of the day. Finally, it uploads the zipped archive to a shared drive such as Google Drive.

## Features
- Automatic creation of daily folders.
- Copies files from the previous day's folder to ensure the new folder is up-to-date.
- Compresses the folder into a `.zip` file at the end of the day.
- Option to upload the `.zip` file to Google Drive or a network-shared directory.

## Requirements
- Python 3.7+
- Google Drive API credentials (if using Google Drive for upload)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/lincalibur/daily-file-logger.git
   cd daily-file-logger
   ```

2. Install required Python modules:
   ```bash
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

3. Set up Google Drive API (if needed):
   - Go to [Google Cloud Console](https://console.cloud.google.com/), create a project, and enable the "Google Drive API."
   - Create credentials and download the `credentials.json` file.
   - Save the file in the project directory.

## Usage
1. Edit the `main()` function in `daily_file_logger.py` to set your base directory and Google Drive folder ID:
   ```python
   BASE_DIR = "./daily_logs"  # Path where daily folders will be created
   SHARED_DRIVE_FOLDER_ID = "your_google_drive_folder_id"  # Google Drive folder ID
   ```

2. Run the script:
   ```bash
   python daily_file_logger.py
   ```

3. To automate the script daily, use a scheduler like `cron` (Linux/macOS) or Task Scheduler (Windows).

## Roadmap
- Add support for additional cloud storage providers (e.g., Dropbox, OneDrive).
- Implement detailed logging of daily operations.
- Add a GUI for user-friendly configuration.

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests to enhance the project.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
