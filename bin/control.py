#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import subprocess
import os
import sys
import time

#获取当前路径
HOME = os.getcwd()
#创建文件夹
isExists=os.path.exists(HOME+'/../log')
if not isExists:
    os.makedirs(HOME+'/../log')

SCRPET = os.path.basename(sys.argv[0])
if len(sys.argv) != 3 or sys.argv[1] == '-h':
    sys.exit("Usage: %s ServerName {start, stop, restart}" % SCRPET)

RUN = "python"
NAME = sys.argv[1]
DirName = '../'+NAME
OP = sys.argv[2]
NAME_NOPOSTFIX = NAME.split(".")[0]

#PID文档和LOG文档
PIDFILE = "%s/%s.pid" % (HOME+'/../log',NAME_NOPOSTFIX)
LOGFILE = "%s/%s_ctrl.log" % (HOME+'/../log',NAME_NOPOSTFIX)

def start():
    print " | ".join([HOME, NAME])
    print "Starting", NAME, "..."
    # if os.path.exists(PIDFILE):
    #     print "%s has been running | PID:%s" % (NAME, open(PIDFILE).readline()), "Continue?(Y/N)"
    #     k = raw_input()
    #     if not k in ("Y", "y"):
    #         sys.exit(1)
    try:
        p = subprocess.Popen([RUN, DirName], stderr=subprocess.PIPE)
        # 生成pidfile
        pid = p.pid
        open(PIDFILE, "w").write("%s" % pid)
        print " | ".join(["Start OK", "PID:%s" % pid])
        # 输出定向到日志
        out = p.stderr.read()
        open(LOGFILE, "a").write(out)
    except Exception as e:
        print e

def stop():
    pid = open(PIDFILE).readline()
    print pid

    print "Stopping", NAME, '...'
    if pid:
        if subprocess.call(["kill " + pid], shell=True) == 0:
            print " | ".join(["Stop OK", "PID:%s" % pid])
            if subprocess.call(["rm " + PIDFILE], shell=True) != 0:
                print "Delete Permission Denied"
    else:
        print "Stop Error"


def restart():
    stop()
    time.sleep(1)
    start()

ops = {"start":start,"stop":stop,"restart":restart}

if __name__ == "__main__":
    ops[OP]()
