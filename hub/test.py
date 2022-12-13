import os
import time

while True:
    print (os.stat("hub/data.txt").st_size)
    time.sleep(2)