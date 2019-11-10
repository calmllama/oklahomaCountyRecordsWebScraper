#!/usr/bin/python3

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QComboBox
from urllib.request import urlopen
from urllib.request import Request
from PyQt5.QtCore import QSize, QRect    
from bs4 import BeautifulSoup as soup
import re
import time
import html5lib


def grabInstruments():
    url = "https://okcountyrecords.com/search/adair"
    request = Request(url, headers = {'User-Agent' :\
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"})
    uClient = urlopen (request)
    page_html = uClient.read ()
    uClient.close ()

    pageSoup = soup (page_html, 'html.parser')
    rangeSoup = pageSoup.body.find_all('dd')[11].find_all('option')

    townships = []
    
    for rangee in rangeSoup:
        matches=re.findall(r'\=\"(.+?)\"\>',str(rangee))
        if len(matches) > 0:
            if not str(matches[0])[-1] == "." and not str(matches[0])[0] == "0":
                print (str(matches[0]))
                print ("")
                townships.append(str(matches[0]))
    print (len(townships))

    # shoudl be 65 township

grabInstruments()