#!/usr/bin/env python

"""
Copyright (c) 2017

"""

from urllib2 import Request, urlopen, HTTPError
from bs4 import BeautifulSoup
from common.banner import banner
from optparse import OptionParser

import threading, sys, time, datetime

subdomains = []
url_original = ""

def saveFile(File):
    global subdomains
    f = open(File, "w")
    for i in range(len(subdomains)):
        f.write(subdomains[i] + "\n")
    f.close()
    print '[+] Archivo guardado correctamente'


def isread(url):
    global subdomains
    for i in range(len(subdomains)):
        if subdomains[i] == url:
            return True
    return False

def read_url(url):
    """
    :param url: target to find subfolders
    :return:
    """
    global subdomains
    global url_original


    url = url.replace(" ","%20")

    req = Request(url)

    try:
        a = urlopen(req).read()
    except HTTPError as e:
        if e.code == 404:
            None
            sys.exit()
        print e
        sys.exit()
    except Exception as e:
        print e
        sys.exit()

    soup = BeautifulSoup(a, 'html.parser')
    x = (soup.find_all('a'))

    for i in x:
        file_name = i.extract().get_text()
        try:
            file_name = i.attrs['href']
        except:
            None

        url_new = file_name
        url_new = url_new.replace(" ","%20")

        try:
            if "http" not in url_new:
                if url_new[0] != "/":
                    url_new = url_original + "/" + url_new
                else:
                    url_new = url_original + url_new

            if (isread(url_new) == False and (url_original in url_new)):
                subdomains.append(url_new)
                print(url_new)
                r = threading.Thread(target=read_url, args=(url_new,))
                r.start()



        except Exception as inst:
            print inst[0]
            # None



def main():
    """
    Main function of domler when running from command line.
    """
    global url_original
    global subdomains


    banner()

    usage = "usage:%prog [options] arg1"
    parser = OptionParser(usage=usage)
    parser.add_option("-u", "--url", action="store",
                      type="string", dest="url",
                      help="target to search subfiles")

    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose",
                      help="show VERBOSE")

    parser.add_option("-f", "--filename", dest="outputfile",
                      metavar = "FILE", help ="write output to FILE")

    (options, args) = parser.parse_args()

    url_original = options.url
    print '\n'
    print '[*] Domler finder begins'
    print '------------------------------------------------'

    print options.url
    subdomains.append(url_original)

    start = time.time()
    t = threading.Thread(name='hilo primero',
                         target=read_url,
                         args=(url_original,))
    t.start()

    while threading.active_count()>1:
        None

    print 'hilo principal acabado'
    # while t.is_alive:
    #     pass

    # read_url(url_original)

    end = time.time()
    diffTime = end - start
    msg = "Date & Time: " + time.strftime('%d/%m/%Y %H:%M:%S')
    print msg
    msg = "Completed in: " + str(datetime.timedelta(seconds=diffTime)).split(".")[0]
    print msg


    if options.outputfile:
        saveFile(options.outputfile)

if __name__ == "__main__":
    main()