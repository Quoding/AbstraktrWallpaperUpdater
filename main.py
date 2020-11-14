from os.path import exists
from os import mkdir
from time import sleep
import ctypes
from win32com.shell import shell, shellcon
from requests import get
from bs4 import BeautifulSoup

# Globals
url = "http://deadauthor.org/art/"
image_path = ""
PICTURES_FOLDER = shell.SHGetFolderPath(0, shellcon.CSIDL_MYPICTURES, None, 0)
DIR = r"{}\abstrakt_images".format(PICTURES_FOLDER)


def download_image(url, path):
    r = get(url)
    with open(path, "wb") as f:
        f.write(r.content)


def get_latest_image(url):
    global DIR
    global image_path

    html_text = get(url).text
    soup = BeautifulSoup(html_text, "html.parser")
    images = soup.findAll("a", href=True)
    last_image_name = images[-1]["href"]

    image_url = url + last_image_name
    path = DIR + "/" + last_image_name
    image_path = path

    if not exists(path):
        download_image(image_url, path)


if __name__ == "__main__":
    if not exists(DIR):
        mkdir(DIR)

    while True:
        get_latest_image(url)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)
        sleep(3660)
