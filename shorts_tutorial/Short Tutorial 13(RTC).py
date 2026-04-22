import machine
machine.usb_mode('VCP+MSC')

with open('test.txt', 'w') as f:
    f.write('USB MSC test\r\n')
    
with open('test.txt', 'r') as f:
    data = f.read()

print(data)