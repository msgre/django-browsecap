import time
import re

from django.http import HttpResponseRedirect, HttpResponse
from django.utils.http import cookie_date
from django.conf import settings

from browsecap.browser import is_mobile

# default cookie expire time is one month
DEFAULT_COOKIE_MAX_AGE = 3600*24*31

class MobileRedirectMiddleware(object):
    def process_request(self, request):
        if not getattr(settings, 'MOBILE_DOMAIN', False):
            return 
        
        # Cookie settings
        max_age = getattr(settings, 'MOBILE_COOKIE_MAX_AGE', DEFAULT_COOKIE_MAX_AGE)
        expires_time = time.time() + max_age
        expires = cookie_date(expires_time)

        # test for browser return
        if (
                # is mobile?
                is_mobile(request.META.get('HTTP_USER_AGENT', None)) 
                    and 
                # but has param m2w?
                request.GET.get('m2w', False) 
                    and 
                # does currently not have a is browser cookie with 1
                request.COOKIES.get('isbrowser', '0') == '0'
        ):
            ''' Set a cookie for Mobile 2 Web if a mobile browser does not want to browse mobile '''
            response = HttpResponseRedirect(request.META.get('PATH_INFO', '/'))
            response.set_cookie('ismobile', '0', domain=settings.SESSION_COOKIE_DOMAIN, max_age=max_age, expires=expires)
            response.set_cookie('isbrowser', '1', domain=settings.SESSION_COOKIE_DOMAIN, max_age=max_age, expires=expires)
            return response
        
        # test for mobile browser
        if (
                # check for override cookie, do not check if present
                request.COOKIES.get('ismobile', '0') == '1' or (
                    # browser info present
                    'HTTP_USER_AGENT' in request.META
                    and 
                    # desktop browser override not set
                    request.COOKIES.get('isbrowser', '0') != '1' 
                    and 
                    # check browser type
                    is_mobile(request.META.get('HTTP_USER_AGENT', None))
                    and
                    # check whether ipad should be redirected
                    self.redirect_ipad(request.META.get('HTTP_USER_AGENT', None))
                )
            ):
            redirect = settings.MOBILE_DOMAIN
            if getattr(settings, 'MOBILE_REDIRECT_PRESERVE_URL', False):
                redirect = redirect.rstrip('/') + request.path_info
            
            # redirect to mobile domain
            response = HttpResponseRedirect(redirect)
            response.set_cookie('ismobile', '1', domain=settings.SESSION_COOKIE_DOMAIN, max_age=max_age, expires=expires)
            return response


    def redirect_ipad(self, user_agent):
        if not getattr(settings, 'BROWSECAP_REDIRECT_IPAD'):
            match = re.search('iPad', user_agent, re.I)
            if match:
                return False
        return True