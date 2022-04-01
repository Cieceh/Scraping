from bs4 import BeautifulSoup
import requests
import re
import time

textcat = []
def text_categories(url):
    r = requests.get('https://yellowpages.com.eg/en/related-categories')
    soup = BeautifulSoup(r.content, 'lxml')
    for div in soup.find_all('div', class_='well-content'):
        for catss in div.find_all('a', class_='well'):
            textcat.append(catss.text)
    return textcat


catlist = []
def scrape_categories(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    for div in soup.find_all('div', class_='well-content'):
        for cat in div.find_all('a', class_='well'):
            firsthalf = 'https://yellowpages.com.eg' + str(cat['href'])
            catlist.append(firsthalf)
    return catlist

for x in range(1,35):
    scrape_categories(f'https://yellowpages.com.eg/en/related-categories/p{x}')
    text_categories(f'https://yellowpages.com.eg/en/related-categories/p{x}')
    time.sleep(5)
    print(f'Scraping page{x}')

textcategories= list(map(lambda s: re.sub('\s\(\d+\)', '', s), textcat))