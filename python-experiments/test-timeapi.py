# -- written by Anjul Patney -- #
# -- replacement for timeapi in python -- #

import csv, math, sys, os, datetime, glob, re, array
import matplotlib.pyplot as plt
from subprocess import call
import math
import datetime
import string
# import ntplib
from time import ctime


numbers = [ "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
"nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
"eighteen", "nineteen" "twenty", "twenty one", "twenty two", "twenty three", "twenty four",
"twenty five", "twenty six", "twenty seven", "twenty eight", "twenty nine", "thirty", 
"thirty one", "thirty two", "thirty three", "four thirty", "thirty five", "thirty six",
"thirty seven", "thirty eight", "thirty nine", "forty", "forty one", "forty two", "forty three",
"forty four", "forty five", "forty six", "forty seven", "forty eight", "forty nine", "fifty",
"fifty one", "fifty two", "three fifty", "four fifty", "fifty five", "fifty six", "fifty seven",
"fifty eight", "fifty nine", "sixty" ]

inputs = [ 
  "make coffee in 30 seconds",
  "get inside in 80 minutes",
  "cut grass in 7 hours",
  "play soccer in 2 days",
  "do work in 1 week",
  "come back in 12 months",
  "do other stuff in 1 year",
  "put water in pot in 2 weeks",
]


for remstr in inputs:
  splitlist = string.split(remstr, " in ")
  remmsg = " in ".join(splitlist[:-1])
  timestr = splitlist[-1]
  print "%s =>\n\t[%s]\n\t%s\n" % (remstr, remmsg, timestr)


# c = ntplib.NTPClient()
# response = c.request('pool.ntp.org')
# print ctime(response.tx_time)


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
