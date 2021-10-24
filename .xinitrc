#!/bin/sh
xrdb -merge ~/.Xresources

xset +fp /usr/local/share/fonts
xset +fp $HOME/lib/fonts
setxkbmap -option ctrl:nocaps
xset r rate 200 40
xset s off -dpms

# start default applications
# some of these are started in `.config/qtile/config.py`
# firefox &
# emacs &
compton &
dropbox start &

/home/nitta/bin/disphome

# desktop background
feh --bg-scale ~/Dropbox/home/lib/photos/wallpaper/debian10-wallpaper.png

# start window manager
/home/nitta/.local/bin/qtile start
