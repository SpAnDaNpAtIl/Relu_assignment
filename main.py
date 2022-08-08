import requests as re
import pandas as pd
from bs4 import BeautifulSoup
import json
import time

start=time.time()
data = pd.read_csv(r'data.csv')[['id', 'Asin', 'country']]
headers = {'Host': 'www.amazon.fr', #ignore current host in this dict, host value will get changed according to region URL
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate, br',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'none',
'Sec-Fetch-User': '?1'}


res = []

#print(data.country.unique())
#for knowing the countries present in DB

for index, row in data.iterrows():
    url = 'https://www.amazon.{}/dp/{}'.format(row['country'], row['Asin'])
    headers_temp = headers.copy()
    headers_temp['Host'] = 'www.amazon.{}'.format(row['country'])
    r = re.get(url, headers=headers)
    if(r.status_code == 200):
        soup = BeautifulSoup(r.text, 'html.parser')
        #print(index, row['Asin'], row['country'])
        try:
            title = soup.find('span', {'id': 'productTitle'}).text
        except:
            continue #sometimes amazon asks for captcha, code does not have captcha bypass so it is ignored and loop is continued
        #titleOfLink = soup.title.text
        #subTitle = soup.find('span', {'id': 'productSubtitle'}).text
        imgUrl = soup.find('div', {'id': 'img-canvas'}).find('img')['src']
        try:
            indexTemp = imgUrl.find('._') #returns better image url
            if indexTemp != -1:
                imgUrl = imgUrl[:indexTemp] + '.jpg'
        except:
            None
        priceCol = soup.find('div', {'id':'tmmSwatches'})
        try:
            price = priceCol.find('span', {'class':'a-size-base a-color-price a-color-price'}).text.split(" ")[-2]
        except:
            price = priceCol.find('span', {'class':'a-color-base'}).text.split(" ")[-17]
            # website returns lots of whitespaces in this part of code so 17th element from string split has original price
        try:
            detailsCol = soup.find('div', {'id':'detailBullets_feature_div'}).find_all('span', {'class':'a-list-item'})
        except:
            continue
        details = []
        for i in detailsCol:
            detailsData = i.find_all('span')
            detailsTemp = []
            for j in detailsData:
                try:
                    detailsTemp.append(j.text.split("\n")[0])
                except:
                    detailsTemp.append(j.text)
            details.append(detailsTemp)
        if(details[-1]==[]):
            details.pop(-1)
        res.append({'Product Title': title, 'Product Image URL': imgUrl, 'Price of the Product': price, 'Product Details': details})
    elif(r.status_code == 404):
        print("{} not available".format(url))

    if((index+1)%100 == 0):
        print("Time elapsed is {}".format(time.time()-start))

jsonString = json.dumps(res)
jsonFile = open("data.json", "w")
jsonFile.write(jsonString)
jsonFile.close()

#i can create database and dump the data in it but my freeSQLdatabase account is expired and python anywhere does not allow connecting code from IDEs to their free SQL servers
#i can also create local database using sqlite3 but it is not required in this case as results have very less data and json library is sufficient for faster computations






