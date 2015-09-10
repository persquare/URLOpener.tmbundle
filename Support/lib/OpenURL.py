#!/usr/bin/env python -S

"""Open a link (or Markdown style reference link) in TextMate's companion window."""

import os
import sys
import re
from urlparse import urlparse

envvars = ['TM_BUNDLE_SUPPORT', 'TM_SUPPORT_PATH']
sys.path[:0] = [os.environ[v]+'/lib' for v in envvars if os.environ[v] not in sys.path]


# MATCH_URL = r'.*?((?:https?://|file://|mailto:|message://)\S+)'
MATCH_URL = r'([a-z0-9_-]+):(?://)?([^\s\>\)]+)'
MATCH_REF_URL = r'.*?\[.+?\]\[(.+?)\]'
MATCH_REF_TEMPLATE = r'^.*?\[%s\]:\s*(.+)'
MATCH_SCHEME = r'(.+?):'

def expand_reference(ref):
    MATCH_REF = MATCH_REF_TEMPLATE % (ref,)
    with open(os.environ.get('TM_FILEPATH'), 'r') as f:
        for line in f:
            line = line.rstrip()
            match = re.match(MATCH_REF, line)
            if match:
                return match.group(1)
    return None
            
def scan_line(line):
    """Scan line for URL or reference, return URL or None)"""
    URL = None
    type = None
    # Check for direct URL first
    match = re.search(MATCH_URL, line)
    if match:
        return match.group(0)
    # Check for reference URL    
    match = re.match(MATCH_REF_URL, line)
    if not match:
        return None
    # So, it's a reference, scan doc for corresponding URL
    return expand_reference(match.group(1))
            
def split_url(url):
    match = re.match(MATCH_URL, url)
    return (match.group(1), match.group(2)) 

def open_in_default_app(url):
    os.system("open %s" % (url))

def open_in_editor(path):
    os.system("open txmt://open?url=file://%s" % (path))
     
def open_in_htmlview(url):
   print """
    <!DOCTYPE HTML>
    <html lang="en-US">
        <head>
            <meta charset="UTF-8">
            <script type="text/javascript">
                window.location.href = "%s"
            </script>
        </head>
        <body>
        </body>
    </html>
    """ % (url)

