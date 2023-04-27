from test import download_html,validate_code,validate_hostbyname
from unittest.mock import patch

@patch('urllib.request.urlopen')
def test_scraping(mocker):
    cad = '<html><head><title>Cafeteros se le rebelan a Gustavo Petro y eligen a nuevo gerente: Germán Bahamón</title></head><body><p>Este es un ejemplo de HTML</p></body></html>'
    mocker.return_value.read.return_value = cad.encode('utf-8')
    html = download_html("https://www.eltiempo.com/")
    assert html == cad.encode('utf-8')


def test_validate_code():
    assert validate_code("https://www.eltiempo.com/") in [200,201,202]


def test_validate_hostbyname():
    assert validate_hostbyname("https://www.eltiempo.com/") == True