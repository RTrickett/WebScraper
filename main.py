# Web scraper to collect tyre info given a user input
#
# Author: Rowan Trickett-Tappenden
# Date: Sep 2022

from xlwt import Workbook, Font, XFStyle
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests

# create a workbook and add an empty sheet
wb = Workbook()
sheet = wb.add_sheet('Sheet 1')
idx = 1

# Heading style
font1 = Font()
font1.bold = True
style = XFStyle()
style.font = font1

# Adding headings
sheet.write(0, 0, "Website", style)
sheet.write(0, 1, "Brand", style)
sheet.write(0, 2, "Tyre Pattern", style)
sheet.write(0, 3, "Tyre Size", style)
sheet.write(0, 4, "Price", style)

# take user input for tyre specification that will be searched for
print("Enter Tyre Specs")
width = input("Width: ")
aspect_ratio = input("Aspect Ratio: ")
diameter = input("Rim Size: ")

# URLs for pages to be scraped url1 - national, url2 - blackcircles
url1 = "https://www.national.co.uk/tyres-search?width=" + width + "&profile=" + aspect_ratio \
       + "&diameter=" + diameter + "&pc=S101NU"
url2 = "https://www.blackcircles.com/tyres/" + width + "-" + aspect_ratio + "-" + diameter

# urls = ["https://www.national.co.uk/tyres-search?width=205&profile=55&diameter=16&pc=S101NU",
#        "https://www.national.co.uk/tyres-search?width=225&profile=50&diameter=16&pc=S101NU",
#        "https://www.national.co.uk/tyres-search?width=185&profile=60&diameter=14&pc=S101NU"]


# Gathering data from the first website
first_page_to_scrape = requests.get(url1)
#print(first_page_to_scrape)   # prints a response relating to if the url exists and responds

if first_page_to_scrape.status_code != 200:
    print(url1 + " - Page not found")
else:
    soup = BeautifulSoup(first_page_to_scrape.content, "html.parser")
    base1 = urlparse(url1).netloc     # find base of url

    num_data = 0
    for details in soup.find_all("div", attrs={"class": "details"}):
        num_data += 1
        img_tag = details.find('img')
        pattern_link = details.find('a').text  # extracts only text
        tyre_size = details.find_all('p')[
            1].text.strip()  # collects text from second instance of p & removes empty space

        sheet.write(idx, 0, base1)
        sheet.write(idx, 1, img_tag.attrs['alt'])  # finding brand from alt section of image
        sheet.write(idx, 2, pattern_link)          # collecting tyre pattern
        sheet.write(idx, 3, tyre_size)             # collecting tire size
        idx += 1

    idx = idx-num_data
    for price in soup.find_all("div", attrs={"class": "price text-center padding-2"}):
        cost = price.find('strong').text.strip()    # find cost (per tyre)
        sheet.write(idx, 4, cost)
        idx += 1


# Gathering data from the second website
second_page_to_scrape = requests.get(url2)

if second_page_to_scrape.status_code != 200:
    print(url2 + " - Page not found")
else:
    soup2 = BeautifulSoup(second_page_to_scrape.content, "html.parser")
    base2 = urlparse(url2).netloc     # find base of url

    for details in soup2.find_all("div", attrs={"class": "resBox"}):
        img_data = details.find("img")
        brand = img_data.attrs["title"]
        pattern_link = details.find("a", attrs={"class": "model-name"}).text.strip()
        tyre_size = details.find("p", attrs={"class": "model-size"}).text
        price = details.find("div", attrs={"class": "model-price"}).text
        sheet.write(idx, 0, base2)         # base of URL
        sheet.write(idx, 1, brand)         # get tyre brand
        sheet.write(idx, 2, pattern_link)  # get tyre pattern link
        sheet.write(idx, 3, tyre_size)     # get tyre size
        sheet.write(idx, 4, price)         # get tyre price
        idx += 1

wb.save('Tyre Data.csv')    # save data as csv
