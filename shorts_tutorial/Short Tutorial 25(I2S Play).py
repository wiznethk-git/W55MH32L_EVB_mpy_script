from machine import I2S, Pin
import gc

gc.collect()

# I2S pins (BCLK, LRC, DIN)
BCLK_PIN = "PB3"
LRC_PIN  = "PA15"
DIN_PIN  = "PB5"

audio = I2S(3, sck=Pin(BCLK_PIN), ws=Pin(LRC_PIN), sd=Pin(DIN_PIN),
            mode=I2S.TX, bits=16, format=I2S.STEREO, rate=44100, ibuf=20000)

# Calculate bytes for 15 seconds of 16‑bit stereo at 44.1 kHz
# 44100 samples/sec * 2 channels * 2 bytes/sample * 15 sec = 2,646,000 bytes
MAX_BYTES = 44100 * 2 * 2 * 15

with open("/sd/bg.wav", "rb") as f:
    f.seek(44)                     # skip WAV header
    buf = bytearray(4096)
    remaining = MAX_BYTES
    while remaining > 0 and (n := f.readinto(buf)):
        if n > remaining:
            n = remaining
        audio.write(buf[:n])
        remaining -= n

audio.deinit()
print("Played first 15 seconds.")