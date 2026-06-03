import music
from machine import Pin

# Play a built‑in melody 
print("Playing PUNCHLINE...")

music.play(music.PUNCHLINE,Pin("PD15", Pin.OUT))

# Wait for playback to finish (the `play` function is blocking)
print("Done.")

