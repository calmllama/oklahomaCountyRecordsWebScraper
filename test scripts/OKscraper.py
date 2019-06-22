from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import re
import csv
import os

countys = ["adair", "atoka", "beaver", "alfalfa", "beckham", "carter", "blaine", "choctaw",
"comanche", "craig", "custer", "cotton", "delaware", "ellis", "garvin", "dewey", "grant", "harmon", "harper",
"jackson", "hughes", "johnston", "kingfisher", "kiowa", "latimer", "logan", "leflore", "love", "marshall",
"mayes", "mcclain", "mccurtain", "muskogee", "nowata", "noble", "okmulgee", "pawnee", 
"pittsburg", "pushmataha", "roger mills", "sequoyah", "stephens", "seminole", "washington",
"washita", "tillman", "woodward"]

minDeedCounties = ["bryan", "cherokee", "cimarron", "coal", "greer", "haskell", "jefferson", "kay", "lincoln", "major", "mcintosh", "murray",
"okfuskee", "ottawa", "osage", "pontotoc", "rogers", "texas",]

if not os.path.exists("OKcountyrecords"):
    os.makedirs("OKcountyrecords")

for county in countys:

	with open('OKcountyrecords/' + county, 'w') as csvfile:
					filewriter = csv.writer(csvfile, dialect='excel-tab',
						quotechar='|', quoting=csv.QUOTE_MINIMAL)
					filewriter.writerow(["county", "book", "page", "instrument", "documentStamps", "recordedOn", "instrumentDate"])

	startPage = 1
	startUrl = "https://okcountyrecords.com/results/instrument-type=Mineral+Deed:site=" + county + "/page-" + str (startPage)    

	uClient = urlopen (startUrl)
	page_html = uClient.read ()
	uClient.close ()

	pageSoup = soup (page_html, "html.parser")
	pageSoup = pageSoup.body

	pagination = pageSoup.find ("nav", {"class":"pagination"})
	pageList = str(pagination)
	pageList = pageList.split("\n",7)[7];
	result = re.search("/page-(.*)<", str(pageList))
	almostThere = result.group(1)
	pageTotal = ""
	for char in almostThere:
		if char.isdigit ():
			pageTotal += char
			continue
		else:
			break
 
	for page in range(1, int(pageTotal) + 1):
		if page == 0:
			continue
		else:
			url = "https://okcountyrecords.com/results/instrument-type=Mineral+Deed:site=" + county + "/page-" + str (page)
			print ("DEBUG:  I'm opening " + url)
			print ("DEBUG")
			uClient = urlopen (url)
			page_html = uClient.read ()
			uClient.close ()

			pageTag = soup (page_html, "html.parser")
			pageTag = pageTag.body.tbody

			for i in pageTag:
				i = i.a
				i = str(i)
				print ("i: " + i)
				print ("")

				i = re.search("href=\"(.*)\">", i)
				i = i.group (1)

				print ("shorter i: " + i)
				print ("")
				url = "https://okcountyrecords.com" + i

				print ("DEBUG:  I'm opening " + url)
				print ("DEBUG")

				uClient = urlopen (url)
				page_html = uClient.read ()
				uClient.close ()

				finalPage = soup (page_html, "html.parser")

				print ("DEBUG:  I'm looking in tables for data")
				print ("DEBUG")

				tables = finalPage.find_all('table')
				for tbl in tables:
					if tbl == tables[0]:
						tds = tbl.findChildren ('td')
					else:
						tds += tbl.findChildren ('td')

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

				instrumentDate = re.search ("<td>(.*)</td>", str(tds[8]))
				instrumentDate = instrumentDate.group (1)
				
				# Write to CSV file
				print ("DEBUG:  I'm writing to CSV")
				print ("DEBUG")
				with open('OKcountyrecords/' + county, 'a') as csvfile:
					filewriter = csv.writer(csvfile, dialect='excel-tab',
						quotechar='|', quoting=csv.QUOTE_MINIMAL)
					filewriter.writerow([county, book, page, instrument, documentStamps, recordedOn, instrumentDate])

				# print ("County: " + county)
				# print ("Book: " + book)
				# print ("Page: " + page)
				# print ("################################################################")
				# break
			# break
		# break
	# break

 