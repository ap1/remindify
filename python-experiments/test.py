import csv, math, sys, os, datetime, glob, re, array
import matplotlib.pyplot as plt
from subprocess import call
import re
import math


ats = "hello mr abc"
bts = [ ats ]


def get_word(text):
    words = text.split()
    characters = -1
    for word in words:
        characters += len(word)
        if characters >= 0:
            return word

for  at in bts:
    print get_word(at)
    if get_word(at)=="mello":
        print "hey"
    try:
      print 7/0
    except Exception as exc:
      print '[E] %s' % exc

    print 'done'
