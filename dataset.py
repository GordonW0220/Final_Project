import requests
import sqlite3
import csv
from bs4 import BeautifulSoup
import os

conn = sqlite3.connect('Cat.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS CATS')
cur.execute('DROP TABLE IF EXISTS BREEDERS')
cur.execute(
    '''CREATE TABLE CATS(
        name text,
        length text,
        origin text,
        image_link text,
        family_friendly int,
        shedding int,
        general_health int,
        children_friendly int,
        grooming int,
        other_pets_friendly int,
        min_weight int,
        max_weight int,
        min_life_expectancy int,
        max_life_expectancy int
    )'''
)

Cats = ['Abyssinian','American Curl','American Shorthair','American Wirehair','Balinese','Bengal','Birman','Bombay','British Shorthair',
        'Burmese','Burmilla','Chartreux','Colorpoint Shorthair','Cornish Rex','Devon Rex','Egyptian Mau','European Burmese','Exotic','Havana Brown','Japanese Bobtail',
        'Khao Manee','Korat','LaPerm','Lykoi','Manx','Ocicat','Oriental','Persian','RagaMuffin','Ragdoll','Russian Blue','Scottish Fold',
        'Selkirk Rex','Siamese','Siberian','Singapura','Somali','Sphynx','Tonkinese','Turkish Angora','Turkish Van']


for cat in  Cats:
    name = cat
    api_url = 'https://api.api-ninjas.com/v1/cats?name={}'.format(name)
    response = requests.get(api_url, headers={'X-Api-Key': 'Xy6vfBYK8RO5f846Yg48RQ==S0oitV8HeV5OanXJ'})
    if response.status_code == requests.codes.ok:
        length = response.json()[0]['length']
        origin = response.json()[0]['origin']
        image_link= response.json()[0]['image_link']
        family_friendly= response.json()[0]['family_friendly']
        shedding = response.json()[0]['shedding']
        general_health= response.json()[0]['general_health']
        children_friendly = response.json()[0]['children_friendly']
        grooming = response.json()[0]['grooming']
        other_pets_friendly = response.json()[0]['other_pets_friendly']
        min_weight = response.json()[0]['min_weight']
        max_weight = response.json()[0]['max_weight']
        min_life_expectancy = response.json()[0]['min_life_expectancy']
        max_life_expectancy = response.json()[0]['max_life_expectancy']
        cat_name = response.json()[0]['name']
        cur.execute(
                # Add the SQL query to insert
                '''INSERT INTO CATS VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(cat_name,length,origin,image_link,family_friendly,shedding,general_health,children_friendly,grooming,other_pets_friendly,min_weight,max_weight,min_life_expectancy,max_life_expectancy)
            )
        conn.commit()
    else:
        print("Error:", response.status_code, response.text)
cur.close()
conn.commit()
conn.close()


curl='https://meowfacts.herokuapp.com/?count=50'
if os.path.exists("CATFACT.txt"):
  os.remove("CATFACT.txt")
f = open("CATFACTS.txt",'w')
res = requests.get(curl)
for fact in res.json()['data']:
    f.write(fact)
    f.write('\n')


conn = sqlite3.connect('Cat.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS BREEDERS')

cur.execute(
    '''CREATE TABLE BREEDERS(
        name text,
        link_page text,
        rating real,
        type text
    )'''
)



def scrap_one_page(page):
    url = "https://www.yelp.com/search?cflt=petbreeders&find_loc=Southern+California%2C+CA&sortby=rating"
    if page!=1:
        url = url + '&start=' + str(10*(page-1))
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    listings = soup.find_all('div', {'class': 'y-css-1iy1dwt'})

    breeders = []
    for listing in listings:
        try:
            name = listing.find('a', {'class': 'y-css-12ly5yx'}).text
            link = listing.find('a', {'class': 'y-css-12ly5yx'})
            link = 'https://www.yelp.com/'+ link['href']
            rating = listing.find('span', {'class': 'y-css-jf9frv'}).text
            Type = listing.find('div', {'class': 'y-css-1lvo3zq'}).text
            if name not in breeders:
                breeders.append(name)
                cur.execute(
                    '''INSERT INTO BREEDERS VALUES (?,?,?,?)''',(name,link,rating,Type)
                )
                conn.commit()
        except AttributeError:
            continue
    return None

for i in range(5):
    scrap_one_page(i+1)

cur.close()
conn.commit()
conn.close()
