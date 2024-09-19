import requests
r = requests.get("https://newsdata.io/api/1/news?apikey=pub_4168327df559976a0e9986d8b5305938780a8&q=cryptocurrency")
# print(r.content)
import json
d=json.loads(r.content)
for i in d['results']:
    print(i)
    # print(i['keywords'])
    print(
        # i['title'],
        #   i['author'],
        #   i['url'],
        #   i['urlToImage'],
        #   i['description'],
          # i['content'],
          # i['publishedAt']
    )
    print("==================================================================")


