import network
from machine import SPI, Pin, PWM
import socket, time, gc


spi = SPI(2, baudrate=8_000_000)
cs = Pin("PB12", Pin.OUT)
rst = Pin("PD9", Pin.OUT)

nic = network.WIZNET5K(spi, cs, rst)
nic.active(True)
nic.ifconfig(("169.254.100.20", "255.255.0.0", "169.254.1.1", "8.8.8.8"))
time.sleep(1)

ip = nic.ifconfig()[0]
print(f"Server: http://{ip}:8080")   # use port 8080 to avoid permission issues

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, 8080))
s.listen(5)
print("Listening...")

red_pwm = PWM(Pin("PA6", Pin.OUT), freq=1000)
green_pwm = PWM(Pin("PB9", Pin.OUT), freq=1000)
blue_pwm = PWM(Pin("PA0", Pin.OUT), freq=1000)

# ----- Copy of the working text server's structure -----
try:
    while True:
        conn = None
        try:
            conn, addr = s.accept()
            print("Client:", addr)
            request = conn.recv(1024).decode()
            

            if "GET /color?" in request:
                # Parse RGB values from query string
                try:
                    # Example: "/color?r=128&g=64&b=255"
                    params = request.split(' ')[1]    # "/color?r=128&g=64&b=255"
                    qs = params.split('?')[1]         # "r=128&g=64&b=255"
                    pairs = qs.split('&')
                    rgb = {}
                    for p in pairs:
                        k, v = p.split('=')
                        rgb[k] = int(v)
                    r_val = rgb.get('r', 0)
                    g_val = rgb.get('g', 0)
                    b_val = rgb.get('b', 0)
                    print("RGB set:", r_val, g_val, b_val)
                    # --- Control RGB LED (PWM) ---
                    red_pwm.duty(r_val)   # 0-255 → 0-65535
                    green_pwm.duty(g_val)
                    blue_pwm.duty(b_val)
                    
                except Exception as e:
                    print("Color parse error:", e)
            
            body = f"""<html>
<body>
    <h1>LED Control</h1>
    <br>
    <label>Red: <input type="range" id="r" min="0" max="255" value="0" oninput="update()"></label><br>
    <label>Green: <input type="range" id="g" min="0" max="255" value="0" oninput="update()"></label><br>
    <label>Blue: <input type="range" id="b" min="0" max="255" value="0" oninput="update()"></label>
    <br>
    <span>RGB: <span id="rgbValue">0,0,0</span></span>

    <script>
        function update() {{
            let r = document.getElementById('r').value;
            let g = document.getElementById('g').value;
            let b = document.getElementById('b').value;
            document.getElementById('rgbValue').innerText = r + ',' + g + ',' + b;
            fetch('/color?r=' + r + '&g=' + g + '&b=' + b);
        }}
    </script>
</body>
</html>"""
            body_bytes = body.encode('utf-8')
            
            header = "HTTP/1.0 200 OK\r\n"
            header += "Content-Type: text/html\r\n"
            header += "Content-Length: " + str(len(body_bytes)) + "\r\n"
            header += "Connection: close\r\n"
            header += "\r\n"
            
            conn.send(header.encode('utf-8'))
            conn.send(body_bytes)
            time.sleep(0.1)
            conn.close()
            print("Sent successfully")
            
            gc.collect()
            
        except Exception as e:
            if conn:
                conn.close()
            print("Error:", e)
            gc.collect()
            
except KeyboardInterrupt:
    print("\nServer stopped by user")
finally:
    s.close()
    print("Socket closed")