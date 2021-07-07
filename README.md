# AbstraktrWallpaperUpdater

A simple wallpaper updater that runs in the background and fetches the latest abstraktr.py image and sets it as your desktop wallpaper.

Windows is supported. For Linux, nitrogen is used as the wallpaper manager.

## Setup

Just use your scheduler (Windows' or crontab) to decide the interval at which you would like to fetch the new image. Keep in mind a new image is added approximately every hour. For crontab, this line will probably be useful `DISPLAY=":0.0"` as it seems crontab cannot find the default display to set the background on.

## Windows Defender

Some people might get an alert that this is a trojan. I'm not a Windows user, so I couldn't say for sure why, but if I had to guess it's because I'm interfacing with the Win32 API. If you don't trust the code, you can always clone the repo and build from source (I used pyinstaller), I think all the manipulations in the code are clear.

## Pictures folder

The pictures from abstraktr.py are saved locally in your User's Picture folder on Windows in a folder called `abstrakt_images`. On Linux, it's in `/home/<user>/Pictures/abstrakt_images`.

## Disclaimer

This is literally code I wrote in 30 minutes. It sucks
