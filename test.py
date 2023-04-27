import json
import urllib.request
import boto3
import socket
from urllib.parse import urlparse
from datetime import datetime

name_file = ""


def f(event, context):
    url = "https://www.eltiempo.com/"
    html = urllib.request.urlopen(url).read().decode('utf-8')
    s3 = boto3.client('s3')
    s3.put_object(Bucket="aws-glue-assets-325503392442-us-east-1", Key="Folder_Test/"+datetime.strftime(datetime.now(), '%Y_%m_%d %H:%M;%S')+".html", Body=html)
    return {
        'statusCode': 200,
        'body': json.dumps('Función Lambda ejecutada exitosamente')
    }


def download_html(mocker):
    req = urllib.request.Request("https://www.eltiempo.com/")
    response = urllib.request.urlopen(req)
    print("Edwin"+response.getcode())
    print("Edwin_2", response.read())
    return response.read()


def validate_code(url):
    return urllib.request.urlopen(url).getcode()


def validate_hostbyname(url):
    parsed_url = urlparse(url)
    try:
        socket.gethostbyname(parsed_url.netloc)
        return True
    except socket.error:
        return False
