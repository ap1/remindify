from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import mail
from dateutil.tz import gettz, tzutc
from datetime import datetime
from datetime import timedelta
from timezones import TimeZone
import urllib
from dateutil import parser
import logging
from encode import *
import os
import time

def parse_time(tz, text):
    # TODO: modify to parse send-date as well for relative time expressions
    max_tries = 3
    for _try in range(max_tries):
        try:
            #response = urlfetch.fetch('http://www.timeapi.org/%s/%s' % (tz.lower(), urllib.quote(text)))
            response = urlfetch.fetch('http://chronic.herokuapp.com/%s/%s' % (tz.lower(), urllib.quote(text)))
            if response.status_code == 200:
                return response.content
            elif response.status_code == 500:
                logging.info( 'TimeAPI returned 500 on "%s"' % text )
        except Exception(e):
            logging.info( 'TimeAPI fetch failed with "%s"' % str(e) )
    

def format_datetime( dt, tz ):
    date_format = '%A, %B %d, %Y at %I:%M %p (%Z)'
    return dt.replace(tzinfo=tzutc()).astimezone( TimeZone[ tz ] ).strftime( date_format )

def send_agenda( msg, tz, user ):
    try:
        account = Account.all().filter('user =', user).fetch(2)[0]
        msgbody = "All your unfired reminders:\n\n"
        reminders = Reminder.all().filter('user = ', user)
        reminders = [r for r in reminders if not r.fired]
        for (idx,reminder) in enumerate(reminders):
            created = format_datetime( reminder.created, account.tz )
            scheduled = format_datetime( reminder.scheduled, account.tz )
            msgbody = msgbody + "\t%d. \"%s\"\n\tcreated: %s\n\tscheduled: %s\n\n" % ( (idx+1), reminder.text, created, scheduled )
        mail.send_mail( sender=from_field('p'), to=msg.sender,
                        subject='Re: '+ msg.subject,
                        body=msgbody)
        logging.info ( 'Sent agenda for request "%s"' % msg.subject )        
    except:
        logging.error( 'Failed to send agenda for request "%s"' % msg.subject )
    
def send_agenda_today( msg, tz, user ):
    try:
        account = Account.all().filter('user =', user).fetch(2)[0]
        msgbody = "Next 24 hours:\n\n"
        reminders = Reminder.all().filter('user = ', user)
        reminders = [r for r in reminders if not r.fired and r.scheduled <= (datetime.now() + timedelta(hours=24))]
        for (idx,reminder) in enumerate(reminders):
            created = format_datetime( reminder.created, account.tz )
            scheduled = format_datetime( reminder.scheduled, account.tz )
            msgbody = msgbody + "\t%d. \"%s\"\n\tcreated: %s\n\tscheduled: %s\n\n" % ( (idx+1), reminder.text, created, scheduled )
        mail.send_mail( sender=from_field('p'), to=msg.sender,
                        subject='Re: '+ msg.subject,
                        body=msgbody)
        logging.info ( 'Sent agenda for request "%s"' % msg.subject )        
    except:
        logging.error( 'Failed to send agenda for request "%s"' % msg.subject )

def create_reminder( s, tz, user ):
    try:
        reminder = Reminder( parse=s, timezone=tz, user=user )
        reminder.put()
        return reminder
    except:
        logging.error( 'Failed to create Reminder for request "%s"' % s )

class Reminder(db.Model):
    # TODO: replace user with account reference, to avoid needless queries
    user = db.UserProperty(required=True)
    raw = db.StringProperty(required=True)
    text = db.StringProperty()
    scheduled_raw = db.StringProperty()
    scheduled = db.DateTimeProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    fired = db.BooleanProperty(default=False)
    #TODO: recurrence
    
    def __init__(self, *args, **kwargs):
        if 'parse' in kwargs:
            kwargs['text'], kwargs['scheduled_raw'] = self.parse(kwargs['parse'], kwargs['timezone'])
            kwargs['scheduled'] = parser.parse(kwargs['scheduled_raw'])
            kwargs['raw'] = kwargs['parse']
        super(Reminder, self).__init__(*args, **kwargs)
    
    def scheduled_local(self):
        return parser.parse(self.scheduled_raw)
    
    def parse(self, raw, timezone):
        ats = raw.split(' at ')
        if len(ats) == 2:
            return (ats[0], parse_time(timezone, 'at %s' % ats[1]))
        ins = raw.split(' in ')
        if len(ins) == 2:
            return (ins[0], parse_time(timezone, 'in %s' % ins[1]))
        return raw, None
    
    def parse_and_update(self, raw, timezone):
        self.scheduled_raw = parse_time(timezone, raw)
        logging.info( 'parse_and_update returned raw: ' + str(self.scheduled_raw) )
        self.scheduled = self.scheduled_local()
        self.fired = False
    

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
    
