import requests
from bs4 import BeautifulSoup as bf 
import sqlite3
flagsl=[]
namesl=[]

# table="""
# CREATE TABLE FLAGS (
#             NAME VARCHAR(255) NOT NULL,
#             LINK CHAR(255) NOT NULL)


# """


url='https://www.worldometers.info/geography/flags-of-the-world/'
r=requests.get(url)
content = r.content
soup = bf(content,'html.parser')
#print(content)
flag = soup.find_all('div', {'class': 'col-md-4'})

div_list=soup.select('.col-md-4 div:first-child')
for div in div_list:
    try:
        name=div.select_one('div div').text
        flag="https://www.worldometers.info"+str(div.select_one('div a')['href'])
        #print(flag)
        #print(name)
        flagsl.append(flag)
        namesl.append(name)
        
    except:
        pass
print(len(flagsl))
print(len(namesl))
conn = sqlite3.connect('flags.db')
cursor_obj = conn.cursor()
for i in range (0,len(flagsl)):
    quary= 'INSERT INTO FLAGS (NAME , LINK) VALUES ("'+namesl[i]+'","'+flagsl[i]+'");'
    print(quary)
    cursor_obj.execute(quary)

# quary= "insert into flags (name , link) values ("+name+","+flag+")"
# cursor_obj.execute(quary)
# conn.close()