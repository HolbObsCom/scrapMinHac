from ClassScrapper import baseScrapper
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
from collections import defaultdict

class PortalTrans(baseScrapper):
    url='http://www.pte.gov.co/WebsitePTE/AQuienSeContrataSectorCovid'
    # check this two diferent endpoints
    #url='http://www.pte.gov.co/WebsitePTE/AQuienSeContrataSectorPandemia'

    def scrapper(self, entitiesdict=defaultdict(list)):
        regexTaglinks = re.compile('^A(q|Q).*(s|S).*(C|c).*(SectorEntidad)')
        firstIteration = False
        regexTagPagination = re.compile(r"^(javascript:)(.+)'(Page\$)(\d*)'\)$")
        if len(entitiesdict.keys()) == 0:
            urls = 1
            firstIteration = True
        else:
            listurl = list(entitiesdict.values())
            urls = len(listurl)
        for indexurldriver in range(urls):
            driver = webdriver.Firefox()
            if len(entitiesdict.keys()) == 0:
                driver.get(self.url)
            else:
                print(listurl[indexurldriver][0])
                driver.get(listurl[indexurldriver][0])
            soup = BeautifulSoup(driver.page_source,'html5lib')
            paginationtags = soup.find_all('a', {'href': regexTagPagination})
            for index in range(len(paginationtags)+1):
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source,'html5lib')
                pages = driver.find_elements_by_xpath('//tr[@class="pagination-ys"]/td/table/tbody/tr/td/a')
                Entitieslinks = soup.find_all('a', {'href': regexTaglinks})
                for entitie in Entitieslinks:
                    if firstIteration is True:
                        entitiesdict[entitie.contents[0]].append('http://www.pte.gov.co/WebsitePTE/' + entitie.get('href'))
                    else:
                        entitiesdict[list(entitiesdict.keys())[indexurldriver]].append('http://www.pte.gov.co/WebsitePTE/' + entitie.get('href'))
                if len(pages) > index:
                    driver.execute_script("arguments[0].scrollIntoView();", pages[index])
                    driver.execute_script("arguments[0].click();", pages[index])
            driver.close()
        return entitiesdict

if __name__ == '__main__':
    scrap = PortalTrans()
    dictenti = scrap.scrapper()
    scrap.printdict(dictenti)
    scrap.checkWithTxt(dictenti)
    dictenti2= scrap.scrapper(dictenti)
    scrap.printdict(dictenti2)
    scrap.checkWithTxt(dictenti2)