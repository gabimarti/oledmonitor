#!/usr/bin/python3

import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# A few constants
LOOP_DELAY = 0.5        # Time to refresh display in seconds
LINE_HEIGHT = 11        # Line height in pixels


# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Note you can change the I2C address by passing an i2c_address parameter like:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

# Alternatively you can specify an explicit I2C bus number, for example
# with the 128x32 display you would use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=2)

# 128x32 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 128x64 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Alternatively you can specify a software SPI implementation by providing
# digital GPIO pin numbers for all the required display pins.  For example
# on a Raspberry Pi with the 128x32 display you might use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, sclk=18, din=25, cs=22)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# text encoding
encoding = 'utf-8'

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -5
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 2  # left margin

# Load default font.
# font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)
font = ImageFont.truetype('PixelOperator.ttf', 16)

# Some functions
# Print default line with default font and fill
def print_line(left_margin, line_num, text):
   draw.text((left_margin, line_num*LINE_HEIGHT), text, font=font, fill=255)

def draw_black_frame_outline():
   draw.rectangle((0, 0, width-1, height-1), outline=16, fill=0)


while True:
   # Draw a black filled box to clear the image.
   draw_black_frame_outline()

   # Obtain CPU Temperature
   # cputemp = CPUTemperature()
   cmd = "vcgencmd measure_temp"
   GPUtemp = subprocess.check_output(cmd, shell = True )
   cmd = "cat /sys/class/thermal/thermal_zone0/temp"
   CPUtemp = int(subprocess.check_output(cmd, shell = True )) / 1000

   # Obtiene tiempo hora, tiempo encendido y usuarios conectados
   TimeUsers = "uptime | awk '{print $1 \"  \" $3 \" Us \" $4}'"
   TimeUsers = subprocess.check_output(TimeUsers, shell = True)

   # Obtiene consumo CPU
   CPU1 = "grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage \"%\"}'"
   CPU1 = subprocess.check_output(CPU1, shell = True)


   # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
   cmd = "hostname -I | cut -d\' \' -f1"
   IP = subprocess.check_output(cmd, shell = True )
   cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
   CPU = subprocess.check_output(cmd, shell = True )
   cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
   MemUsage = subprocess.check_output(cmd, shell = True )
   # cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
   # Disk = subprocess.check_output(cmd, shell = True )

   # Write two lines of text.

   print_line(x, 0, "IP: " + str(IP, encoding))
   print_line(x, 1, str(TimeUsers, encoding))
   print_line(x, 2, "Load: " + str(CPU1, encoding))
   print_line(x, 3, str(MemUsage, encoding))
   print_line(x, 4, "CPU: " + str(CPUtemp) + " GPU " + str(GPUtemp, encoding))
   # draw.text((x, top+25),    str(Disk),  font=font, fill=255)

   # Display image.
   disp.image(image)
   disp.display()
   time.sleep(LOOP_DELAY)
