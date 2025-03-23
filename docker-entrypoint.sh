#!/bin/bash

# Kalau ENV variable RUN_OPTION ada isinya, jalankan main.py dengan option tersebut
# Kalau tidak ada, default ke option 4 (Exit)
if [ -n "$RUN_OPTION" ]; then
    echo "$RUN_OPTION" | python main.py
else
    echo "4" | python main.py
fi