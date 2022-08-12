import requests
from bs4 import BeautifulSoup as bf

url = "https://parade.com/966507/parade/truth-or-dare-questions/"
request = requests.get(url)
content = request.content
soup = bf(content, "html.parser")
div = soup.find('div', {'class': 'm-detail--body'})
children = div.findChildren("p" , recursive=False)
counter=0
numbers=[0,1,2]
f1=open('Truth.txt','w')
f2=open("Dare.txt","w")
for i in children:
    if counter in numbers or counter==261:
        pass
    elif counter <= 260:
        print('truth: '+ i.text + "\n")
        f1.write('truth: '+ i.text + "\n")
    else:
        print("dare: "+ i.text + "\n")
        f2.write("dare: "+ i.text +"\n")
    counter=counter+1