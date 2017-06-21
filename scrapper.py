#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request as ulib
from bs4 import BeautifulSoup
from datetime import datetime

### CONSTANTES ###
URL = "https://fr.investing.com/economic-calendar/"
PAYS = ['USD', 'EUR']
#Requete HTTP et recuperation de la page
#User agent Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36

def firstWithoutSpaces(string):
    for i in range(len(string)):
        if string[i] != ' ':
            return string[i:]

def scrapper():
    req      = ulib.Request(URL, headers = {'User-agent' : 'Mozilla/5.0'})
    response = ulib.urlopen(req)
    the_page = response.read()

    # Parsing de la page récupérée : table>tr>td.class
    soup        = BeautifulSoup(the_page, 'html.parser')
    infos       = soup.findAll("td", { "class" : "event" })
    pays        = soup.findAll("td", { "class" : "flagCur" })
    jour        = soup.findAll("td", {"class" : "theDay"})
    heures      = soup.findAll("td", { "class" : "time" })
    actuelles   = soup.findAll("td", { "class" : "act" })
    previsions  = soup.findAll("td", { "class" : "fore" })
    precedentes = soup.findAll("td", { "class" : "prev" })

    items = []

    #Stockage des données dans un tableau d'objets

    for i in range(len(infos)):
        try:
            country = pays[i].text.replace('\xa0', '').replace(' ', '')
            if country in PAYS:
                items += [{
                    #Stockage et formattage des chaines
                    "info":      firstWithoutSpaces(infos[i].a.text.replace('\n', '').replace('\t', '').replace('\r', '')),
                    "pays":      country,
                    "heure":     datetime.strptime(str(datetime.now().day) + '/' + str(datetime.now().month) + '/' + str(datetime.now().year) + ' ' + heures[i].text, '%d/%m/%Y %H:%M'),
                    #Si on a \xa0 => Pas de données on met True à la place de l'info inutile pour mieux la traiter
                    "actuel":    True if (actuelles[i].text == '\xa0') else actuelles[i].text,
                    "prevision": True if (previsions[i].text == '\xa0') else previsions[i].text,
                    "precedent": True if (precedentes[i].text == '\xa0') else precedentes[i].text
                }]

        except:
            #Il faudra gerer les exceptions
            print('lol')

    return items

print(scrapper())
