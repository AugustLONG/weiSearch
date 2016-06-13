import os

def stop():
    os.system("ps axu | grep main.py | grep -v grep | awk '{print $2;}'|xargs kill ")
    os.system("ps axu | grep scrapy | grep -v grep | awk '{print $2;}'|xargs kill -9")
    print 'yes'


if __name__ == "__main__":
    stop()
