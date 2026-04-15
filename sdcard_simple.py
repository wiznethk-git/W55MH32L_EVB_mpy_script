with open("/sd/testing.txt", "w") as f:
    f.write(f"Hi from W55MH32!")

with open("/sd/testing.txt", "r") as f:
    data= f.read()
    print(data)
