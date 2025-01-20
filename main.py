import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.progressbar import ProgressBar
from kivy.properties import BooleanProperty
import requests
import os
import threading

kivy.require('2.1.0')

class MainPage(BoxLayout):
    api_key_valid = BooleanProperty(False) 

    def __init__(self, app, **kwargs):
        super().__init__(orientation='vertical', padding=10, **kwargs)
        self.app = app

        self.api_input = TextInput(hint_text="Enter SoundCloud API Key", multiline=False, size_hint=(1, 0.1))
        self.add_widget(self.api_input)

        self.api_button = Button(text="Submit API Key", size_hint=(1, 0.1))
        self.api_button.bind(on_press=self.submit_api_key)
        self.add_widget(self.api_button)

        self.url_input = TextInput(hint_text="Enter song URL", multiline=False, size_hint=(1, 0.1))
        self.add_widget(self.url_input)

        self.choose_button = Button(text="Choose Download Location", size_hint=(1, 0.1))
        self.choose_button.bind(on_press=self.choose_download_location)
        self.add_widget(self.choose_button)

        self.download_location_label = Label(
            text=f"Download location: {self.app.download_location}", size_hint=(1, 0.1)
        )
        self.add_widget(self.download_location_label)

        self.download_button = Button(text="Download", size_hint=(1, 0.1), disabled=True)
        self.download_button.bind(on_press=self.download_song)
        self.add_widget(self.download_button)

        self.progress_bar = ProgressBar(value=0, max=100, size_hint=(1, 0.1))
        self.add_widget(self.progress_bar)

    def submit_api_key(self, instance):
        """Save the API key entered by the user and validate it."""
        self.app.api_key = self.api_input.text
        if self.validate_api_key():
            self.api_key_valid = True
            self.download_button.disabled = False
            self.show_popup("Success", "API Key validated and saved successfully!")
        else:
            self.api_key_valid = False
            self.download_button.disabled = True
            self.show_popup("Error", "Invalid API Key. Please try again.")

    def validate_api_key(self):
        """Validate the API key by making a test request to SoundCloud."""
        test_url = f"https://api.soundcloud.com/tracks?client_id={self.app.api_key}"
        response = requests.get(test_url)
        return response.status_code == 200

    def choose_download_location(self, instance):
        """Open a file chooser to select the download location."""
        filechooser = FileChooserIconView(filters=["!*.sys"], show_hidden=False)
        filechooser.bind(on_selection=self.select_location)
        popup = Popup(title="Select Download Location", content=filechooser, size_hint=(0.8, 0.8))
        popup.open()

    def select_location(self, filechooser, selection):
        """Set the selected download location."""
        if selection:
            self.app.download_location = selection[0]
            self.download_location_label.text = f"Download location: {self.app.download_location}"

    def download_song(self, instance):
        """Start downloading the song if API key and URL are provided."""
        if not self.app.api_key:
            self.show_popup("Error", "Please enter a valid API Key first.")
            return

        song_url = self.url_input.text
        if not song_url:
            self.show_popup("Error", "Please enter a song URL.")
            return

        if not self.app.download_location:
            self.show_popup("Error", "Please select a download location.")
            return

        self.start_download(song_url)

    def start_download(self, url):
        """Start the download in a separate thread."""
        download_thread = threading.Thread(target=self.download_file, args=(url,))
        download_thread.start()

    def download_file(self, url):
        """Download the file and update the progress bar."""
        local_filename = os.path.join(self.app.download_location, 'downloaded_song.mp3')
        response = requests.get(url, stream=True)

        with open(local_filename, 'wb') as f:
            total_length = int(response.headers.get('content-length', 0))
            downloaded = 0
            for data in response.iter_content(chunk_size=4096):
                downloaded += len(data)
                f.write(data)
                self.update_progress(downloaded / total_length * 100 if total_length > 0 else 0)

        self.show_popup("Success", "Download completed successfully!")

    def update_progress(self, percent):
        """Update the progress bar."""
        self.progress_bar.value = percent

    def show_popup(self, title, message):
        """Display a popup message."""
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.5, 0.5))
        popup.open()


class SoundCloudDownloaderApp(App):
    def build(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.download_location = os.path.join(current_dir, "downloads")
        if not os.path.exists(self.download_location):
            os.makedirs(self.download_location)
        self.api_key = None
        return MainPage(self)


if __name__ == '__main__':
    SoundCloudDownloaderApp().run()
