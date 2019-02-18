import datetime
from time import sleep
import sys

def get_time():
    sleep(1)
    return datetime.datetime.now()

while True:
    print('\r%s'%get_time(), end = " ")
    sys.stdout.flush()
