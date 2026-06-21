# Lemonade
An open source, pocket-sized game console, able to load any pygame program with just a little modification! Parts are relatively cheap, and it's **open source**, meaning anyone can make it (with enough movitvation)!

## Use
**BEFORE ASSEMBLING COMPONENTS, PLEASE FOLLOW THE USE IN https://github.com/laojoh/Lemonade-Driver,** it will help guide the initial TFT SPI Display set up process. 

### Use within console

This is a little guide to setup certain things within the console.

### Use PuTTY to SSH into your Raspberry Pi

to make internal changes to the raspberry pi and run this repo, follow these steps!

1. Clone **this branch** of the repository

You can do that with this command (assuming you have git installed):

```
git clone -b console https://github.com/laojoh/Lemonade
```

2. Editing rc.local to execute driver on startup

Ok, this is a big one. 
After installing the driver, reinstall raspi-config to change one setting:

```
sudo apt install raspi-config

[wait for it to install]

sudo raspi-config
```

From there, enter the system settings, and the autologin option. **Enable it**

now finish, and after getting back to the main screen, access another file:

```
sudo nano /etc/rc.local
```

From there, hold CTRL+K to delete everything. Replace it with this:

```
#! /bin/sh -e

/home/[user]/Lemonade-Driver/build/fbcp-ili9341 &

cd home/[user]/Lemonade/assets
python3 /home/[user]/Lemonade/assets/Home.py

exit 0
```

That is the startup script for what the pi should do at startup. 

## Why?
You might be asking yourself, why make this in the first place??

Well, here's your answer. Cheapish game consoles don't really exist anymore. the 3DS and gameboy aren't really around (albeit people still have them), and the nintendo switch or steamdeck is just wayyy too much, not only in terms of price, but also in size. The Playdate is the size exception, but not the price exception. Making this an open source project allows people to make their own games, learn pygame, and be able to use it for entertainment!
