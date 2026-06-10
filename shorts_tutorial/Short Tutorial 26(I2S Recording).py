from machine import I2S, Pin
import time
import gc

gc.collect()

# ===== Adjustable gain (increase if mic is too quiet) =====
GAIN = 4          # try 2, 4, 8; higher may cause distortion

# ===== Shared I2S pins =====
BCLK = "PB3"
LRC  = "PA15"

# ===== Data pins =====
DATA = "PB5"   # speaker DIN

# ===== Button =====
btn = Pin("PG8", Pin.IN)

# ===== Button =====
LED = Pin("PG7", Pin.OUT)

# ===== Audio settings =====
SAMPLE_RATE = 8000     # 8 kHz (memory‑friendly)
RECORD_SECS = 10        # max 5 seconds
CHUNK_SIZE = 1024      # small buffer
WAV_FILE = "/sd/memo.wav"

# ===== Helper: apply gain to 16‑bit mono samples =====
def apply_gain(buf, gain):
    """Multiply each 16‑bit little‑endian sample by gain, clamp to ±32767"""
    for i in range(0, len(buf), 2):
        # Combine two bytes into signed 16‑bit integer
        sample = buf[i] | (buf[i+1] << 8)
        if sample & 0x8000:          # negative
            sample = sample - 0x10000
        # Multiply and clamp
        sample = sample * gain
        if sample > 32767:
            sample = 32767
        elif sample < -32768:
            sample = -32768
        # Write back as little‑endian
        buf[i]   = sample & 0xFF
        buf[i+1] = (sample >> 8) & 0xFF

# ===== Helper: create WAV header =====
def make_wav_header(num_samples):
    data_size = num_samples * 2   # 16‑bit mono = 2 bytes/sample
    header = bytearray(44)
    header[0:4]  = b'RIFF'
    header[4:8]  = (data_size + 36).to_bytes(4, 'little')
    header[8:12] = b'WAVE'
    header[12:16] = b'fmt '
    header[16:20] = (16).to_bytes(4, 'little')
    header[20:22] = (1).to_bytes(2, 'little')
    header[22:24] = (1).to_bytes(2, 'little')   # mono
    header[24:28] = (SAMPLE_RATE).to_bytes(4, 'little')
    byte_rate = SAMPLE_RATE * 2
    header[28:32] = (byte_rate).to_bytes(4, 'little')
    block_align = 2
    header[32:34] = (block_align).to_bytes(2, 'little')
    header[34:36] = (16).to_bytes(2, 'little')
    header[36:40] = b'data'
    header[40:44] = (data_size).to_bytes(4, 'little')
    return header

# ===== Record =====
def record():
    LED.on()
    print(f"Recording... (gain={GAIN}, hold button, release to stop)")
    i2s = I2S(3, sck=Pin(BCLK), ws=Pin(LRC), sd=Pin(DATA),
              mode=I2S.RX, bits=16, format=I2S.MONO, rate=SAMPLE_RATE, ibuf=20000)
    with open(WAV_FILE, "wb") as f:
        f.write(bytearray(44))          # placeholder header
        buf = bytearray(CHUNK_SIZE)
        total = 0
        start = time.ticks_ms()
        while btn.value() == 0:         # button pressed
            n = i2s.readinto(buf)
            if n:
                apply_gain(buf, GAIN)   # <── amplify here
                f.write(buf[:n])
                total += n
            if time.ticks_diff(time.ticks_ms(), start) > RECORD_SECS * 1000:
                break
    i2s.deinit()
    print(f"Recorded {total} bytes")
    # fix header
    samples = total // 2
    header = make_wav_header(samples)
    with open(WAV_FILE, "r+b") as f:
        f.write(header)
    gc.collect()
    LED.off()

# ===== Playback (mono to stereo conversion) =====
def playback():
    print("Playing...")
    i2s = I2S(3, sck=Pin(BCLK), ws=Pin(LRC), sd=Pin(DATA),
              mode=I2S.TX, bits=16, format=I2S.STEREO, rate=SAMPLE_RATE, ibuf=20000)
    with open(WAV_FILE, "rb") as f:
        f.seek(44)      # skip header
        buf = bytearray(CHUNK_SIZE)
        while True:
            n = f.readinto(buf)
            if n == 0:
                break
            # Convert mono (n bytes) to stereo (n*2 bytes)
            stereo = bytearray(n * 2)
            for i in range(0, n, 2):
                stereo[i*2]   = buf[i]
                stereo[i*2+1] = buf[i+1]
                stereo[i*2+2] = buf[i]
                stereo[i*2+3] = buf[i+1]
            i2s.write(stereo)
    i2s.deinit()
    print("Done")
    gc.collect()

# ===== Main =====
print("Hold button to record (max 10s), release to play")
while True:
    if btn.value() == 0:
        time.sleep_ms(50)
        if btn.value() == 0:
            record()
            playback()
            while btn.value() == 0:
                time.sleep_ms(50)
    time.sleep_ms(50)