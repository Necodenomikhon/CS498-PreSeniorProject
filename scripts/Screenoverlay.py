import tkinter as tk
from tkinter import ttk
import random

class Overlay:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Remove window decorations
        
        self.root.attributes('-topmost', True)  # Keep window on top
        self.root.attributes('-transparentcolor', '#abcdef')  # Set transparent color

        self.text_label = tk.Label(self.root, text="", font=("Arial", 24), bg="#ffffff", fg="black")
        self.text_label.pack()

        self.update_text("")

    def update_text(self, text):
        self.text_label.config(text=text)

def main():
    root = tk.Tk()
    overlay = Overlay(root)
    

    # Simulate receiving text from a separate program
    def receive_text():
        words = ["Press escape to quit", "banana", "cherry", "date", "elderberry","This is a scam","This is not a scam","Don't click any links"]
        text = random.choice(words)
        overlay.update_text(text)
        root.after(1000, receive_text)  # Update text every 1 second
    def quit_program(event=None):
        root.destroy()

    #pressing escape key will quit the program
    root.bind("<Escape>", quit_program)
    receive_text()

    root.mainloop()

if __name__ == "__main__":
    main()