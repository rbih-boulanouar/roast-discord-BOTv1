import requests
from bs4 import BeautifulSoup as bf
url="http://www.indiabix.com/general-knowledge/basic-general-knowledge/005002"
r= requests.get(url)
content = r.content
#print(content)
soup = bf(content,'html.parser')
questions=soup.find_all('td', {'class': 'bix-td-qtxt'})
choices= soup.findAll("td", {"width" : "99%","id": "tdOptionDt_D_923"})
answers= soup.find_all('span', {'class': 'jq-hdnakqb mx-bold'})
#print(answers)
j=0
for i in questions:
    print("question: "+str(i.text))
    print ("\n"+"A-"+str(choices[j].text)+"\n"+"B-"+str(choices[j+1].text)+"\n"+"C-"+str(choices[j+2].text)+'\n'+"D-"+str(choices[j+3].text)+'\n')
    print("correct answer is : "+ str(answers[questions.index(i)].text)+ "\n")
    j=j+4
#print(str(questions[0].text)+"\n")
#print(str(answers[0].text)+"\n"+str(answers[1].text)+"\n"+str(answers[2].text)+"\n"+str(answers[3].text)+"\n")