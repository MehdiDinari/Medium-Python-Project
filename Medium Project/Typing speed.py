import tkinter as tk
from tkinter import messagebox
import time
import random

# Load text from a file
def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()

class TypingTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speed Typing Test")
        self.root.geometry("800x400")
        self.root.configure(bg="#f7f7f7")

        self.target_text = load_text()
        self.current_text = ""
        self.start_time = None

        # UI Elements
        self.label_title = tk.Label(
            root, text="Speed Typing Test", font=("Helvetica", 24, "bold"), bg="#f7f7f7", fg="#333"
        )
        self.label_title.pack(pady=20)

        self.text_display = tk.Label(
            root, text=self.target_text, font=("Courier", 16), bg="#f7f7f7", wraplength=700, justify="left"
        )
        self.text_display.pack(pady=10)

        self.entry = tk.Entry(root, font=("Courier", 14), width=50)
        self.entry.pack(pady=20)
        self.entry.bind("<KeyRelease>", self.on_key_release)

        self.label_wpm = tk.Label(
            root, text="WPM: 0", font=("Helvetica", 16), bg="#f7f7f7", fg="#666"
        )
        self.label_wpm.pack(pady=10)

        self.button_restart = tk.Button(
            root, text="Restart", font=("Helvetica", 14), bg="#4CAF50", fg="white", command=self.restart
        )
        self.button_restart.pack(pady=20)

    def on_key_release(self, event):
        if self.start_time is None:
            self.start_time = time.time()

        self.current_text = self.entry.get()
        self.update_wpm()

        if self.current_text == self.target_text:
            self.finish_test()

    def update_wpm(self):
        elapsed_time = max(time.time() - self.start_time, 1)
        words_typed = len(self.current_text) / 5
        wpm = round(words_typed / (elapsed_time / 60))
        self.label_wpm.config(text=f"WPM: {wpm}")

    def finish_test(self):
        elapsed_time = time.time() - self.start_time
        words_typed = len(self.current_text) / 5
        wpm = round(words_typed / (elapsed_time / 60))
        messagebox.showinfo("Test Completed", f"You finished the test!\nWPM: {wpm}")
        self.restart()

    def restart(self):
        self.target_text = load_text()
        self.text_display.config(text=self.target_text)
        self.entry.delete(0, tk.END)
        self.current_text = ""
        self.start_time = None
        self.label_wpm.config(text="WPM: 0")

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTestApp(root)
    root.mainloop()
