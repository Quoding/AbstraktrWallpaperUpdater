from os.path import exists
from os import mkdir
from time import sleep
from datetime import datetime
import ctypes
from win32com.shell import shell, shellcon
from requests import get
from bs4 import BeautifulSoup

# Globals
url = "https://deadauthor.org/art/"
image_path = ""
PICTURES_FOLDER = shell.SHGetFolderPath(0, shellcon.CSIDL_MYPICTURES, None, 0)
DIR = r"{}\abstrakt_images".format(PICTURES_FOLDER)


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


if __name__ == "__main__":
    if not exists(DIR):
        mkdir(DIR)

    while True:
        get_latest_image(url)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)
        sleep(3660)
