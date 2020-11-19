#!/bin/python
from os.path import exists
from os import mkdir
import subprocess
from time import sleep
from datetime import datetime
import platform
import getpass
import ctypes
import logging
from requests import get
from bs4 import BeautifulSoup

try:
    from win32com.shell import shell, shellcon
except ImportError:
    logging.warning(
        "PyWin32 could not be imported. This is not an issue if you are not on Windows"
    )

# Globals
url = "https://deadauthor.org/art/"
image_path = ""

OS_NAME = platform.system()

if OS_NAME == "Windows":
    PICTURES_FOLDER = shell.SHGetFolderPath(0, shellcon.CSIDL_MYPICTURES, None, 0)
    DIR = r"{}\abstrakt_images".format(PICTURES_FOLDER)

elif OS_NAME == "Linux":
    PICTURES_FOLDER = "/home/{}/Pictures".format(getpass.getuser())
    DIR = "{}/abstrakt_images".format(PICTURES_FOLDER)
else:
    raise ("{} is not currently supported".format(OS_NAME))


def get_dates(datelines):
    dates = [
        " ".join(date.strip().split(" ")[0:2]) for date in datelines
    ]  # Extract just the motherfucking date from this shitty ass format

    dates = [datetime.strptime(date, "%d-%b-%Y %H:%M") for date in dates]

    return dates


def download_image(url, path):
    r = get(url)
    with open(path, "wb") as f:
        f.write(r.content)


def get_latest_image(url):
    global DIR
    global image_path

    html_text = get(url).text
    soup = BeautifulSoup(html_text, "html.parser")
    lines = soup.find("pre").contents
    images = lines[2::2]
    datelines = lines[3::2]

    dates = get_dates(datelines)

    image_dates = list(zip(images, dates))
    image_dates = sorted(image_dates, key=lambda t: t[1], reverse=True)

    last_image_name = image_dates[0][0].get_text()

    image_url = url + last_image_name
    path = DIR + "/" + last_image_name
    image_path = path

    if not exists(path):
        download_image(image_url, path)


def change_wallpaper():
    if OS_NAME == "Windows":
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)
    elif OS_NAME == "Linux":
        command = "nitrogen --set-scaled {}".format(image_path)
        subprocess.call(command.split())


if __name__ == "__main__":
    if not exists(DIR):
        mkdir(DIR)

    get_latest_image(url)
    change_wallpaper()
