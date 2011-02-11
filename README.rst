Django browsecap
================

Browsecap is a simple library for django for detecting browser type.

The main interface consists of two function in `browsecap.browser`:

    `is_mobile`: returns True if the given user agent is a known mobile browser

    `is_rich_mobile`: returns True if the given user agent is a known "rich" mobile browser, see bellow

    `is_crawler`: returns True if the given user agent is a known crawler

MobileRedirectMiddleware
------------------------

For your convenience there is also a middleware that automatically redirects
all mobile users to alternate domain.

To use just add `browsecap.middleware.MobileRedirectMiddleware` to your
`settings.MIDDLEWARE_CLASSES` and define a `MOBILE_DOMAIN` that you want your
mobile users redirected to. Note that the value must contain full path
including the protocol (http://)

The middleware sets ismobile cookie to value 1 and can be overriden by deleting
that cookie setting isbrowser cookie to 1.

Internals
---------

Browsecap works by parsing the browscap.ini file and storing a list of browsers
as regexps in memory. Each user agent to be checked is then matched against the
set of regexps until we run out (False) or a match is found (True). The result
is stored in a dictionary to speedup further processing of the same user agent
(in our experience, 200k users only have around 8k distinct user agents, so
caching works).

Performance of the matchig is adequate and shouldn't slow down the request
processing even if used every time (middleware), the only thing that is
somewhat slow (under a second on a laptop) is parsing the browscap.ini file.
This is done only when the module is first loaded and stores it's results in
cache so that start of the next thread/process should not be hindered.

"Rich" mobile phones
--------------------

If you need to identify modern mobile browsers with rich capabilities, you
could use `is_rich_mobile` function.

This function by default put device into "rich" group, if it have set
"Platform" property inside `browsercap.ini` file to "Android" or "iPhone OSX"
value. This behaviour should be overriden by `RICH_MOBILE_BROWSER_FN` in your
`settings.py` file.  It should be set to callable function, which accept one
`conf` argument and return `True` (device is rich) or `False` (device isn't
rich). For example:

    def my_rich_fn(conf):
        javascript = conf.get('javascript', 'false')
        supportscss = conf.get('supportscss', 'false')
        return javascript == 'true' and supportscss == 'true'

    RICH_MOBILE_BROWSER_FN = my_rich_fn

Credits
-------
It is based on henning's snippet #267 -
http://www.djangosnippets.org/snippets/267/

Thank you very much for the great work!
