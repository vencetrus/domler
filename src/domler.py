#!/usr/bin/env python

"""
Copyright (c) 2017

"""

from urllib2 import Request, urlopen
from bs4 import BeautifulSoup
from common.banner import banner
from optparse import OptionParser

subdomains = []
url_original = ""

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
    a = urlopen(req).read()
    soup = BeautifulSoup(a, 'html.parser')
    x = (soup.find_all('a'))
    for i in x:
        file_name = i.attrs['href']
        # file_name = i.extract().get_text()
        # try:
        #     file_name = i.attrs['href']
        # except:
        #     None
        # url_new = url + file_name
        url_new = file_name
        url_new = url_new.replace(" ","%20")
        if "http" not in url_new:
            if url_new[0] != "/":
                url_new = url_original + "/" + url_new
            else:
                url_new = url_original + url_new
        try:
            if (isread(url_new) == False and (url_original in url_new)):
                subdomains.append(url_new)
                print(url_new)
                read_url(url_new)

        except Exception as inst:
            # print inst[0]
            None

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
    read_url(url_original)
    return subdomains

if __name__ == "__main__":
    main()