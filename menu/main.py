#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import sys
import datetime

def main():
    menu = requests.get("https://gastrogate.com/restaurang/arsenalen/page/3/")
    soup = BeautifulSoup(menu.content)
    lista = soup.find_all('td', { 'class': 'td_title'})
    day_names = [ 'Måndag', 'Tisdag', 'Onsdag', 'Torsdag', 'Fredag' ]
    day = 0
    day_inc = 0
    i = 0
    dishes = []
    lunch_week = { 0: '',
                   1: '',
                   2: '',
                   3: '',
                   4: '' }

    for row in lista:
        item = row.get_text().strip()
        dishes.append(item)
        i += 1
        if i > 4:
            lunch_week[day] = dishes
            dishes = []
            i = 0
            day +=1
    today = datetime.datetime.today().weekday()
    for j in range(0, len(lunch_week[today])):
            output = lunch_week[today][j].encode('utf-8')
            print output

if __name__ == '__main__':
    main()

