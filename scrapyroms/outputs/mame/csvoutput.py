import json
import csv
import requests
import urllib
from urllib.parse import urlparse, quote

data = {}

def sanitize_url(url):
    parsed_url = urlparse(url)
    # Remove control characters from the path and query
    sanitized_path = quote(''.join(char for char in parsed_url.path if 31 < ord(char) < 127))
    sanitized_query = quote(''.join(char for char in parsed_url.query if 31 < ord(char) < 127))
    
    # Reconstruct the sanitized URL
    sanitized_url = parsed_url._replace(path=sanitized_path, query=sanitized_query).geturl()
    sanitized_url = sanitized_url.replace(' ', '20%')
    return sanitized_url

def tiny_url(url):
    url = sanitize_url(url)
    apiurl = "http://tinyurl.com/api-create.php?url="
    tinyurl = urllib.request.urlopen(apiurl + url).read()
    return tinyurl.decode("utf-8")

def convert_to_original_size(size_kb):
    if size_kb >= 1024 * 1024 * 1024:
        size = size_kb / (1024 * 1024 * 1024)
        return f"{size:.2f} GiB"
    elif size_kb >= 1024 * 1024:
        size = size_kb / (1024 * 1024)
        return f"{size:.2f} MiB"
    elif size_kb >= 1024:
        size = size_kb / 1024
        return f"{size:.2f} KB"
    else:
        return f"{size_kb:.2f} Bytes"
    
def load_names():
    with open('mame', "r") as file:
        for line in file:
            data[line[6:37].strip()] = line[38:157].strip()

def scrap(name, filename):
    # Fetch JSON data from the REST service
    base = name
    json_url = 'https://archive.org/details/' + base + '?output=json'  # Replace with the actual REST service URL
    response = requests.get(json_url)
    json_data = response.json()
    type = 'zip'

    # Extract the "files" dictionary from the JSON data
    files_data = json_data["files"]

    # Write CSV data to a file
    csv_file = filename  # Specify the CSV file name
    with open(csv_file, 'a', newline='', encoding="utf-8") as f:
        csv_writer = csv.writer(f,  delimiter=';')
        #csv_writer.writerow(['name','link','size','format','origem','type'])

        for key, values in files_data.items():
            name = key.strip("/")
            if 'zip' in name:
                origem = 'https://archive.org/download/' + base
                size = convert_to_original_size(float(values["size"]))
                link = origem + "/" + name
                #try:
                #    link = tiny_url(link)
                #except Exception as err:
                #    print(err)
                name = name.replace('.zip', '').strip()
                try:
                    name = data[name]
                except:
                    pass
                format_type = values["format"]
                csv_writer.writerow([name, link, size, format_type, origem, type])
                
load_names()                

names = ['mame-chds-roms-extras-complete']
for name in names:
    print(name)
    try:
        scrap(name, 'MAME.csv')
    except:
        print('Error - ' + name)
        
        
        
        
        