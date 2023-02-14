import json
from lxml import html
import requests

with open("step1.json", "r") as f:
    hrefs = json.load(f)


hrefs_type_1 = []
hrefs_type_2 = []
for i in hrefs:
    if i[-3:] == "htm" or i[-3:] == "tm/":
        hrefs_type_2.append(i)
    else:
        hrefs_type_1.append(i)


result = []

headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
for i in hrefs_type_1:
    url = "https://lenta.ru"+i
    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)
    text = dom.xpath("//h1/span/text()")[0]
    i = i.split("/")
    data = i[2]+"/"+i[3]+"/"+i[4]
    result.append({"Текст": text, "Сылка": url, "Дата": data, "Издательство":"Лента"})

for i in hrefs_type_2:
    url = i
    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)
    text = dom.xpath("//h1//text()")[0]
    data = i.split(".")[-2][-10:]
    result.append({"Текст": text, "Сылка": url, "Дата": data, "Издательство":"Мослента"})

with open("result.json", "w") as f:
    json.dump(result, f)
