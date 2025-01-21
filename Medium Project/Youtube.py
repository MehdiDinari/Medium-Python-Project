import tkinter as tk
from tkinter import filedialog, messagebox
from pytube import YouTube


class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("500x250")
        self.root.resizable(False, False)

        # URL Input
        self.url_label = tk.Label(root, text="YouTube URL:", font=("Arial", 12))
        self.url_label.pack(pady=10)
        self.url_entry = tk.Entry(root, width=60, font=("Arial", 10))
        self.url_entry.pack(pady=5)

        # Save Path
        self.save_label = tk.Label(root, text="Save Location:", font=("Arial", 12))
        self.save_label.pack(pady=10)
        self.save_button = tk.Button(root, text="Select Folder", command=self.select_folder, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=15, height=1)
        self.save_button.pack(pady=5)
        self.save_path = tk.Label(root, text="", fg="blue", font=("Arial", 10))
        self.save_path.pack(pady=5)

        # Download Button
        self.download_button = tk.Button(root, text="Download Video", command=self.download_video, bg="#2196F3", fg="white", font=("Arial", 12, "bold"), width=20, height=2)
        self.download_button.pack(pady=20)

        # Save path variable
        self.folder_path = ""

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.save_path.config(text=self.folder_path)

    def download_video(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return

        if not self.folder_path:
            messagebox.showerror("Error", "Please select a save location.")
            return

        try:
            yt = YouTube(url)
            stream = yt.streams.filter(progressive=True, file_extension="mp4").get_highest_resolution()
            stream.download(output_path=self.folder_path)
            messagebox.showinfo("Success", "Video downloaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
