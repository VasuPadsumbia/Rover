#!/bin/bash

echo " "
echo "Setting GPS to simulator mode ..."
<<<<<<< HEAD
python3 setup_piksi.py -f settings_file/settings.ini
=======
python3 /home/outdoor/piksi_tools/piksi_tools/settings.py -t -p 195.37.48.193:55555 write_from_file settings_file/settings.ini
>>>>>>> b1272f9ad00038afafac271744630b3d1b37f9a9
echo " "
    echo "Task finished."
