import pyaudio
import numpy as np
import pygame
import tkinter as tk
window = tk.Tk()
window.title("amp")

note_label = tk.Label(window, text="Detected note: ")
note_label.pack()
amp_button = tk.Button(window, text="Off", command=lambda: toggle_amp(amp_button))
amp_button.pack()

def toggle_amp(button):
    if button["text"] == "Off":
        button["text"] = "On"
    else:
        button["text"] = "Off"

window.geometry("500x300")
window.mainloop()

notes = {
    'E': 82.41,
    'A': 110.00,
    'D': 146.83,
    'G': 196.00,
    'B': 246.94,
    'e': 329.63
}

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024)

pygame.mixer.init()

while True:
    data = np.frombuffer(stream.read(1024), dtype=np.float32)

    fft = np.fft.fft(data)
    frequency = np.argmax(np.abs(fft))

    closest_note = min(notes, key=lambda x: abs(notes[x] - frequency))

    print(f"Detected note: {closest_note}")

    pygame.mixer.Sound(f"{closest_note}.wav").play()
