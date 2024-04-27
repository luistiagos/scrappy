import requests
from bs4 import BeautifulSoup
import csv, urllib
import json
import csv
import requests
import urllib
from urllib.parse import urlparse, quote
import undetected_chromedriver as uc 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def tiny_url(url):
    apiurl = "http://tinyurl.com/api-create.php?url="
    tinyurl = urllib.request.urlopen(apiurl + url).read()
    return tinyurl.decode("utf-8")

def scrap(url):
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all the links on the webpage
    links = soup.find_all('a')
    
    with open('Gamecube_Jogos.csv', 'a', newline='', encoding="utf-8") as csvfile:
        csvwriter  = csv.writer(csvfile, delimiter=';')
        
        for link in links:
            if 'rvz' in link.text:
                name = link.text.replace('.rvz', '').strip()
                size = link.parent.parent.find_all('td')[1].text
                link = url + '/' + link['href']
                try:
                    link = tiny_url(link)
                except:
                    pass
                format = 'RVZ'
                csvwriter.writerows([[name, link, size, format, url]])
                print(name + ':' + link) 
                
url = 'https://archive.org/download/rvz-gc-europe-redump/RVZ-GC-EUROPE-REDUMP/'
scrap(url)    