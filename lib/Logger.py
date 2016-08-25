# -*- coding: utf-8 -*-

import sys
import os

def d(msg):
    print "DEBUG: " + msg

def i(msg):
    print "INFO: " + msg

def e(msg):
    print "ERROR: " + msg

def f(msg):
    print "FATAL: " + msg

def d(tag, msg):
    print "DEBUG: " + tag + " " + msg

def w(tag, msg):
    print "WARNING: " + tag + " " + msg

def i(tag, msg):
    print "INFO: " + tag + " " + msg

def e(tag, msg):
    print "ERROR: " + tag + " " + msg

def f(tag, msg):
    print "FATAL: " + tag + " " + msg

def df(tag, array):
    msg = ''
    for item in array:
	msg += "," + str(item)
    msg = '[' + msg[1:] + ']'

    print "DEBUG: " + tag + " " + msg
