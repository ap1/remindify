from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import mail
from dateutil.tz import gettz, tzutc
from datetime import datetime
from datetime import timedelta
from timezones import TimeZone
import urllib
#from dateutil import parser
import logging
from encode import *
import os
import time
import string
from dateutil.relativedelta import *

def compute_delta_seconds(how_many):
  datetime_now = datetime.utcnow()
  return datetime_now + relativedelta(seconds = how_many)

def compute_delta_minutes(how_many):
  datetime_now = datetime.utcnow()
  return datetime_now + relativedelta(minutes = how_many)

def compute_delta_hours(how_many):
  datetime_now = datetime.utcnow()
  return datetime_now + relativedelta(hours = how_many)

def compute_delta_days(how_many):
  datetime_now = datetime.utcnow()
  return datetime_now + relativedelta(days = how_many)

def compute_delta_weeks(how_many):
  datetime_now = datetime.utcnow()
  return datetime_now + relativedelta(weeks = how_many)

def compute_delta_months(how_many):
  datetime_now = datetime.utcnow()
  return datetime_now + relativedelta(months = how_many)

def compute_delta_years(how_many):
  datetime_now = datetime.utcnow()
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


# def parse_time(tz, text):
#     # TODO: modify to parse send-date as well for relative time expressions
#     max_tries = 5
#     for _try in range(max_tries):
#         try:
#             response = urlfetch.fetch('http://www.timeapi.org/%s/%s' % (tz.lower(), urllib.quote(text)))
#             #response = urlfetch.fetch('http://chronic.herokuapp.com/%s/%s' % (tz.lower(), urllib.quote(text)))
#             if response.status_code == 200:
#                 return response.content
#             elif response.status_code == 500:
#                 logging.info( 'TimeAPI returned 500 on "%s"' % text )
#         except Exception, e:
#           logging.info( 'TimeAPI try %d: fetch failed with "%s"' % (_try, str(e)) )
    

def parse_delta_time(tz, delta_str):
  try:
    delta_str  = delta_str.strip()
    delta_list = delta_str.split()

    delta_val  = int(delta_list[0].strip())
    delta_unit = delta_list[1].strip()

    computed_datetime = time_units[delta_unit](delta_val)

    return computed_datetime
  except Exception, e:
    logging.info( 'Error: "%s"' % (str(e)) )

def format_datetime( dt, tz ):
    date_format = '%A, %B %d, %Y at %I:%M %p (%Z)'
    return dt.replace(tzinfo=tzutc()).astimezone( TimeZone[ tz ] ).strftime( date_format )

def send_agenda( msg, tz, user ):
    try:
        account = Account.all().filter('user =', user).fetch(2)[0]
        msgbody = "All your unfired reminders:\n\n"
        reminders = Reminder.all().filter('user = ', user)
        reminders = [r for r in reminders if not r.fired]
        reminders = sorted(reminders, key = lambda rem: rem.scheduled)
        for (idx,reminder) in enumerate(reminders):
            created = format_datetime( reminder.created, account.tz )
            scheduled = format_datetime( reminder.scheduled, account.tz )
            #msgbody = msgbody + "\t%d. \"%s\"\n\tcreated: %s\n\tscheduled: %s\n\n" % ( (idx+1), reminder.text, created, scheduled )
            #msgbody = msgbody + "\t%d. \"%s\" due %s\n" % ( (idx+1), reminder.text, scheduled )
            msgbody = msgbody + "\t%d. %s: \"%s\"\n" % ( (idx+1), scheduled, reminder.text )
        mail.send_mail( sender=from_field('p'), to=msg.sender,
                        subject='Re: '+ msg.subject,
                        body=msgbody)
        logging.info ( 'Sent agenda for request "%s" - system time %s' % (msg.subject, datetime.now()))
    except:
        logging.error( 'Failed to send agenda for request "%s"' % msg.subject )
    
