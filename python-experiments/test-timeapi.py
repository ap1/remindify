# -- written by Anjul Patney -- #
# -- replacement for timeapi in python -- #

import datetime
import string
from datetime import timedelta
from dateutil.relativedelta import *
from dateutil import parser

inputs = [ 
  "make coffee in 30 seconds",
  "get inside in 86   minutes ",
  "cut grass in 7 hours   ",
  "play soccer in 2 days",
  "do  work in   1 week  ",
  "come back in 17 months",
  "do other stuff http://idav.ucdavis.edu/~anjul/ in 1 year",
  "put water in  in in in pot in   2   weeks",
  "in in in in in 10 minutes"
]

def compute_delta_seconds(how_many):
  datetime_now = datetime.datetime.utcnow()
  return datetime_now + relativedelta(seconds = how_many)

def compute_delta_minutes(how_many):
  datetime_now = datetime.datetime.utcnow()
  return datetime_now + relativedelta(minutes = how_many)

def compute_delta_hours(how_many):
  datetime_now = datetime.datetime.utcnow()
  return datetime_now + relativedelta(hours = how_many)

def compute_delta_days(how_many):
  datetime_now = datetime.datetime.utcnow()
  return datetime_now + relativedelta(days = how_many)

def compute_delta_weeks(how_many):
  datetime_now = datetime.datetime.utcnow()
  return datetime_now + relativedelta(weeks = how_many)

def compute_delta_months(how_many):
  datetime_now = datetime.datetime.utcnow()
  return datetime_now + relativedelta(months = how_many)

def compute_delta_years(how_many):
  datetime_now = datetime.datetime.utcnow()
  return datetime_now + relativedelta(years = how_many)

time_units = {
  "second"  : compute_delta_seconds,
  "seconds" : compute_delta_seconds,

  "minute"  : compute_delta_minutes,
  "minutes" : compute_delta_minutes,

  "hour"    : compute_delta_hours,
  "hours"   : compute_delta_hours,

  "day"     : compute_delta_days,
  "days"    : compute_delta_days,

  "week"    : compute_delta_weeks,
  "weeks"   : compute_delta_weeks,

  "month"   : compute_delta_months,
  "months"  : compute_delta_months,

  "year"    : compute_delta_years,
  "years"   : compute_delta_years,
}

#print datetime_now

# def parse_delta_time(tz, delta_str):
#   try:
#     delta_str  = delta_str.strip()
#     delta_list = delta_str.split()

#     delta_val  = int(delta_list[0].strip())
#     delta_unit = delta_list[1].strip()

#     computed_datetime = time_units[delta_unit](delta_val)

#     return computed_datetime
#   except Exception, e:


for remstr in inputs:
  splitlist = remstr.split(" in ")


  #print "(%s) (%s)" %(remstr[:in_pos], remstr[(in_pos+4):])

  in_pos = remstr.rfind(" in ")
  remmsg = remstr[:in_pos]
  delta_str = remstr[(in_pos+4):]

  # remmsg = " in ".join(splitlist[:-1])
  # delta_str = splitlist[-1].strip()
  print "%s =>\n\t[%s]\n\t%s" % (remstr, remmsg, delta_str)

  delta_str = delta_str.strip()

  delta_list = delta_str.split()

  delta_val = int(delta_list[0].strip())
  delta_unit = delta_list[1].strip()

  print "\tfetching [%d], [%s]" % (delta_val, delta_unit)
  print "\t", datetime.datetime.utcnow()
  dt = time_units[delta_unit](delta_val)
  print "\t", dt
  # parse("2003 10:36:28 BRST 25 Sep Thu", tzinfos=TZOFFSETS)
  print "\t", dt.strftime("%B %d, %Y, %I:%M:%S %p UTC")
  print "\t", parser.parse(dt.strftime("%B %d, %Y, %I:%M:%S %p UTC"))
  print ""

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
