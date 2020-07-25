from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import requests
import re


def scrapper():
    driver = webdriver.Firefox()
    url = 'https://www.minhacienda.gov.co/webcenter/portal/EntOrdenNacional/pages_presupuestogralnacion/presemerCOVID19'
    listaAux = []
    dictPDFs = dict() 
    driver.get(url)
    tags = driver.find_elements_by_css_selector("a.x1cn")
    try:
        for i in range(len(tags)+1):
            soup = BeautifulSoup(driver.page_source, 'html5lib')
            findTags = soup.find_all('a', {'id': re.compile('^(T:dclay).*(pad1:)(\d*).*(goLink1)$')})
            for num,link in enumerate(findTags):
                #listaPDFs.append(str(link.get('href')))
                dictPDFs[str(link.get('title'))] = str(link.get('href'))
            target = driver.find_element_by_css_selector("a.x1cq")
            driver.execute_script("arguments[0].scrollIntoView();", target)
            target.click()
        driver.close()
    except:
        print("Error")
    return dictPDFs
def printdict(dictPDFs):
    for key, val  in dictPDFs.items():
        print(f'title: {key}')  
        print(f'link: {val}')
def gotPDFs(dictPDFs):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'Referer' : 'https://www.google.com',
    'Accept' : 'text/javascript; charset=UTF-8'
    }
    for key,url in dictPDFs.items():
        response = urlopen(url, context=ctx)
        try:
            with open(f'{key}', 'wb+') as fd:
                while True:
                    chunk = response.read(2000)
                    if not chunk:
                        break
                    f.write(chunk)
        except:
            print(f'NOT FOUND: {key}')
            continue
def checkWithTxt(dictPDFs):
    for title, url in dictPDFs.items():
        with open('decretos.txt', 'a+') as fd:
            fd.write(f'{title}: {url}\n')

if __name__ == "__main__":
    pdfs = dict()
    pdfs = scrapper()
    printdict(pdfs)
    #gotPDFs(pdfs)
    checkWithTxt(pdfs)