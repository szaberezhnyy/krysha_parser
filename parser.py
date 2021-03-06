import sys
from bs4 import BeautifulSoup
import re
import requests


class Flat:
    def __init__ (self):
        
        self.link = None    #str
        self.city = None    #str
        self.dist = None    #str
        self.mcr_dist = None    #str
        self.address = None    #str
        self.floor = None    #int
        self.max_floor = None    #int
        self.room_number = None    #int
        self.square = None    #float
        self.price = None    #float
        self.descr = None    #str
        self.update_date = None    #str


def parse_fst_page(url):
    r=requests.get(url)
    soup=BeautifulSoup(r.content, 'lxml')
    pages = []
    for page in soup.find_all('a'):
        a = page.get('data-page')
        if a:
            pages.append(a)
    if pages:
        max_page=int(pages[-2])
    else:
        max_page=1
    all_flats = soup.find_all('div', {'class':'a-description'})
    parsed_flats = []
    for flats in all_flats:
        f = Flat()
        f.link = flats.find_all("a", {'class':'link'})[0].get('href')
        title = (flats.find_all("a", {'class':'link'})[0].get('title')).split('-комнатная квартира, ',1)
        f.room_number = int( title[0])
        addr = title[1].split(',')
        if 'мкр' in addr[0].lower():
            f.mcr_dist = addr[0]
        f.address = addr[-1].strip()
        f.price = float(flats.find_all('span', {'class':'a-price-value'})[0].text.replace('\u20b8','').replace('млн', '').replace('~','').strip())
        city_square = (flats.find_all('div', {'class':'a-subtitle'})[0].text).split(',')
        f.city = city_square[0].strip()
        for info in city_square:
            if 'р-н' in info:
                f.dist = info.strip()
            if 'этаж' in info:
                try:
                    f.floor = int(info.split()[0])
                except:
                    f.floor = None
                try:
                    f.max_floor =int(info.split()[-1])
                except:
                    f.max_floor = None
        f.square = float(re.findall(r'\d+', city_square[-1])[0])
        f.descr = flats.find_all('div', {'class':'a-text'})[0].text.strip()
        f.update_date = flats.find_all("span", {'class':'a-date status-item'})[0].text.strip()
        parsed_flats.append(f)
    return  parsed_flats, max_page


def parse_page(url):
    r = requests.get(url)
    soup=BeautifulSoup(r.content, 'lxml')
    all_flats = soup.find_all('div', {'class':'a-description'})
    parsed_flats = []
    for flats in all_flats:
        f = Flat()
        f.link = flats.find_all("a", {'class':'link'})[0].get('href')
        title = (flats.find_all("a", {'class':'link'})[0].get('title')).split('-комнатная квартира, ',1)
        f.room_number = int( title[0])
        addr = title[1].split(',')
        if 'мкр' in addr[0].lower():
            f.mcr_dist = addr[0]
        f.address = addr[-1]
        f.price = float(flats.find_all('span', {'class':'a-price-value'})[0].text.replace('\u20b8','').replace('млн', '').replace('~','').strip())
        city_square = (flats.find_all('div', {'class':'a-subtitle'})[0].text).split(',')
        f.city = city_square[0].strip()
        for info in city_square:
            if 'р-н' in info:
                f.dist = info.strip()
            if 'этаж' in info:
                try:
                    f.floor = int(info.split()[0])
                except:
                    f.floor = None
                try:
                    f.max_floor =int(info.split()[-1])
                except:
                    f.max_floor = None
        f.square = float(re.findall(r'\d+', city_square[-1])[0])
        f.descr = flats.find_all('div', {'class':'a-text'})[0].text.strip()
        f.update_date = flats.find_all("span", {'class':'a-date status-item'})[0].text.strip()
        parsed_flats.append(f)
    return parsed_flats


def parse_krysha(url):
    """
    This function will receive a form params
    and send requests to krysha.kz and parse site results
    """
    pf, max_page = parse_fst_page(url)
    proceed = ''
    while proceed != 'y' and proceed != 'n':
        print (max_page)
        proceed = input('парсить все эти страницы? y/n ')
    if proceed == 'y':
        count = 1
        while count < max_page:
            count += 1
            url_page = url + 'page=' + str(count)
            pf += parse_page(url_page)
    return pf, max_page


def combine_url(**kwargs):
    '''
    (price_from, price_to, square_from, square_to, floor_from,
        floor_to, year_from, year_to, room_num, house_type, region, from_owner,
        from_agency, photo)
    This function combines all output from html form to a single url
    '''
    url = 'https://krisha.kz/prodazha/kvartiry/'

    n = '&'

    

    if kwargs['region']:
        url += kwargs['region'] + '/'

    url += '?'
    if kwargs['price_from']:
        url += n + 'das[price][from]=' + kwargs['price_from']

    if kwargs['price_to']:
        url += n + 'das[price][to]=' + kwargs['price_to']

    if kwargs['square_from']:
        url += n + 'das[live.square][from]=' + kwargs['square_from']

    if kwargs['square_to']:
        url += n + 'das[live.square][to]=' + kwargs['square_to']

    if kwargs['floor_from']:
        url += n + 'das[flat.floor][from]=' + kwargs['floor_from']

    if kwargs['floor_to']:
        url += n + 'das[flat.floor][to]=' + kwargs['floor_to']

    if kwargs['year_from']:
        url += n + 'das[house.year][from]=' + kwargs['year_from']

    if kwargs['year_to']:
        url += n + 'das[house.year][to]=' + kwargs['year_to']

    for room in kwargs['room_num']:
        url += n + 'das[live.rooms][]='+room

    building_type = {'Кирпичный': '1', 'Панельный':'2', 'Монолитный':'3',
    'Каркасно-камышитовый': '4', 'Иное':'5'}
    for types in kwargs['house_type']:
        url += n + 'das[flat.building][]='+building_type[types]

    if kwargs['from_owner']:
        url += n + 'das[who]=1'

    if kwargs['from_agency']:
        url += n + 'das[checked]=1'

    if kwargs['photo']:
        url += n + 'das[_sys.hasphoto]=1'
    return url

