#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import sys
import datetime
from BeautifulSoup import BeautifulSoup

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

def findCoverAndDownload(isbn):
    try:
        url = 'http://covers.openlibrary.org/b/isbn/' + isbn + '-L.jpg'
        urllib.urlretrieve(url, isbn + '.jpg')
    except:
        print("Couldn't get cover image for isbn=" % isbn)

def getTitleFromWebSite(url):
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req)
    html = resp.read()
    soup = BeautifulSoup(html)
    return soup.html.head.title.string

def makeUrlEntry(url):
    date = datetime.date.today().strftime('%Y-%m-%d')
    title = getTitleFromWebSite(url)
    return """@misc{<++>,\n title = {%s},\n author = {},\n howpublished =\
    \n {\url{%s}},\n note = {Accessed: %s}\n}""" %\
    (title, url, date)

def makeEntry(query, outputFile):
    result = None
    if query.isdigit():
        result = findAtOttobib(query)
    elif query.startswith('http'):
        result = makeUrlEntry(query)
    if result:
        print(result)
        #findCoverAndDownload(query)
        outputFile.write(result + '\n\n')
    else:
        print('Not found')

def inputLoop(outputFile):
    while True:
        try:
            query = raw_input('> ')
        except:
            break
        makeEntry(query, outputFile)

if __name__ == '__main__':
    try:
        f = open(sys.argv[1], 'a')
    except:
        print('Usage: python isbn2bibtex <FILENAME_TO_APPEND_TO> [<QUERY>]')
        sys.exit(1)
        
    if len(sys.argv) == 3:
        makeEntry(sys.argv[2], f)
    else:
        inputLoop(f)
    f.close()

