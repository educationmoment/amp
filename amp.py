import pyaudio
import numpy as np
import pygame
import tkinter as tk
# Create the tkinter window
window = tk.Tk()
window.title("amp")

# Create a label to display the detected note
note_label = tk.Label(window, text="Detected note: ")
note_label.pack()

# Create a button to toggle the amp on/off
amp_button = tk.Button(window, text="Off", command=lambda: toggle_amp(amp_button))
amp_button.pack()

# Function to toggle the amp on/off
def toggle_amp(button):
    if button["text"] == "Off":
        button["text"] = "On"
    else:
        button["text"] = "Off"

# Start the tkinter event loop
window.geometry("500x300")
window.mainloop()

# Define the frequencies of each note
notes = {
    'E': 82.41,
    'A': 110.00,
    'D': 146.83,
    'G': 196.00,
    'B': 246.94,
    'e': 329.63
}

# Initialize PyAudio
p = pyaudio.PyAudio()

# Set up the audio stream
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024)

# Initialize Pygame
pygame.mixer.init()

# Main loop
while True:
    # Read audio input from the guitar
    data = np.frombuffer(stream.read(1024), dtype=np.float32)

    # Perform frequency analysis on the audio data
    fft = np.fft.fft(data)
    frequency = np.argmax(np.abs(fft))

    # Find the closest note to the detected frequency
    closest_note = min(notes, key=lambda x: abs(notes[x] - frequency))

    # Print the detected note
    print(f"Detected note: {closest_note}")

    # Play the corresponding sound of the note
    pygame.mixer.Sound(f"{closest_note}.wav").play()