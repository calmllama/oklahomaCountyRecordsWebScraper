from tkinter import *
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import HTTPError
from urllib.error import URLError
from tkinter import messagebox
from bs4 import BeautifulSoup as soup
import threading
import re
import csv
import os
import sys
from time import sleep

cancelButtonFlag = False

fields = 'instrument-type', 'recorded-start', 'recorded-stop', 'section', 'township', 'range', 'county'

def fetch(entries):
	# Base search result URL to be added to with user inputted data
   url = "https://okcountyrecords.com/results/"
   for entry in entries:
      field = entry[0]
      text  = entry[1].get()
      if text != "":
	      # OKcountyrecords uses "+" for spaces in URLS.  This replaces " " with "+"
	      if field != "county" and text != "":
	      	url += field + "=" + text + ":"
	      elif field == "county":
	      	county = text
	      	# Makes a CSV file named after the county that's being scraped
	      	makeCSV (text)
	      	# URL here doesn't include page number. Will be added in scrape function
	      	url +="site=" + text + "/page-"
	      	startScrapeThread (url, county)

	  # If there is no text in the county box, throw an error.
      elif text == "" and field == "county":
	      	messagebox.showwarning ("NO County Entered", "Please enter a County and try agian.")

def makeform(root, fields):
   entries = []
   root.title ('OKcountyrecords Scraper')
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=15, text=field, anchor='w')
      ent = Entry(row)
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries.append((field, ent))
   return entries

# make directory and CSV file to save scraped data
def makeCSV (county):
	print ("DEBUG:  I'm creating directory and CSV")
	print ("DEBUG")
	if not os.path.exists("OKcountyrecords"):
		os.makedirs("OKcountyrecords")
	try:
		with open('OKcountyrecords/' + county, 'w') as csvfile:
					filewriter = csv.writer(csvfile, dialect='excel-tab',
						quotechar='|', quoting=csv.QUOTE_MINIMAL)
					filewriter.writerow(["county", "book", "page", "instrument", "documentStamps", "recordedOn", "instrumentDate", "url"])
	except PermissionError:
		messagebox.showerror ("Permission Error", "It looks like you have a file open with the same name as the one being saved.  Please close that file and try again.")
		scrapeCanceled ()
		return

def grabCounties(url):
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

    return countyList


# writes data to CSV.
def writeCSV (county, book, page, instrument, documentStamps, recordedOn, instrumentDate, URL):
	print ("DEBUG:  I'm writing to CSV")
	print ("DEBUG")
	with open('OKcountyrecords/' + county, 'a') as csvfile:
		filewriter = csv.writer(csvfile, dialect='excel-tab',
			quotechar='|', quoting=csv.QUOTE_MINIMAL)
		filewriter.writerow([county, book, page, instrument, documentStamps, recordedOn, instrumentDate, URL])

def startScrapeThread(url, county):
	b1.config(state=DISABLED)
	b2.config(state=ACTIVE)
	b3.config(state=DISABLED)
	global scrapeThread
	scrapeThread = threading.Thread(target=scrape, args=(url, county))
	scrapeThread.daemon = True
	scrapeThread.start()
	root.after(20, checkScrapeThread)

def stopScrapeThread ():
	global cancelButtonFlag
	cancelButtonFlag = True

def checkScrapeThread ():
	if scrapeThread.is_alive():
		root.after(20, checkScrapeThread)
	else:
		b1.config(state=ACTIVE)
		b3.config(state=ACTIVE)
		b2.config(state=DISABLED)
		pass

def scrapeCanceled ():
	global cancelButtonFlag
	# scrapeThread.join ()
	b1.config(state=ACTIVE)
	b3.config(state=ACTIVE)
	b2.config(state=DISABLED)
	cancelButtonFlag = False


def scrape (baseURL, county):
	global cancelButtonFlag
	startPage = 1

	url = baseURL + "1"
	print ("URL IS: " + url)
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
		except:
			messagebox.showerror ("Form Error", "Make sure you spelled everything correctly in the forms and try agian.")
		result = re.search("/page-(.*)<", str(pageList))
		almostThere = result.group(1)
		pageTotal = ""
		for char in almostThere:
			if char.isdigit ():
				pageTotal += char
				continue
			else:
				break
		pageTotal = int(pageTotal) + 1
		workingPage = 1

		for page in range(1, pageTotal + 1):
			if page == 0:
				continue
			else:
				url = baseURL + str (workingPage)

				print ("DEBUG:  I'm opening result url " + url)
				print ("DEBUG")

				request = Request(url, headers = {'User-Agent' :\
            		"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"})
				print ("1")
				uClient = urlopen (request)
				page_html = uClient.read ()
				uClient.close ()
				print ("2")
				# find list of results on result page
				pageTag = soup (page_html, "html.parser")
				pageTag = pageTag.body.tbody

				# for each result in the result page, go to that result and pull data
				for i in pageTag:
					print ("in pagetag for loop                              3")
					if cancelButtonFlag:
						print ("in cancelButtonFlag condition: should only be here if cancelButtonFlag == True                             4")
						scrapeCanceled ()
						sys.exit ()
					print ("after cancelButtonFlag condition                                         5")

					i = i.a
					i = str(i)

					i = re.search("href=\"(.*)\">", i)
					i = i.group (1)

					url = "https://okcountyrecords.com" + i

					print ("DEBUG:  I'm opening page url" + url)
					print ("DEBUG")

					# Open next result from result page
					request = Request(url, headers = {'User-Agent' :\
            			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"})
					uClient = urlopen (request)
					page_html = uClient.read ()
					uClient.close ()

					# Program has reached the destination page for desired data
					finalPage = soup (page_html, "html.parser")

					print ("DEBUG:  I'm looking in tables for data")
					print ("DEBUG")

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

					# write the data to CSV
					writeCSV (county, book, page, instrument, documentStamps, recordedOn, instrumentDate, url)
					# delay so we don't overwhelm the web servers and get blocked or something
					sleep (5)

				# increment page number to go to next page
				workingPage += 1
	except HTTPError:
		messagebox.showerror ("URL/HTTP Error", "Could not access " + url + " Check your internet connection and try again")
	except URLError:
		messagebox.showerror ("URL/HTTP Error", "Could not access " + url + " Check your internet connection and try again")

def endProgram ():
	root.destroy ()
	sys.exit ()

if __name__ == '__main__':
	root = Tk()
	root.geometry ("400x300")
	ents = makeform(root, fields)
	root.bind('<Return>', (lambda event, e=ents: fetch(e)))
	global b1
	b1 = Button(root, text='Scrape!',
		command=(lambda e=ents: fetch(e)))
	b1.pack(side=LEFT, padx=5, pady=5)
	global b2
	b2 = Button(root, text='Cancel', command=stopScrapeThread)
	b2.pack(side=LEFT, padx=5, pady=5)
	b2.config(state=DISABLED)
	global b3
	b3 = Button(root, text='Quit', command=endProgram)
	b3.pack(side=LEFT, padx=5, pady=5)
	root.mainloop()
