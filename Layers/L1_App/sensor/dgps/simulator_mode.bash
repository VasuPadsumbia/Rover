#!/bin/bash

echo " "
echo "Setting GPS to simulator mode ..."


python3 /home/outdoor/piksi_tools/piksi_tools/settings.py -t -p 195.37.48.193:55555 read_to_file settings_file/settings.ini
#python3 /home/outdoor/piksi_tools/piksi_tools/settings.py -t -p 195.37.48.193:55555 write_from_file settings_file/settings.ini

echo " "
    echo "Task finished."
