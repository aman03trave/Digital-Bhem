import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pygame
from tkinter import PhotoImage

# Initialize Pygame mixer
pygame.mixer.init()

# Create main application window
root = tk.Tk()
root.title("Simple Music Player")
root.geometry("500x200")
root.resizable(False, False)

# Global variable to track if a song is loaded
song_loaded = False

# Define functions for music control
def open_file():
    global song_loaded
    file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
    if file_path:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        song_label.config(text=f"Playing: {file_path.split('/')[-1]}")
        song_loaded = True

def play_music():
    if song_loaded:
        pygame.mixer.music.unpause()
        song_label.config(text="Playing")
    else:
        messagebox.showwarning("No Song", "No song is loaded. Please load a song first.")

def pause_music():
    if song_loaded:
        pygame.mixer.music.pause()
        song_label.config(text="Paused")
    else:
        messagebox.showwarning("No Song", "No song is loaded. Please load a song first.")

def stop_music():
    if song_loaded:
        pygame.mixer.music.stop()
        song_label.config(text="Stopped")
    else:
        messagebox.showwarning("No Song", "No song is loaded. Please load a song first.")

def set_volume(val):
    volume = float(val) / 100
    pygame.mixer.music.set_volume(volume)

# Create frames for better layout
frame_controls = tk.Frame(root)
frame_controls.pack(pady=20)

frame_volume = tk.Frame(root)
frame_volume.pack(pady=10)

# Load icons for buttons and resize them
icon_open = PhotoImage(file='icons/open.png').subsample(10, 10)  # Resizing by a factor of 10
icon_play = PhotoImage(file='icons/play.png').subsample(10, 10)
icon_pause = PhotoImage(file='icons/pause.png').subsample(10, 10)
icon_stop = PhotoImage(file='icons/stop.png').subsample(10, 10)

# Create and place buttons with icons
btn_open = tk.Button(frame_controls, text="Open", image=icon_open, compound=tk.LEFT, command=open_file)
btn_open.grid(row=0, column=0, padx=10)

btn_play = tk.Button(frame_controls, text="Play", image=icon_play, compound=tk.LEFT, command=play_music)
btn_play.grid(row=0, column=1, padx=10)

btn_pause = tk.Button(frame_controls, text="Pause", image=icon_pause, compound=tk.LEFT, command=pause_music)
btn_pause.grid(row=0, column=2, padx=10)

btn_stop = tk.Button(frame_controls, text="Stop", image=icon_stop, compound=tk.LEFT, command=stop_music)
btn_stop.grid(row=0, column=3, padx=10)

# Create and place song label
song_label = tk.Label(root, text="No song loaded", fg="blue", font=("Helvetica", 12))
song_label.pack(pady=10)

# Create and place volume control
volume_label = tk.Label(frame_volume, text="Volume")
volume_label.pack(side=tk.LEFT)

volume_slider = ttk.Scale(frame_volume, from_=0, to=100, orient=tk.HORIZONTAL, command=set_volume)
volume_slider.set(50)  # Set default volume to 50%
volume_slider.pack(side=tk.RIGHT)

# Run the application
root.mainloop()
