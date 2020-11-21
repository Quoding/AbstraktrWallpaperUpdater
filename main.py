#!/bin/python
from os.path import exists
from os import mkdir
import subprocess
import platform
import getpass
import ctypes
import logging
from secret import *
import json

from requests import get
import pytumblr


# Globals
URL = "https://abstraktr.m1q.net"
BLOG_NAME = "abstraktr.m1q.net"
image_path = ""
OS_NAME = platform.system()


try:
    from win32com.shell import shell, shellcon
except ImportError:
    logging.warning(
        "PyWin32 could not be imported. This is not an issue if you are not on Windows"
    )

if OS_NAME == "Windows":
    PICTURES_FOLDER = shell.SHGetFolderPath(0, shellcon.CSIDL_MYPICTURES, None, 0)
    DIR = r"{}\abstrakt_images".format(PICTURES_FOLDER)

elif OS_NAME == "Linux":
    PICTURES_FOLDER = "/home/{}/Pictures".format(getpass.getuser())
    DIR = "{}/abstrakt_images".format(PICTURES_FOLDER)
else:
    raise ("{} is not currently supported".format(OS_NAME))


def download_image(url, path):
    r = get(url)
    with open(path, "wb") as f:
        f.write(r.content)


def get_image(url, id_):
    global DIR
    path = DIR + "/" + id_ + ".png"

    if not exists(path):
        download_image(url, path)

    return path


def change_wallpaper(image_path):
    if OS_NAME == "Windows":
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)
    elif OS_NAME == "Linux":
        command = "nitrogen --set-scaled {}".format(image_path)
        subprocess.call(command.split())


if __name__ == "__main__":

    client = pytumblr.TumblrRestClient(
        CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET
    )

    js = client.posts(BLOG_NAME, type="photo", limit=1)
    url = js["posts"][0]["photos"][0]["alt_sizes"][0]["url"]
    id_ = js["posts"][0]["id_string"]

    image_path = get_image(url, id_)
    if not exists(DIR):
        mkdir(DIR)

    change_wallpaper(image_path)