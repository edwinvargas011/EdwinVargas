from bs4 import BeautifulSoup
import pandas as pd
import requests
import boto3
from datetime import date

my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.google.com/',
    'Connection': 'keep-alive'}

#doc_html=dict(map(lambda domain,idx: ("Page_"+str(idx),html.unescape(requests.get(url=domain,headers=my_headers,timeout=15).text)),["https://www.eltiempo.com/","https://www.elespectador.com/"],[1,2]))

web_html= BeautifulSoup(requests.get("https://www.eltiempo.com/").content,'html.parser')
p1=[]   
for un_grid in web_html.select('.content_grid:not([class*=" "])'):
  for tag in un_grid.find_all("article"): 
    if not(tag.find('h2',class_="title-container")is None and tag.find('h3',class_="title-container") is None):
      for tag2 in tag.find_all(['h2','h3'],class_="title-container"):
        for tag3 in tag2.find_all('a',class_="title page-link"):
            if isinstance(tag3, str):
              continue
            p1.append({"Titular":tag3.text,"Section":tag['data-seccion'],"Category":tag['data-category'],"Enlace":"https://www.eltiempo.com"+str(tag3['href'])})
            break;

p2=[]
web_html_2=BeautifulSoup(requests.get("https://www.elespectador.com/").content,"html.parser")
web_html_2.find_all('div',class_='pure-u-1')
for tag,clase in [('div','Layout-Container')]:  
  for tag_class in web_html_2.find_all(tag,class_=clase):
        for card in tag_class.find_all('div',class_='Card-Container'):
          try:
            title=card.find(class_="Card-Title Title Title").find("a").text
          except:
            title=None
          try:
            section=card.find(class_="Card-Section Section").find("a").text
          except:
            section=None
          try:
            url=card.find(class_="Card-Title Title Title").find("a")['href']
          except:
            url=None
          p2.append({"Titular":title,"Section":section,"Enlace":"https://www.elespectador.com"+str(url)})

df=[pd.DataFrame.from_records(info_periodico) for info_periodico in[p1,p2]]
s3 = boto3.client('s3')
i=0
for elem,name in zip(sorted(s3.list_objects_v2(Bucket='mybucket2023',Prefix='headlines/raw/')['Contents'], key=lambda k: k['LastModified'], reverse=False)[-2:],['ElTiempo','ElEspectador']):
    response=s3.get_object(Bucket="mybucket2023",Key=elem['Key'])
    html = response['Body'].read().decode('utf-8')
    ##Generar cada carpeta segun su nombre,año,mes
    texto = date.today().strftime("-%Y-%m-%d")
    final_text = ""
    pos = 0
    for y in ['/year=', '/month=', '/day=']:
        next_pos = texto.find('-', pos + 1)
        if next_pos == -1:
            next_pos = len(texto)
        texto_modificado = texto[pos:next_pos].replace('-', y)
        final_text = final_text + texto_modificado
        pos = next_pos
    s3.put_object(Body=df[i].to_csv(),Bucket="mybucket2023",Key="headlines/final/periodico="+name+final_text+'/'+'contenido_'+date.today().strftime("%Y-%m-%d")+'.csv')
    i=i+1
