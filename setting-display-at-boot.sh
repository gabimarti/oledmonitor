#!/bin/sh
#
# This script configures the display script to start automatically at each start of the system.
#
# It must be executed with root permissions.

# Save the previous version of rc.local
cp /etc/rc.local /etc/rc.local.prev

# Add command to set script to start automatically at startup
grep -iv "exit 0" /etc/rc.local > /etc/rc.local.tmp
cp -f /etc/rc.local.tmp /etc/rc.local
rm -f /etc/rc.local.tmp
echo "python3 $HOME/stats.py &" >> /etc/rc.local
echo "exit 0" >> /etc/rc.local


