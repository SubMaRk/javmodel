# -*-coding:utf8;-*-
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests as rq
from bs4 import BeautifulSoup as bs
from time import sleep as slp
from humanfriendly import format_timespan
import time
import subprocess

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.set_window_size(1024, 600)
driver.maximize_window()

# Clear screen function
clear = lambda: subprocess.call('cls||clear', shell=True)

# Start record processing time
begin_time = time.time()

# SSL Cert ciphers and Headers
rq.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

# Import link txt file
with open('link.txt','r',encoding='utf-8') as f:
    name = 1
    filename = "Javmodel_"
    for link in f:
        numline = name // 200
        if numline != 0:
            filename = 'Javmodel_' + str(numline) + '.txt'
        else:
            filename = 'Javmodel_0.txt'
        #Soup webpage
        driver.get(link)
        #html = rq.get(link, headers=headers)
        data = bs(driver.page_source, 'html.parser')
        #Get information
        file = open(filename,'a+', encoding='utf-8')
        #Get name
        engname = data.select_one(".col-xxl-8 h1").getText()
        jpname = data.select_one(".col-xxl-8 h2").getText()
        #Get BD Date
        bddate = data.select("td")[1].getText()
        # Get Blood type
        bt = data.select("td")[3].getText()
        # Get Breast
        bst = data.select("td")[5].getText()
        # Get Waist
        wt = data.select("td")[7].getText()
        # Get hips
        hp = data.select("td")[9].getText()
        # Get height
        het = data.select("td")[11].getText()
        file.write(str(name) + '\t' + engname + '\t' + jpname + '\t' + bddate + '\t' + bt + '\t' + bst + '\t' + wt + '\t' + hp + '\t' + het + '\n')
        print(engname,jpname,bddate,bt,bst,wt,hp,het)
        #Get image
        a = data.select_one(".veryclear")
        img = a['src']
        imgname = str(name) + '.jpg'
        with open(imgname,'wb') as handle:
            load = rq.get(img, stream=True)
            for block in load.iter_content(1024):
                if not block:
                    break
                handle.write(block)
        name += 1
