from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import random
from Pagination import paginationlist, namelist, headers
from object_categories import textcategories


fakelist = []
mainlist = []

for x in paginationlist:
    url = f'https://yellowpages.com.eg/en/condensed-search/{x}'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    adds = soup.find_all('div', class_='content-widget searchResultsDiv')
    for items in adds:
        global sub
        suburl = items.find('a', class_='companyName companyTitle')['href']
        sub = 'https:' + suburl
        fakelist.append(sub)


def scrape(url):
    e = requests.get(url, headers=headers)
    soup = BeautifulSoup(e.content, 'lxml')
    openhours = soup.find_all('div', class_='col-xs-6 hours')
    for hours in openhours:
        saturday = hours.find('p', class_='opening-hours-day').text.strip().replace(' ', '')
        sunday = hours.find('p', class_='opening-hours-day').text.strip().replace(' ', '')
        monday = hours.find('p', class_='opening-hours-day').text.strip().replace(' ', '')
        tuesday = hours.find('p', class_='opening-hours-day').text.strip().replace(' ', '')
        wednesday = hours.find('p', class_='opening-hours-day').text.strip().replace(' ', '')
        thursday = hours.find('p', class_='opening-hours-day').text.strip().replace(' ', '')
        friday = hours.find('p', class_='opening-hours-day').text.strip().replace(' ', '')
        if monday and wednesday == 'Open24Hours':
            operating_hours_sun_start = 'Open24Hours'
            operating_hours_mon_start = 'Open24Hours'
            operating_hours_tue_start = 'Open24Hours'
            operating_hours_wed_start = 'Open24Hours'
            operating_hours_thu_start = 'Open24Hours'
            operating_hours_fri_start = 'Open24Hours'
            operating_hours_sat_start = 'Open24Hours'
            operating_hours_sun_end = 'Open24Hours'
            operating_hours_mon_end = 'Open24Hours'
            operating_hours_tue_end = 'Open24Hours'
            operating_hours_wed_end = 'Open24Hours'
            operating_hours_thu_end = 'Open24Hours'
            operating_hours_fri_end = 'Open24Hours'
            operating_hours_sat_end = 'Open24Hours'
        else:
            hh = lambda x: x.split('-')
            operating_hours_sun_start = hh(sunday)[0]
            operating_hours_mon_start = hh(monday)[0]
            operating_hours_tue_start = hh(tuesday)[0]
            operating_hours_wed_start = hh(wednesday)[0]
            operating_hours_thu_start = hh(thursday)[0]
            operating_hours_fri_start = hh(friday)[0]
            operating_hours_sat_start = hh(saturday)[0]
            operating_hours_sun_end = hh(sunday)[1]
            operating_hours_mon_end = hh(monday)[1]
            operating_hours_tue_end = hh(tuesday)[1]
            operating_hours_wed_end = hh(wednesday)[1]
            operating_hours_thu_end = hh(thursday)[1]
            operating_hours_fri_end = hh(friday)[1]
            operating_hours_sat_end = hh(saturday)[1]
    if not openhours:
        operating_hours_sun_start = ''
        operating_hours_mon_start = ''
        operating_hours_tue_start = ''
        operating_hours_wed_start = ''
        operating_hours_thu_start = ''
        operating_hours_fri_start = ''
        operating_hours_sat_start = ''
        operating_hours_sun_end = ''
        operating_hours_mon_end = ''
        operating_hours_tue_end = ''
        operating_hours_wed_end = ''
        operating_hours_thu_end = ''
        operating_hours_fri_end = ''
        operating_hours_sat_end = ''
    social = soup.find_all('div', class_='social-links-div')
    for item in social:
        try:
            facebook = item.find('a', class_='facebook')['href']
        except TypeError:
            facebook = ''
        try:
            twitter = item.find('a', class_='twitter')['href']
        except:
            twitter = ''
        try:
            instagram = item.find('a', class_='instagram')['href']
        except TypeError:
            instagram = ''
        try:
            youtube = item.find('a', class_='youtube')['href']
        except TypeError:
            youtube = ''
        try:
            whatsapp = item.find('a', class_='whatsapp')['href']
        except:
            whatsapp = ''
    keyslist = []
    if not soup.find_all('div', class_='header-div header-div-keywords'):
        keywords = ''
    else:
        for div in soup.find_all('div', class_='header-div header-div-keywords'):
            for a in div.find_all('a'):
                keywords = a.text
                keyslist.append(keywords)
    categorylst = []
    if not soup.find_all('div', class_='header-div header-div-categories'):
        categories = ''
    else:
        for div in soup.find_all('div', class_='header-div header-div-categories'):
            for a in div.find_all('a'):
                categories = a.text
                categorylst.append(categories)
    title = soup.find_all('div', class_='row companyName')
    for name in title:
        bn = name.find('p', class_='col-xs-12').text
    if not title:
        bn = soup.find('h1', class_='companyName').text
    for div in soup.find_all('div', class_='company-address'):
        address = div.find('span').text
    add2 = address.split(',')
    region = add2[-1]
    city = add2[-2]
    area = add2[-3]
    try:
        district = add2[-4]
    except IndexError:
        district = ''

    try:
        site = soup.find_all('div', class_='col-sm-8 col-xs-12 contacts-btns')
        for sites in site:
            website = sites.find('a', class_='website btn btn-default')['href']
        if not site:
            website = ''
    except:
        website = ''
    if not address:
        address = soup.find('span', class_='des-address address col-xs-8 padding_0').text
    seed = random.getrandbits(10)
    fax = ''
    email = ''
    pay = soup.find('div', class_='payment_div')
    if pay == None:
        payment = ''
    else:
        payment = pay.text
    try:
        rating = soup.find('span', class_='show-review').text
    except AttributeError:
        rating = ''
    delisearchlist = ['Delivery Pharmacies', 'Pharmacies Home Delivery', 'Delivery', 'Home Delivery', 'Restaurants Home Delivery' |
                  'Delivery Service', 'Supermarkets Home Delivery']
    if any(x in delisearchlist for x in keywords):
        delivery = 1
    elif any(x in delisearchlist for x in categories):
        delivery = 1
    else:
        delivery = 0
    eatoutsearch = ['Restaurants Eat out', 'Eat out']
    if any(x in eatoutsearch for x in keywords):
        eat_out = 1
    elif any(x in eatoutsearch for x in categories):
        eat_out = 1
    else:
        eat_out = 0
    parksearch = ['Smart & Automated Parking']
    if any(x in parksearch for x in categories):
        parking = 1
    else:
        parking = 0
    wifisearch = ["Internet Cafe's & Wi - Fi Hotspots "]
    if any(x in wifisearch for x in categories):
        wifi = 1
    else:
        wifi = 0
    smokesearch = ['Tobacco']
    if any(x in smokesearch for x in categories):
        smoking = 1
        shisha = 1
    else:
        smoking = 0
        shisha = 0
    alchol = ''
    banquet = ''
    minumium = ''
    reservation = ''
    price_range = ''
    kids_ares = ''
    try:
        branchlist = []
        for div in soup.find_all('div', class_='data branches-data'):
            for a in div.find_all('a'):
                branchlist.append(a.text)
                branch_no = len(branchlist) + 1
    except:
        branch_no = 0
    if not branchlist:
        branches = 0
    else:
        branches = 1

    for x in textcategories:
        if x in categorylst:
            inid = str((textcategories.index(x) + 10000))
    for z in namelist:
        if z == bn:
            global bus_id
            bus_id = inid + str(namelist.index(z))

    data = {'business_id': bus_id,
            'social_media_facebook': facebook,
            'social_media_instagram': instagram,
            'social_media_youtube': youtube,
            'social_media_twitter': twitter,
            'social_media_email': email,
            'contacts_whatsapp': whatsapp,
            'operating_hours_sun_start': operating_hours_sun_start,
            'operating_hours_mon_start': operating_hours_mon_start,
            'operating_hours_tue_start': operating_hours_tue_start,
            'operatinh_hourst_wed_start': operating_hours_wed_start,
            'operating_hours_thu_start': operating_hours_thu_start,
            'operating_hours_fri_start': operating_hours_fri_start,
            'operating_hours_sat_start': operating_hours_sat_start,
            'operating_hours_sun_end': operating_hours_sun_end,
            'operating_hours_mon_end': operating_hours_mon_end,
            'operating_hours_tue_end': operating_hours_tue_end,
            'operatinh_hourst_wed_end': operating_hours_wed_end,
            'operating_hours_thu_end': operating_hours_thu_end,
            'operating_hours_fri_end': operating_hours_fri_end,
            'operating_hours_sat_end': operating_hours_sat_end,
            'contact_fax': fax,
            'keywords': keywords,
            'category': categories,
            'facilities_credit_card': payment,
            'facilities_alchol': alchol,
            'branch_name': bn,
            'address': address,
            'address_region': region,
            'address_city': city,
            'address_area': area,
            'address_district': district,
            'website': website,
            'branch_rating': rating,
            'facilities_delivery': delivery,
            'facilities_banquet': banquet,
            'facilites_shisha': shisha,
            'faciliteis_minumum': minumium,
            'facilites_reservation': reservation,
            'facilities_free_wifi': wifi,
            'facilities_smoking_permited': smoking,
            'facilities_eat_out': eat_out,
            'facilities_private_parking': parking,
            'facilities_price_range': price_range,
            'facilities_kids_ares': kids_ares,
            'branch_no': branch_no}
    mainlist.append(data)

    return


def save():
    df = pd.DataFrame(mainlist)
    df.to_csv('yellowresult.csv', index=False)


if __name__ == "__main__":
    for x in fakelist:
        print(f'Scraping {x}')
        scrape(f'{x}')
        time.sleep(5)

save()
print('Scraping Complete')
