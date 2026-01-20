import requests
from bs4 import BeautifulSoup
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

uri = "mongodb+srv://stepgoit:stepgoit@cluster0.q4crmz4.mongodb.net/book?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"
client = MongoClient(uri)

db = client.book

url = 'https://quotes.toscrape.com/'
response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')

def find_born_date(author):
    link = author.parent.find("a")["href"]
    url = 'https://quotes.toscrape.com/'+link
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    born_date = soup.find('span', class_='author-born-date')
    return born_date.get_text()

def find_born_location(author):
    link = author.parent.find("a")["href"]
    url = 'https://quotes.toscrape.com/'+link
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    born_location = soup.find('span', class_='author-born-location')
    return born_location.get_text()

def find_description(author):
    link = author.parent.find("a")["href"]
    url = 'https://quotes.toscrape.com/'+link
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    description = soup.find('div', class_='author-description')
    return description.get_text().strip()

def sort_authors(authors): # Прибираємо авторів які повторюються
    sorted_authors = []
    for author in authors:
        if author not in sorted_authors:
            sorted_authors.append(author)
    return sorted_authors
authors = sort_authors(soup.find_all('small', class_='author'))

data = [] 
for i in range(0, len(authors)):
    data.append({
        "fullname": authors[i].get_text(),
        "born_date": find_born_date(authors[i]),
        "born_location": find_born_location(authors[i]),
        "description": find_description(authors[i])
    })

with open('authors.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
    f.close()

db.authors.insert_many(data)
#################################################
    
################## qoutes.json ##################
def find_tags(block_of_quote):
    tags = block_of_quote.find("div", class_="tags").find_all("a", class_="tag")
    tags_list = []
    for tag in tags:
        tags_list.append(tag.get_text())
    return tags_list

blocks_of_quote = soup.find_all('div', class_='quote')
authors = soup.find_all('small', class_='author')

data = [] 
for i in range(0, len(blocks_of_quote)):
    data.append({
        "tags": find_tags(blocks_of_quote[i]),
        "author": authors[i].get_text(),
        "quote": blocks_of_quote[i].find("span", class_="text").get_text()
    })
with open('qoutes.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

db.quotes.insert_many(data)
#################################################

result_authors = db.authors.find({})
print("------------------------------ autors.json ------------------------------")
for el in result_authors:
    print(el)

result_quotes = db.quotes.find({})
print("------------------------------ qoutes.json ------------------------------")
for el in result_quotes:
    print(el)