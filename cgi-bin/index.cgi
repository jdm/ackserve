#!/usr/bin/env python

# enable debugging
import cgitb
import cgi
import urllib2
from StringIO import StringIO
import gzip
import ConfigParser
import base64
import urllib
import logging
import os
import sys
import subprocess
import itertools
cgitb.enable()

print "Content-Type: text/html;charset=utf-8"
print

form = cgi.FieldStorage()
#sys.stderr.write(str(form.keys()) + '\n')
path = urllib2.unquote(form.getfirst('path', ''))
search = urllib2.unquote(form.getfirst('search', ''))

print '<!DOCTYPE html>'
print '<html>'
print '<title>ack-web</title>'
print '<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/highlight.js/9.1.0/styles/default.min.css">'
print '<script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/9.1.0/highlight.min.js"></script>'
print '<script>hljs.initHighlightingOnLoad()</script>'
print '<style>.hljs { background: none; display: inline; }</style>'
print '<style>pre.codez { display: inline } .highlight { background-color: #EEEEBB }</style>'
print '<body>'
print '<form name="foo" method="get">'
print '<h4>Find <input name="search" value="%s"> in <input name="path" value="%s" size=30> <input type=submit></h4>' % (search, path)
print '</form>'

if search:
    try:
        output = subprocess.check_output(['ack', search, path, '--nocolor'])
    except subprocess.CalledProcessError:
        print 'No results.'
        sys.exit(0)
    lines = output.split('\n')
    files = itertools.groupby(lines, lambda line: line.split(':')[0])
    for (file, group) in files:
        print '<div><a href="?path=%s">%s</a><br>' % (file, file)
        for line in group:
            if not line:
                continue
            #sys.stderr.write(line + '\n')
            (filename, lineno, contents) = line.split(':', 2)
            contents = cgi.escape(contents)
            begin = contents.find(search)
            end = begin + len(search)
            pre = contents[:contents.find(search)]
            actual = contents[begin:end]
            post = contents[end:]
            print '''<a href="?path=%s#%s">line %s</a> -- <pre class="codez">%s</pre><pre class="codez highlight">%s</pre><pre class="codez">%s</pre>''' % (file, lineno, lineno, pre, actual, post)
            #print '</code></pre><br>'
            print '<br>'
        print '</div><br>'
elif os.path.isdir(path):
    if path[-1] != '/':
        path += '/'

    print '<table>'

    dirs = ['..'] + list(os.listdir(path))
    for file in dirs:
        print '<tr>'
        print '<td>'
        filepath = os.path.normpath(path + file)
        if os.path.isdir(filepath):
            print '<a href="?path=' + filepath + '"><img src="../gnome_fs_directory.png" width=20px></a>'
        print '</td><td>'
        print '<a href="?path=' + filepath + '">' + file + '</a>'
        print '</td></tr>'
else:
    with open(path) as f:
        print '<ol>'
        for (idx, line) in enumerate(f.readlines()):
            print '<li id="' + str(idx + 1) + '"><pre style="margin-left: 1em; display: inline; color: black"><code>' + cgi.escape(line.rstrip('\n')) + '</code></pre></li>'
        print '</ol>'

print '</body>'
print '</html>'
