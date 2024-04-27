import requests
from bs4 import BeautifulSoup
import csv, urllib

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
    
    with open('MAME.csv', 'a', newline='', encoding="utf-8") as csvfile:
        csvwriter  = csv.writer(csvfile, delimiter=';')
        
        for link in links:
            if '.zip' in link.text and (',Pt' in link.text or 'Pt,' in link.text):
                name = link.text.replace('.zip', '').strip()
                link = url + link['href']
                link = tiny_url(link)
                csvwriter.writerows([[name, link]])
                print(name + ':' + link) 
                
url = 'https://myrient.erista.me/files/Redump/Microsoft%20-%20Xbox%20360/'
scrap(url)     