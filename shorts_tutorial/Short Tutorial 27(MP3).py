import mp3
from machine import I2S, Pin
import time
import gc

filename = "/sd/haha.mp3"
I2S_ID = 3
SCK_PIN = Pin("PB3")
WS_PIN = Pin("PA15")
SD_PIN = Pin("PB5")
MP3_IN_BUF_SIZE = 4096
PCM_FRAME_SIZE = 4608
I2S_IBUF_SIZE = 8192
GC_EVERY_FRAMES = 20
PRINT_EVERY_FRAMES = 100

in_buffer = bytearray(MP3_IN_BUF_SIZE)
pcm_buf = bytearray(PCM_FRAME_SIZE)
dec = None
i2s = None

def skip_id3(f):
    header = f.read(10)
    if header.startswith(b"ID3") and len(header) == 10:
        size_bytes = header[6:10]
        id3_size = ((size_bytes[0] << 21) | (size_bytes[1] << 14) | (size_bytes[2] << 7) | size_bytes[3]) + 10
        f.seek(id3_size)
    else:
        f.seek(0)

def refill_buffer(f, buffer_view, bytes_used):
    remaining = buffer_view[bytes_used:]
    rem_len = len(remaining)
    in_buffer[:rem_len] = remaining
    mv = memoryview(in_buffer)
    new_read = f.readinto(mv[rem_len:])
    if new_read is None:
        new_read = 0
    return mv[:rem_len + new_read], new_read

try:
    time.sleep_ms(300)
    gc.collect()
    dec = mp3.Decoder()
    dec.volume(80)

    with open(filename, "rb") as f:
        skip_id3(f)
        bytes_read = f.readinto(in_buffer)
        if bytes_read is None:
            bytes_read = 0
        buffer_view = memoryview(in_buffer)[:bytes_read]

        first_len = 0
        channels = 2
        rate = 44100

        while len(buffer_view) > 0:
            res = dec.decode(buffer_view)
            if isinstance(res, int):
                break
            bytes_used, pcm_data, channels, rate, bitrate = res
            if bytes_used <= 0:
                break
            buffer_view, new_read = refill_buffer(f, buffer_view, bytes_used)
            if len(pcm_data) > 0:
                first_len = len(pcm_data)
                if first_len > len(pcm_buf):
                    first_len = 0
                    break
                pcm_buf[:first_len] = pcm_data
                break

        if first_len <= 0:
            print("No valid PCM frame found")
        else:
            gc.collect()
            time.sleep_ms(50)
            i2s = I2S(I2S_ID, sck=SCK_PIN, ws=WS_PIN, sd=SD_PIN,
                      mode=I2S.TX, bits=16,
                      format=I2S.STEREO if channels == 2 else I2S.MONO,
                      rate=rate, ibuf=I2S_IBUF_SIZE)
            time.sleep_ms(20)
            if first_len == len(pcm_buf):
                i2s.write(pcm_buf)
            else:
                i2s.write(memoryview(pcm_buf)[:first_len])

            frame_count = 0
            while len(buffer_view) > 0:
                t0 = time.ticks_us()
                res = dec.decode(buffer_view)
                decode_us = time.ticks_diff(time.ticks_us(), t0)
                if isinstance(res, int):
                    break
                bytes_used, pcm_data, channels, rate_now, bitrate = res
                if bytes_used <= 0:
                    break
                n = len(pcm_data)
                write_us = 0
                if n > 0:
                    if n > len(pcm_buf):
                        break
                    pcm_buf[:n] = pcm_data
                    t1 = time.ticks_us()
                    if n == len(pcm_buf):
                        i2s.write(pcm_buf)
                    else:
                        i2s.write(memoryview(pcm_buf)[:n])
                    write_us = time.ticks_diff(time.ticks_us(), t1)
                buffer_view, new_read = refill_buffer(f, buffer_view, bytes_used)
                frame_count += 1
                if frame_count % PRINT_EVERY_FRAMES == 0:
                    print("frame:", frame_count, "decode_us:", decode_us, "write_us:", write_us, "free:", gc.mem_free())
                if frame_count % GC_EVERY_FRAMES == 0:
                    gc.collect()
                if new_read == 0 and len(buffer_view) == 0:
                    break
            print("Playback finished. frames:", frame_count)

except KeyboardInterrupt:
    print("Stopped by Ctrl+C")
finally:
    try:
        if i2s is not None:
            time.sleep_ms(50)
            i2s.deinit()
            time.sleep_ms(150)
    except Exception as e:
        print("i2s.deinit error:", e)
    try:
        if dec is not None:
            dec.deinit()
            time.sleep_ms(20)
    except Exception as e:
        print("dec.deinit error:", e)
    gc.collect()
    print("cleanup done")