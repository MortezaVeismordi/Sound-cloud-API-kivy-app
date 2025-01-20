# SoundCloud Downloader App

## Overview
The **SoundCloud Downloader App** is a Python application built with Kivy that allows users to:
- Download songs from SoundCloud using their API Key.
- Enter song URLs to initiate downloads.
- Choose a custom download location for saving songs.
- Track download progress through a progress bar.

This application ensures a user-friendly experience and handles errors gracefully, such as invalid API keys or missing inputs.

---

## Features
- **API Key Management**: Validate and save SoundCloud API Keys.
- **Song Download**: Download songs using SoundCloud track URLs.
- **Custom Download Location**: Choose a folder to save downloaded songs or use the default `downloads` folder.
- **Progress Tracking**: Visualize the download progress with a progress bar.
- **Error Handling**: Informative messages for invalid inputs, API errors, and download issues.

---

## Requirements
To run this app, ensure the following are installed on your system:
- Python 3.7 or higher
- Kivy 2.1.0 or higher
- Requests library

Install required libraries using:
```bash
pip install kivy requests
```

---

## Usage

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/soundcloud-downloader.git
   cd soundcloud-downloader
   ```

2. **Run the App**:
   Execute the following command to launch the application:
   ```bash
   python main.py
   ```

3. **Steps to Use**:
   - Enter your SoundCloud API Key in the provided field and click **Submit API Key**.
   - Paste the SoundCloud song URL into the URL field.
   - (Optional) Click **Choose Download Location** to select a custom folder. If skipped, songs will be saved in the default `downloads` folder.
   - Click **Download** to start downloading the song.
   - Monitor the download progress via the progress bar.

---

## Notes
- Ensure you have a valid SoundCloud API Key. You can register for an API Key at [SoundCloud Developer Portal](https://soundcloud.com/you/apps).
- Only public tracks are downloadable through the SoundCloud API.

---

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes and push them:
   ```bash
   git commit -m "Add your feature description"
   git push origin feature/your-feature
   ```
4. Open a Pull Request on GitHub.

---
