import serial
import time 

class PM8155():
    def __init__(self, paper_size="A4") -> None:
        self.serial_port = serial.Serial(
            port="/dev/tty.usbserial-B000PAHI",
            baudrate=9600,
            bytesize=serial.SEVENBITS,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE,
            xonxoff=True,
            timeout=1
        )
        self.paper_size = paper_size
        self.dimensions = () # TODO: set dimensions based on paper_size

    def _write(self, command, pause=0.2):
        # If the command does not end with a terminator, add it
        if not command.endswith(";"):
            command = command + ";"

        command_in_bytes = str.encode(command)
        self.serial_port._write(command_in_bytes)
        time.sleep(pause) # Sleep a bit between commands..

    def move(self, x, y):
        self._write(f"PU{x},{y};")

    def point(self, x, y):
        self.move(x, y)
        self._write("PD;") 
        self._write("PU;")

    def line(self, x1, y1, x2, y2):
        self.move(x1, y1)
        self._write(f"PD{x2},{y2};")

    def rect(self, x, y, width, height):
        # Move to X,Y with the pen up
        self.move(x,y)
        self._write(f"PA{x+width},{y}")
        self._write(f"PA{x+width},{y+height}")
        self._write(f"PA{x},{y+height}")
        self._write(f"PA{x},{y}")

    def circle(self, x, y, radius):
        # Move to X,Y with the pen up
        self.move(x,y)
        # https://www.isoplotec.co.jp/HPGL/eHPGL.htm#-CI(Circle)
        self._write(f"CT0.1;")
        self._write(f"CI{radius};")