from bs4 import BeautifulSoup
import requests
import time
from object_categories import catlist
import csv

paginationlist = []
namelist = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
}
def scrape_page(url):
    while True:
        b = requests.get(url, headers=headers)
        soup = BeautifulSoup(b.content, 'lxml')
        nextpage = soup.find('a', {'aria-label': 'Next'})
        if nextpage:
            uu = nextpage.get('href')
            url = 'http://www.yellowpages.com.eg' + str(uu)
            paginationlist.append(url)
            print(url)
            time.sleep(5)
        else:
            break
        continue


def scrapenames(url1):
    r = requests.get(url1, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    adds = soup.find_all('div', class_='col-xs-12 item-details')
    for add in adds:
        name = add.find('a', class_='item-title').text
        if any(k in name for k in namelist):
            pass
        else:
            namelist.append(name)
    return namelist


for urls in catlist[0:221]:
    scrape_page(urls)
    print(f'Scrpaing {urls} phase 1')
    time.sleep(5)
time.sleep(300)

for urls in catlist[222:421]:
    scrape_page(urls)
    print(f'Scraping {urls} phase 2')
    time.sleep(5)

time.sleep(300)
for urls in catlist[421:664]:
    scrape_page(urls)
    scrape_page(urls)
    print(f'Scraping {urls} phase 3')
    time.sleep(5)

        
for x in paginationlist:
    scrapenames(x)
    print(f'Scraping {x}')
    time.sleep(10)
