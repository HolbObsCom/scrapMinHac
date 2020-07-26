from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import requests
import re


def scrapper():
    ''' Web Driver'''
    driver = webdriver.Firefox()
    url = 'https://www.minhacienda.gov.co/webcenter/portal/EntOrdenNacional/pages_presupuestogralnacion/presemerCOVID19'
    listaAux = []
    dictPDFs = dict()
    ''' Open the url in the browser''' 
    driver.get(url)
    ''' Find the tags to pagination '''
    tags = driver.find_elements_by_css_selector("a.x1cn")
    try:
        for i in range(len(tags)+1):
            soup = BeautifulSoup(driver.page_source, 'html5lib')
            ''' Find the tags url to dowload PDF with regex '''
            findTags = soup.find_all('a', {'id': re.compile('^(T:dclay).*(pad1:)(\d*).*(goLink1)$')})
            for num,link in enumerate(findTags):
                ''' Put into dictionary a title and link as a key a value '''
                dictPDFs[str(link.get('title'))] = str(link.get('href'))
            ''' Find the next page icon for click and change the page '''
            target = driver.find_element_by_css_selector("a.x1cq")
            ''' Scroll down to target '''
            driver.execute_script("arguments[0].scrollIntoView();", target)
            ''' Click in next page '''
            target.click()
        ''' Close the Browser '''
        driver.close()
    except:
        print("Error")
    return dictPDFs

def printdict(dictPDFs):
    for key, val  in dictPDFs.items():
        print(f'title: {key}')  
        print(f'link: {val}')

def gotPDFs(dictPDFs):
    ''' Forget the Problem with SSL in next three lines'''
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    for key,url in dictPDFs.items():
        ''' Do the request '''
        response = urlopen(url, context=ctx)
        try:
            ''' Create or overwrite the PDF '''
            with open(f'{key}', 'wb+') as fd:
                while True:
                    chunk = response.read(2000)
                    if not chunk:
                        break
                    ''' Write into the PDF until chunk exits '''
                    fd.write(chunk)
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
    gotPDFs(pdfs)
    checkWithTxt(pdfs)