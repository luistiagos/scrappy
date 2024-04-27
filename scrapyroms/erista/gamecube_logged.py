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

def scrap():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    #options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=options)
    driver.get("https://www.google.com") 
    # Parse the HTML content
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    url = driver.current_url
    # Find all the links on the webpage
    links = soup.find_all('a')
    
    with open('gamecube_jogos.csv', 'a', newline='', encoding="utf-8") as csvfile:
        csvwriter  = csv.writer(csvfile, delimiter=';')
        
        for link in links:
            if 'rvz' in link.text:
                name = link.text.replace('.rvz', '').strip()
                size = link.parent.parent.find_all('td')[1].text
                link = 'https://archive.org/download/rvz-gc-usa-redump/RVZ-GC-USA-REDUMP/' + link['href']
                try:
                    link = tiny_url(link)
                except:
                    pass
                format = 'rvz'
                csvwriter.writerows([[name, link, size, format, url]])
                print(name + ':' + link) 
                
scrap()    