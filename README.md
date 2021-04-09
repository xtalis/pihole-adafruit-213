# pihole-adafruit-213
Displays Pihole info on a AdaFruit 2.13" EInk screen

<img src="https://github.com/xtalis/pihole-adafruit-213/blob/main/stats.py.png?raw=true" width="250">

### Preparing for use ###
Assuming you are starting with a bare Raspian install, you will need to run the following commands.
This will install Python3, Adafruit CircuitPythonEPD and some font and imaging library.

```bash
sudo su
apt update & apt upgrade -y
apt install python3-pip
pip3 install --upgrade setuptools
pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
python3 raspi-blinka.py
pip3 install adafruit-circuitpython-epd
wget https://github.com/adafruit/Adafruit_CircuitPython_framebuf/raw/master/examples/font5x8.bin
apt-get install ttf-dejavu
apt-get install python3-pil
```

Of course also install [Pi-Hole](https://pi-hole.net/)
```
curl -sSL https://install.pi-hole.net | bash
```

or

```
wget -O basic-install.sh https://install.pi-hole.net
sudo bash basic-install.sh
```
### Usage ###

`python3 stats.py`

#### Cron ####

If you change the .py script to be executable, you can add a cron job.

`chmod a+x stats.py`

...and add this line to /etc/crontab ('sudo pico /etc/crontab')...

`10 *    * * *   root    /home/pi/stats.py`

...this will run at 10 minutes past each hour.


### License ###
Licensed under [GLWTPL](https://github.com/me-shaon/GLWTPL/)
