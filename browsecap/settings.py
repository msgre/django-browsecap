import os

from django.conf import settings


BROWSECAP_CACHE_KEY = getattr(settings, 'BROWSECAP_CACHE_KEY', 'browsecap')
BROWSECAP_CACHE_TIMEOUT = getattr(settings, 'BROWSECAP_CACHE_TIMEOUT', 60*60*2) # 2 hours

BROWSECAP_URL = getattr(settings, 'BROWSECAP_URL', 'http://browsers.garykeith.com/stream.asp?BrowsCapINI')
BROWSECAP_INI_PATH = getattr(settings, 'BROWSECAP_INI_PATH', os.path.abspath(os.path.dirname(__file__ or os.getcwd())) )
BROWSECAP_NOTIFY = getattr(settings, 'BROWSECAP_NOTIFY',  False)