from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from urllib.request import Request
import re


def grabCounties():
    url = "https://okcountyrecords.com/site-list"
    request = Request(url, headers = {'User-Agent' :\
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"})
    uClient = urlopen (request)
    page_html = uClient.read ()
    uClient.close ()

    pageSoup = soup (page_html, 'html.parser')
    pageSoup = pageSoup.body.tbody

    countyList = []

    for tr in pageSoup.find_all('tr'):
        county = str(tr.find('td').find('span'))
        county = county[21:-14]
        if (len (county) > 0):
            countyList.append (county)

    print (countyList)

    return countyList

if __name__ == '__main__':
    grabCounties ()
