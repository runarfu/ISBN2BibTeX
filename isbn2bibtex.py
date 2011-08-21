#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import sys

def findAtOttobib(isbn):
    try:
        url = 'http://www.ottobib.com/search/searchisbn'
        values = {'citetype' : 'BibTeX', 'search' : isbn}

        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        resp = urllib2.urlopen(req)
        page = resp.read()

        start = page.find('@Book')
        stop  = page.find('</textarea>', start)
        if start == -1 or stop == -1:
            return None
        result = page[start:stop]
        return result
    except:
        return None

def inputLoop(outputFile):
    while True:
        try:
            isbn = raw_input('> ')
        except:
            break
        result = findAtOttobib(isbn)
        if result:
            print(result)
            outputFile.write(result + '\n\n')
        else:
            print('Not found')

try:
    f = open(sys.argv[1], 'a')
except:
    print('Usage: python isbn2bibtex <FILENAME_TO_APPEND_TO>')
    sys.exit(1)

inputLoop(f)
f.close()

