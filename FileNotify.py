# -*- coding:utf-8 -*-                                                                                                                                                                        
import os
import sys
import pyinotify
from functions import *
from lib import S3ImgUploader

WATCH_PATH = '/dianyi/app/offer_miner_new/offer_miner_new/icons/' #监控目录

if not WATCH_PATH:
    print ('Error',"The WATCH_PATH setting MUST be set.")
    sys.exit()
else:
    if os.path.exists(WATCH_PATH):
        print ('Watch status','Found watch path: path=%s.' % (WATCH_PATH))
    else:
        print ('Error','The watch path NOT exists, watching stop now: path=%s.' % (WATCH_PATH))
        sys.exit()

class OnIOHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
    	filepath = os.path.join(event.path,event.name)
        print ('Action',"create file: %s " % filepath)

        S3ImgUploader.uploadIconImg(filepath)

def auto_compile(path = '.'):
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_MODIFY
    notifier = pyinotify.Notifier(wm)
    wm.add_watch(path, mask,rec = True,auto_add = True)
    print ('Start Watch','Start monitoring %s' % path)
    try:
        notifier.loop(daemonize=True, callback=OnIOHandler,pid_file='/tmp/pyinotify2.pid', stdout='/tmp/pyinotify2.log')
    except pyinotify.NotifierError, err:
        print >> sys.stderr, err

if __name__ == "__main__":
     auto_compile(WATCH_PATH)