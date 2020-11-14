# AbstraktrWallpaperUpdater
 A simple Windows (yikes) wallpaper updater that runs in the background and fetches the latest abstraktr.py image every 61 minutes.

## Windows Defender
Some people might get an alert that this is a trojan. I'm not a Windows user, so I couldn't say for sure why, but if I had to guess it's because I'm interfacing with the Win32 API. If you don't trust the code, you can always clone the repo and build from source (I used pyinstaller), I think all the manipulations in the code are clear.

## Startup task
If you want this code to run at startup, try putting it on the startup list of programs on Windows 10 (CTRL + R: type shell:startup and put the .exe file in there, it should appear when you go on the Startup tab in the task manager)

## Disclaimer
 This is literally code I wrote in 30 minutes. It might skip on the 60th hour since the release of a new image doesn't seem exactly on time. No guarantees whatsoever, it is definitely ugly/trash code, but it gets the job done. I'm not a dev.
