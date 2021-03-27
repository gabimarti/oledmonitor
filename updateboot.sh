#!/bin/sh
# Setting displayd.sh to load at init

cp "displayd.sh" "/etc/init.d/display_daemon"
chmod +x /etc/init.d/display_daemon
chown root /etc/init.d/display_daemon
chgrp root /etc/init.d/display_daemon
sudo update-rc.d display_daemon defaults
#sudo reboot