def send_agenda_today( msg, tz, user ):
    try:
        account = Account.all().filter('user =', user).fetch(2)[0]
        msgbody = "Next 24 hours:\n\n"
        reminders = Reminder.all().filter('user = ', user)
        reminders = [r for r in reminders if not r.fired and r.scheduled <= (datetime.now() + timedelta(hours=24))]
        reminders = sorted(reminders, key = lambda rem: rem.scheduled)
        for (idx,reminder) in enumerate(reminders):
            created = format_datetime( reminder.created, account.tz )
            scheduled = format_datetime( reminder.scheduled, account.tz )
            #msgbody = msgbody + "\t%d. \"%s\"\n\tcreated: %s\n\tscheduled: %s\n\n" % ( (idx+1), reminder.text, created, scheduled )
            #msgbody = msgbody + "\t%d. \"%s\" due %s\n" % ( (idx+1), reminder.text, scheduled )
            msgbody = msgbody + "\t%d. %s: \"%s\"\n" % ( (idx+1), scheduled, reminder.text )
        mail.send_mail( sender=from_field('p'), to=msg.sender,
                        subject='Re: '+ msg.subject,
                        body=msgbody)
        logging.info ( 'Sent agenda for request "%s" - system time %s' % (msg.subject, datetime.now()))
    except:
        logging.error( 'Failed to send agenda for request "%s"' % msg.subject )

def create_reminder( s, tz, user ):
    try:
        reminder = Reminder( parse=s, timezone=tz, user=user )
        reminder.put()
        return reminder
    except Exception, e:
        logging.error( 'Failed to create Reminder for request "%s": %s' % (s, str(e)) )

class Reminder(db.Model):
    # TODO: replace user with account reference, to avoid needless queries
    user            = db.UserProperty(required=True)
    raw             = db.StringProperty(required=True)
    text            = db.StringProperty()
    scheduled_raw   = db.StringProperty()
    scheduled       = db.DateTimeProperty()
    created         = db.DateTimeProperty(auto_now_add=True)
    updated         = db.DateTimeProperty(auto_now=True)
    fired           = db.BooleanProperty(default=False)
    #TODO: recurrence
    
    def __init__(self, *args, **kwargs):
        if 'parse' in kwargs:
            kwargs['text'], kwargs['scheduled_raw'], kwargs['scheduled'] = self.parse(kwargs['parse'], kwargs['timezone'])
            #kwargs['scheduled'] = parser.parse(kwargs['scheduled_raw'])
            kwargs['raw'] = kwargs['parse']
        super(Reminder, self).__init__(*args, **kwargs)
    
    def parse(self, raw, timezone):
        in_pos = raw.strip().rfind(" in ")
        if in_pos >= 0:
            remmsg = raw[:in_pos]
            delta_str = raw[(in_pos+4):]
            parsed_datetime = parse_delta_time(timezone, delta_str)
            parsed_raw = format_datetime(parsed_datetime, timezone)
            return (remmsg, parsed_raw, parsed_datetime)
        else:
            logging.error("Cannot find *in* in your reminder!\n")
            raise Exception("Cannot find *in* in your reminder!\n")
            return raw, None, None
    
    def parse_and_update(self, raw, timezone):
        in_pos = raw.strip().find("in ")
        if in_pos >= 0:
            remmsg = raw[:in_pos]
            delta_str = raw[(in_pos+3):]
            self.scheduled = parse_delta_time(timezone, delta_str)
            self.scheduled_raw = format_datetime(self.scheduled, timezone)
            logging.info( 'parse_and_update returned raw: ' + str(self.scheduled_raw) )
            self.fired = False
        else:
            logging.error("Cannot find *in* in your reminder!\n")
            raise Exception("Cannot find *in* in your reminder!\n")
            return raw, None, None
    

def account_for_sender( sender ):
    if '<' in sender:
        sender = sender.split('<')[-1].split('>')[0]
    accts = Account.gql( "WHERE emails = :sender", sender=sender ).fetch(2)
    if not accts:
        return None
    if len( accts ) > 1:
        logging.error( 'Matched multiple accounts for sender %s---this should not happen' % sender )
        return None
    return accts[ 0 ]

class Account(db.Model):
    user = db.UserProperty(required=True)
    emails = db.StringListProperty( )
    tz = db.StringProperty(default='PDT')
    
    timezones = [ 'PST', 'PDT', 'MST', 'MDT', 'CST', 'CDT', 'EST', 'EDT' ]
    
    def __init__(self, *args, **kwargs):
        if 'emails' not in kwargs:
            kwargs['emails'] = []
        if kwargs['user'].email() not in kwargs['emails']:
            kwargs['emails'].append( kwargs['user'].email() )
        
        super(Account, self).__init__(*args, **kwargs)
    
