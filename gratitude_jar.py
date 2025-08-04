
import tkinter as tk
from tkinter import messagebox
import os
import random
from datetime import datetime

# Constants
GRATITUDE_FILE = "gratitude_jar.txt"
JAR_WIDTH = 400
JAR_HEIGHT = 450
NOTE_COLORS = ["#FFD1DC", "#FFECB8", "#B5EAD7", "#C7CEEA", "#E2F0CB", "#FFDAC1"]

class GratitudeJar:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Virtual Gratitude Jar ✨")
        self.root.geometry("500x700+100+100")
        self.root.configure(bg="#FFF5EB")  # Soft peach background
        
        # Custom fonts
        self.font_normal = ("Comic Sans MS", 11)
        self.font_title = ("Comic Sans MS", 16, "bold")
        
        self.setup_ui()
        self.load_messages()

    def setup_ui(self):
        """Set up all UI elements"""
        # Header
        tk.Label(
            self.root, text="✨ Virtual Gratitude Jar ✨",
            font=self.font_title, bg="#FFF5EB", fg="#6A4C93"
        ).pack(pady=10)

        # Input area
        input_frame = tk.Frame(self.root, bg="#FFF5EB")
        input_frame.pack(pady=5)
        
        self.entry = tk.Text(
            input_frame, height=4, width=40,
            font=self.font_normal, bg="white",
            wrap=tk.WORD, padx=10, pady=10
        )
        self.entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            input_frame, text="Add Note 🌸",
            command=self.add_to_jar,
            font=self.font_normal, bg="#B5EAD7",
            activebackground="#FFB6C1", relief=tk.RAISED
        ).pack(side=tk.LEFT)

        # Jar canvas (for glass effect)
        self.canvas = tk.Canvas(
            self.root, width=JAR_WIDTH, height=JAR_HEIGHT,
            bg="#FFF5EB", highlightthickness=0
        )
        self.canvas.pack(pady=10)
        self.draw_jar_outline()

    def draw_jar_outline(self):
        """Draw transparent jar with glass effects"""
        # Jar body (light blue)
        self.canvas.create_rectangle(
            50, 50, JAR_WIDTH-50, JAR_HEIGHT-50,
            fill="#E6F3FF", outline="#A8D8EA", width=3
        )
        
        # Curved bottom
        self.canvas.create_oval(
            30, JAR_HEIGHT-70, JAR_WIDTH-30, JAR_HEIGHT+30,
            fill="#E6F3FF", outline="#A8D8EA", width=3
        )
        
        # Lid (wooden texture)
        self.canvas.create_oval(
            40, 20, JAR_WIDTH-40, 90,
            fill="#F0D5B5", outline="#D4B989", width=3
        )

    def add_to_jar(self):
        message = self.entry.get("1.0", tk.END).strip()
        if not message:
            messagebox.showwarning("Empty!", "Write something first!")
            return

        # Save to file
        with open(GRATITUDE_FILE, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d')}::{message}\n")
        
        # Create visual note
        self.create_note(message)
        self.entry.delete("1.0", tk.END)
        messagebox.showinfo("Added!", "Your note sparkles in the jar! ✨")

    def create_note(self, message):
        """Create a colorful note inside the jar"""
        note_color = random.choice(NOTE_COLORS)
        x = random.randint(70, JAR_WIDTH-120)
        y = random.randint(100, JAR_HEIGHT-100)
        
        # Note visual
        note_id = self.canvas.create_rectangle(
            x, y, x+100, y+40,
            fill=note_color, outline="#E0E0E0", width=1,
            tags=("note",)
        )
        
        # Note text (truncate if too long)
        text = message[:20] + "..." if len(message) > 20 else message
        text_id = self.canvas.create_text(
            x+50, y+20,
            text=text, font=self.font_normal,
            width=90, tags=("note",)
        )
        
        # Hover effect
        def on_enter(e):
            self.canvas.itemconfig(note_id, outline="gold", width=2)
            # Show full message in status bar
            self.root.status = tk.Label(
                self.root, text=message,
                bg="#FFF5EB", font=self.font_normal
            )
            self.root.status.pack()

        def on_leave(e):
            self.canvas.itemconfig(note_id, outline="#E0E0E0", width=1)
            if hasattr(self.root, 'status'):
                self.root.status.destroy()

        self.canvas.tag_bind(note_id, "<Enter>", on_enter)
        self.canvas.tag_bind(note_id, "<Leave>", on_leave)

    def load_messages(self):
        """Load existing messages into the jar"""
        if not os.path.exists(GRATITUDE_FILE): 
            return
            
        with open(GRATITUDE_FILE, "r", encoding="utf-8") as f:
            for line in f.readlines():
                parts = line.strip().split("::")
                if len(parts) == 2:
                    self.create_note(parts[1])

if __name__ == "__main__":
    root = tk.Tk()
    app = GratitudeJar(root)
    root.mainloop()
