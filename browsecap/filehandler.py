import ConfigParser
import io
import logging
import os

from urllib2 import Request, urlopen

from django.conf import settings
from django.core.mail import send_mail

from browsecap.settings import *


logger = logging.getLogger(__name__)

class BrowseCapImport(object):
    ''' 
        This class wil import the latest version of the BrowseCap ini to the filesystem.
        It\'s called from within our management command, but could easily be ported into for eg. browser.py
    '''
        
    def __init__(self):
        self.errors = []
        self.process()


    def process(self):
        if self.retrieve_file() and self.validate_ini():
            result = self.save_local()
        else:
            result = False
        self.send_notify(result)


    def retrieve_file(self):
        ''' Retrieve the content from the BrowseCap ini resource at Gary Keith '''
        req = Request(BROWSECAP_URL)
        
        try:
            response = urlopen(req)
        except IOError, e:
            if hasattr(e, 'reason'):
                self.process_error('We failed to reach a server. Reason: %s ' % e.reason)
            elif hasattr(e, 'code'):
                self.process_error('The server couldn\'t fulfill the request. Error code: %d' % e.code)
            return False
        else:
            self.data = response.read()
            return True


    def validate_ini(self):
        ''' Validate the retrieved INI file if it really is considered a config file '''
        config = ConfigParser.RawConfigParser()
        try:
            config.readfp(io.BytesIO(self.data))
        except ConfigParser.ParsingError, e:
            self.process_error('The Ini file we tried to retrieve has an error. Reason: %s' % e.message)
            return False            
        return True


    def save_local(self):
        ''' When the URL is retrieved and the INI is considered valid, place the file on the filesystem '''
        try:
            fsock = open('%s/browscap.ini' % BROWSECAP_INI_PATH, "w")
            try:                 
                fsock.write(self.data)
            finally:
                fsock.close()              
                return True
        except IOError, e:
            self.process_error('Could not save Browsecap error. Reason: %s' % e)        
        return False
    
    
    def process_error(self, message):
        ''' Made a central function to register errors '''
        self.errors.append(message)
        logger.error(message)
    

    def send_notify(self, result=False):
        ''' 
            Send out a notification email to the ADMINS when they want a notify in case of errors 
        '''
        if BROWSECAP_NOTIFY and not result:
            subject = "%s BrowseCap import " % settings.EMAIL_SUBJECT_PREFIX
            message = "An error occured while importing and validating the latest BrowseCap INI file: \n"
            for error in self.errors:
                message+= "\t%s" % error
                
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, dict(settings.ADMINS).values(), fail_silently=True)