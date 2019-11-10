from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import *
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup as soup
import re
import threading
import sys
from urllib.error import HTTPError
from urllib.error import URLError
from time import sleep
app = QtWidgets.QApplication ([])
dlg = uic.loadUi ("okScraper.ui")
startCal = QtWidgets.QCalendarWidget ()
startCal.setGridVisible (True)
stopCal = QtWidgets.QCalendarWidget ()
stopCal.setGridVisible (True)
startURL = "https://okcountyrecords.com/"
cancelButtonFlag = False

def grabCounties():
    url = "https://okcountyrecords.com/site-list"
    request = Request(url, headers = {'User-Agent' :\
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"})
    uClient = urlopen (request)
    page_html = uClient.read ()
    uClient.close ()

    pageSoup = soup (page_html, 'html.parser')
    pageSoup = pageSoup.body.tbody

    for tr in pageSoup.find_all('tr'):
        county = str(tr.find('td').find('span'))
        county = county[21:-14]
        if (len (county) > 0):
            dlg.countyComboBox.addItem(county)

def toggleButtons(setBool, clear=True):
    if clear == True:
        dlg.instrumentComboBox.clear()
        dlg.sectionComboBox.clear()
        dlg.townshipComboBox.clear()
        dlg.rangeComboBox.clear()
        dlg.instrumentComboBox.addItem("Instrument Type")
        dlg.sectionComboBox.addItem("Section")
        dlg.townshipComboBox.addItem("Township")
        dlg.rangeComboBox.addItem("Range")
        dlg.startDateButton.setText("Start Date")
        dlg.stopDateButton.setText("Stop Date")
 
    dlg.instrumentComboBox.setEnabled(setBool)
    dlg.sectionComboBox.setEnabled(setBool)
    dlg.townshipComboBox.setEnabled(setBool)
    dlg.rangeComboBox.setEnabled(setBool)
    dlg.startDateButton.setEnabled(setBool)
    dlg.stopDateButton.setEnabled(setBool)
    dlg.scrapeButton.setEnabled(setBool)

def grabComboItems ():
    county = dlg.countyComboBox.currentText()

    if county == "County":
        toggleButtons(False, clear = True)
        dlg.instrumentComboBox.setEditable (False)
        dlg.townshipComboBox.setEditable (False)
        dlg.sectionComboBox.setEditable (False)
        dlg.rangeComboBox.setEditable (False)
    else:
        toggleButtons(True, clear = True)
        url = "https://okcountyrecords.com/search/" + county.replace(" ", "+")
        request = Request(url, headers = {'User-Agent' :\
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"})
        uClient = urlopen (request)
        page_html = uClient.read ()
        uClient.close ()

        pageSoup = soup (page_html, 'html.parser')
        instrumentSoup = pageSoup.body.find_all('dd')[4].find_all('option')
        sectionSoup = pageSoup.body.find_all('dd')[9].find_all('option')
        townshipSoup = pageSoup.body.find_all('dd')[10].find_all('option')
        rangeSoup = pageSoup.body.find_all('dd')[11].find_all('option')

        for instrument in instrumentSoup:
            matches=re.findall(r'\=\"(.+?)\"\>',str(instrument))
            if len(matches) > 0:
                dlg.instrumentComboBox.addItem(re.sub('amp;', '', str(matches[0])))
        if dlg.instrumentComboBox.count () < 2:
            dlg.instrumentComboBox.setEditable (True)
            dlg.instrumentComboBox.clear ()
            dlg.instrumentComboBox.addItem ("Type Instrument Here")
        else:
            dlg.instrumentComboBox.setEditable (False)

        
        for section in sectionSoup:
            matches=re.findall(r'\=\"(.+?)\"\>',str(section))
            if len(matches) > 0:
                dlg.sectionComboBox.addItem(str(matches[0]))
        if dlg.sectionComboBox.count () < 2:
            dlg.sectionComboBox.setEditable (True)
            dlg.sectionComboBox.clear ()
            dlg.sectionComboBox.addItem ("Type Section")
        else:
            dlg.sectionComboBox.setEditable (False)

        for township in townshipSoup:
            matches=re.findall(r'\=\"(.+?)\"\>',str(township))
            if len(matches) > 0:
                if not str(matches[0])[-1] == ".":
                    dlg.townshipComboBox.addItem(str(matches[0]))
        if dlg.townshipComboBox.count () < 2:
            dlg.townshipComboBox.setEditable (True)
            dlg.townshipComboBox.clear ()
            dlg.townshipComboBox.addItem ("Type Township")
        else:
            dlg.townshipComboBox.setEditable (False)

        for rangee in rangeSoup:
            matches=re.findall(r'\=\"(.+?)\"\>',str(rangee))
            if len(matches) > 0:
                if not str(matches[0])[-1] == "." and not str(matches[0])[0] == "0":
                    dlg.rangeComboBox.addItem(str(matches[0]))
        if dlg.rangeComboBox.count () < 2:
            dlg.rangeComboBox.setEditable (True)
            dlg.rangeComboBox.clear ()
            dlg.rangeComboBox.addItem ("Type Range")
        else:
            dlg.townshipComboBox.setEditable (False)

        toggleButtons(True, clear=False)

def openCal (title):
    toggleButtons (False, clear=False)
    if title == "Select Start Date":
        startCal.show()
        startCal.setWindowTitle(title)
    elif title == "Select Stop Date":
        stopCal.show()
        stopCal.setWindowTitle(title)

def closeCal(title):
    toggleButtons (True, clear=False)
    if title == "start":
        startCal.hide ()
        startDate = startCal.selectedDate ()
        dlg.startDateButton.setText ("Start: " + str(startDate.toPyDate()))
    if title == "stop":
        stopCal.hide ()
        stopDate = stopCal.selectedDate ()
        dlg.stopDateButton.setText ("Stop: " + str(stopDate.toPyDate()))
    
def setConnects ():
    dlg.countyComboBox.currentIndexChanged.connect (grabComboItems)
    dlg.startDateButton.clicked.connect (lambda: openCal("Select Start Date"))
    dlg.stopDateButton.clicked.connect (lambda: openCal("Select Stop Date"))
    startCal.selectionChanged.connect (lambda: closeCal('start'))
    stopCal.selectionChanged.connect (lambda: closeCal('stop'))
    dlg.scrapeButton.clicked.connect (lambda: startScrapeThread (startURL))

def scrape (baseURL):
    global cancelButtonFlag
    county = dlg.countyComboBox.currentText ()
    startPage = 1
    baseURL = makeURL(baseURL)
    if baseURL == "nope":
        QMessageBox.about (dlg, "Form Error", "There is not enough information to perform a data scrape.  Try selecting more information.")
        return
    url = baseURL + "/page-1"
    try:
        request = Request(url, headers = {'User-Agent' :\
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"})
        uClient = urlopen (request)
        page_html = uClient.read ()
        uClient.close ()

        pageSoup = soup (page_html, "html.parser")
        pageSoup = pageSoup.body

        # find out how many pages of results there are and obtain that number
        pagination = pageSoup.find ("nav", {"class":"pagination"})
        pageList = str(pagination)
        try:
            pageList = pageList.split("\n",7)[-2];
            result = re.search("/page-(.*)<", str(pageList))
            almostThere = result.group(1)
            pageTotal = ""
            for char in almostThere:
                if char.isdigit ():
                    pageTotal += char
                    continue
                else:
                    break
        except:
            # Check if there are no results and handle that
            # if no result:
                # QMessageBox.about (dlg, "Form Error", "There were no results. Try a different search.")
            # else:
            pageTotal = 0
        
        pageTotal = int(pageTotal) + 1
        workingPage = 1

        for page in range(1, pageTotal + 1):
            if page == 0:
                continue
            else:
                url = baseURL + "/page-" + str (workingPage)

                print ("DEBUG:  I'm opening result url " + url)
                print ("DEBUG")

                request = Request(url, headers = {'User-Agent' :\
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"})
                # print ("1")
                uClient = urlopen (request)
                page_html = uClient.read ()
                uClient.close ()
                # print ("2")
                # find list of results on result page
                pageTag = soup (page_html, "html.parser")
                pageTag = pageTag.body.tbody

                # for each result in the result page, go to that result and pull data
                for i in pageTag:
                    # print ("in pagetag for loop                              3")
                    if cancelButtonFlag:
                        # print ("in cancelButtonFlag condition: should only be here if cancelButtonFlag == True                             4")
                        scrapeCanceled ()
                        sys.exit ()
                    # print ("after cancelButtonFlag condition                                         5")

                    i = i.a
                    i = str(i)

                    i = re.search("href=\"(.*)\">", i)
                    i = i.group (1)

                    url = "https://okcountyrecords.com" + i

                    # print ("DEBUG:  I'm opening page url" + url)
                    # print ("DEBUG")

                    # Open next result from result page
                    request = Request(url, headers = {'User-Agent' :\
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"})
                    uClient = urlopen (request)
                    page_html = uClient.read ()
                    uClient.close ()

                    # Program has reached the destination page for desired data
                    finalPage = soup (page_html, "html.parser")

                    # print ("DEBUG:  I'm looking in tables for data")
                    # print ("DEBUG")

                    # find all data fields in the table that contains the desired data
                    tables = finalPage.find_all('table')
                    for tbl in tables:
                        if tbl == tables[0]:
                            tds = tbl.findChildren ('td')
                        else:
                            tds += tbl.findChildren ('td')

                    # TODO: Add better handling here.  could result in shifted CSV rows if any of these data are missing.
                    book = re.search(">(.*)</td>", str(tds[0]))
                    book = book.group (1)

                    page = re.search(">(.*)</td>", str(tds[1]))
                    page = page.group (1)

                    instrument = re.search("heavy\">(.*)</td>", str(tds[2]))
                    instrument = instrument.group (1)

                    documentStamps = re.search("<td>(.*)</td>", str(tds[6]))
                    documentStamps = documentStamps.group (1)

                    recordedOn = re.search ("<td>(.*)</td>", str(tds[7]))
                    recordedOn = recordedOn.group (1)

                    if len(tds) > 8:
                        instrumentDate = re.search ("<td>(.*)</td>", str(tds[8]))
                        instrumentDate = instrumentDate.group (1)
                    else:
                        instrumentDate = ""

                    addrow (county, book, page, instrument, documentStamps, recordedOn, instrumentDate, url)

                    # write the data to CSV
                    # writeCSV (county, book, page, instrument, documentStamps, recordedOn, instrumentDate, url)

                    # delay so we don't overwhelm the web servers and get blocked or something
                    sleep (2.5)

                # increment page number to go to next page
                workingPage += 1
    except HTTPError:
        QMessageBox.about (dlg, "URL/HTTP Error", "Could not access {} Check your internet connection and try again".format (url))
    except URLError:
        QMessageBox.about (dlg, "URL/HTTP Error", "Could not access {} Check your internet connection and try again".format (url))

def makeURL (url):
    url += "results/"
    counter = 0

    if not dlg.instrumentComboBox.currentText () == "Instrument Type":
        url += "instrument-type={}:".format (dlg.instrumentComboBox.currentText ().replace (" ", ""))
    else:
        counter += 1
    if not dlg.startDateButton.text () == "Start Date":
        url += "recorded-start={}:".format (dlg.startDateButton.text ()[7:])
    if not dlg.stopDateButton.text () == "Stop Date":
        url += "recorded-end={}:".format (dlg.stopDateButton.text ()[6:])
    if not dlg.sectionComboBox.currentText () == "Section":
        url += "section={}:".format (dlg.sectionComboBox.currentText ().replace (" ", ""))
    else:
        counter += 1
    if not dlg.townshipComboBox.currentText () == "Township":
        url += "township={}:".format (dlg.townshipComboBox.currentText ().replace (" ", ""))
    else:
        counter += 1
    if not dlg.rangeComboBox.currentText () == "Range":
        url += "range={}:".format (dlg.rangeComboBox.currentText ().replace (" ", ""))
    else:
        counter += 1
    
    if counter < 4:
        url += "site={}:".format (dlg.countyComboBox.currentText ().replace (" ", ""))
        url = url[:-1]
    else:
        url = "nope"

    print (url)
    return url

def startScrapeThread(url):
	toggleButtons (False, clear=False)
	global scrapeThread
	scrapeThread = threading.Thread(target=scrape, args=url)
	scrapeThread.daemon = True
	scrapeThread.start()
	# root.after(20, checkScrapeThread)

def stopScrapeThread ():
    global cancelButtonFlag
    cancelButtonFlag = True
    toggleButtons (True, clear=False)

def checkScrapeThread ():
    if scrapeThread.is_alive():
        print ("yah")
		# root.after(20, checkScrapeThread)
    else:
        pass

def scrapeCanceled ():
	global cancelButtonFlag
	# scrapeThread.join ()
	b1.config(state=ACTIVE)
	b3.config(state=ACTIVE)
	b2.config(state=DISABLED)
	cancelButtonFlag = False

def addrow (county, book, page, instrument, documentStamps, recordedOn, instrumentDate, url):
    # Create a empty row at bottom of table
    numRows = dlg.dataTable.rowCount ()
    dlg.dataTable.insertRow (numRows)
    # Add text to the row
    dlg.dataTable.setItem(numRows, 0, QtWidgets.QTableWidgetItem("test"))
    dlg.dataTable.setItem(numRows, 1, QtWidgets.QTableWidgetItem(book))
    dlg.dataTable.setItem(numRows, 2, QtWidgets.QTableWidgetItem(page))
    dlg.dataTable.setItem(numRows, 3, QtWidgets.QTableWidgetItem(instrument))
    dlg.dataTable.setItem(numRows, 4, QtWidgets.QTableWidgetItem(documentStamps))
    dlg.dataTable.setItem(numRows, 5, QtWidgets.QTableWidgetItem(recordedOn))
    dlg.dataTable.setItem(numRows, 6, QtWidgets.QTableWidgetItem(instrumentDate))
    dlg.dataTable.setItem(numRows, 7, QtWidgets.QTableWidgetItem(url))

def main ():
    grabCounties ()
    setConnects ()
    dlg.show()
    app.exec()

if __name__ == "__main__":
    main ()