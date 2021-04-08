#!/usr/bin/python3
import digitalio
import busio
import board
import subprocess
import requests
import json
from adafruit_epd.epd import Adafruit_EPD
from PIL import Image, ImageDraw, ImageFont

 
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)
srcs = None

large_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
large_font_italic = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf", 20)
small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10)

api_url = 'http://localhost/admin/api.php'

height = 122
width = 250
x = width - 250 #0?!
y = height - 122


from adafruit_epd.ssd1675 import Adafruit_SSD1675
display = Adafruit_SSD1675(122, 250, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=srcs,rst_pin=rst, busy_pin=busy)
display.rotation = 3

display.fill(Adafruit_EPD.WHITE)
 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

image = Image.new("RGB", (250, 122), color=WHITE)
draw = ImageDraw.Draw(image)


cmd = "hostname -I | cut -d\' \' -f1 | tr -d \'\\n\'"
IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
cmd = "hostname | tr -d \'\\n\'"
HOST = subprocess.check_output(cmd, shell=True).decode("utf-8")
cmd = "top -bn1 | grep load | awk " \
      "'{printf \"CPU: %.2f\", $(NF-2)}'"
CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
cmd = "free -m | awk 'NR==2{printf " \
      "\"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
cmd = "df -h | awk '$NF==\"/\"{printf " \
      "\"Disk: %d/%dGB %s\", $3,$2,$5}'"
Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
cmd = "date | cut -d \' \' -f5"
DATER = subprocess.check_output(cmd, shell=True).decode("utf-8")


try:
        r = requests.get(api_url)
        data = json.loads(r.text)
        CLIENTS = data['unique_clients']
        BLOCKDOMAINS = data['domains_being_blocked']
        ADSPERCENTAGE = data['ads_percentage_today']  
        DNSQUERIES = data['dns_queries_today']
        ADSBLOCKED = data['ads_blocked_today']
        QUERYCACHE = data['queries_cached']
        QUERYFWD = data['queries_forwarded']
        
except KeyError:
        time.sleep(1)


STATUS = str("{:,}".format(BLOCKDOMAINS)) + " on blacklist."

draw.text(  (x,                 y),     "[" + HOST + "]",       font=large_font_italic,fill=BLACK)
draw.text(  ((width / 2) - 28,  y),     IP + '  |  ' + DATER,   font=small_font, fill=BLACK)
draw.text(  ((width / 2) - 28,  y+12),  STATUS,                 font=small_font, fill=BLACK)

draw.text(  (x,                 y+22),   CPU + " | " + Disk,    font=small_font, fill=BLACK)
draw.text(  (x,                 y+32),   MemUsage,              font=small_font, fill=BLACK)

draw.text(  (x,                 y+42),   "queries",             font=large_font, fill=BLACK)
draw.text(  ((width/2) - 25,    y+42),   str(DNSQUERIES),       font=large_font, fill=BLACK)

draw.text(  (x,                 y+60),   "blocked",             font=large_font_italic, fill=BLACK)
draw.text(  ((width/2) - 25,    y+60),   str(ADSBLOCKED),       font=large_font_italic, fill=BLACK)
draw.text(  (((width/4) * 3) - 25,y+60), "(" + str(round(ADSPERCENTAGE,1)) + "%)",  font=large_font_italic, fill=BLACK)

draw.text(  (x,                 y+78),   "cached",              font=large_font, fill=BLACK)
draw.text(  ((width/2) - 25,    y+78),   str(QUERYCACHE),       font=large_font, fill=BLACK)

draw.text(  (x,                 y+96),   "forward",             font=large_font, fill=BLACK)
draw.text(  ((width/2) - 25,    y+96),   str(QUERYFWD),         font=large_font, fill=BLACK)


display.image(image)
display.display()