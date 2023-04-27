import urllib.request
from datetime import date
import boto3
import random

s3 = boto3.client('s3')

def download_page(url,id):
  fid=urllib.request.urlopen(url)
  webpage=fid.read()
  s3.put_object(Body=webpage, Bucket='mybucket2023', Key='headlines/raw/'+id)

numero_aleatorio = random.randint(0,100000000000)
print(numero_aleatorio)
print('https://www.eltiempo.com/','contenido-'+date.today().strftime("%Y-%m-%d")+'.html')
download_page('https://www.eltiempo.com/','contenido-'+date.today().strftime("%Y-%m-%d-%s")+str(numero_aleatorio)+'.html')
download_page('https://www.elespectador.com/','contenido-'+date.today().strftime("%Y-%m-%d-%s")+str(numero_aleatorio)+'_2.html')