from time import sleep_ms

SEGMENT_MAP = [0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F,
               0x77,0x7C,0x39,0x5E,0x79,0x71,0x00]

CHAR_TO_SEG = {
    '0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,
    'A':10,'b':11,'C':12,'d':13,'E':14,'F':15,' ':16,'-':16,'_':16
}

class TM1650:
    def __init__(self, i2c):
        self.i2c = i2c
        self.buffer = [0]*4
        self._init_display()

    def _init_display(self):
        self.write_cmd(0x24, 0x01)
        self.set_brightness(3)

    def write_cmd(self, addr, data):
        try:
            self.i2c.writeto(addr, bytes([data]))
        except:
            pass

    def write_digit(self, pos, value, dp=False):
        if 0 <= pos <= 3 and 0 <= value <= 9:
            seg = SEGMENT_MAP[value]
            if dp:
                seg |= 0x80
            self.buffer[pos] = seg
            self._update()

    def _update(self):
        for i, seg in enumerate(self.buffer):
            self.i2c.writeto(0x34 + i, bytes([seg]))

    def show(self, value):
        s = "%4s" % str(value).upper()[:4]
        for i, c in enumerate(s):
            idx = CHAR_TO_SEG.get(c, 16)
            self.write_digit(i, idx, dp=False)

    def show_number(self, num, leading_zeros=False):
        s = f"{num:04d}" if leading_zeros else f"{num:4d}"
        self.show(s)

    def show_float(self, value, decimals=1):
        self.show_number(int(value))

    def set_brightness(self, level):
        level = max(0, min(7, level))
        if level == 0:
            self.write_cmd(0x24, 0x00)
        else:
            cmd = 0x01 | (level << 4)
            self.write_cmd(0x24, cmd)

    def display_on(self):
        self.set_brightness(7)

    def display_off(self):
        self.set_brightness(0)

    def clear(self):
        self.buffer = [0]*4
        self._update()

    def test(self):
        self.show("8888")
        sleep_ms(800)
        self.clear()
        sleep_ms(300)
        for i in range(10):
            self.show_number(i*1111)
            sleep_ms(180)
        self.show("done")
        sleep_ms(1200)
        self.clear()