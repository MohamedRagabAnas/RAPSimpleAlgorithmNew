import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import lxml.html
import re
import sys
import csv
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
#options
ACM_BASE_URL = 'https://dl.acm.org/'
ACM_SEARCH_URL = ACM_BASE_URL + "results.cfm?within=owners.owner%3DGUIDE&srt=_score&query=persons.authors.personName:"

DBLP_BASE_URL = 'http://dblp.uni-trier.de/'
DBLP_SEARCH_URL = DBLP_BASE_URL + "search?q="


def readAuthorscsv(CSVFile):
    df=pd.read_csv(CSVFile)
    return df


def query_DBLP(authorName):

    driver = webdriver.Chrome()
    driver.get(DBLP_SEARCH_URL+""+authorName)
    html = driver.page_source
    time.sleep(1)
    elem = driver.find_element_by_tag_name("body")
    no_of_pagedowns = 50
    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
        no_of_pagedowns-=1

    html = driver.page_source    
    return BeautifulSoup(html,"lxml")

def get_co_Authors(authorNamesFile="Authors.csv"):
    
    authorsDF=readAuthorscsv(authorNamesFile)
    authors = []
    authorNames=authorsDF['Name'].tolist()

    for authName in authorNames:
        soup = query_DBLP(authName)
        authorsSoup=soup.findAll('span', attrs={"itemprop": "author"})
        co_auths=[]
        for author in authorsSoup:
            co_auths.append(author.text)
        authors.append(list(set(co_auths)))
    return authors

def query_Acm(authorNamesFile="Authors.csv"):

    authorsDF=readAuthorscsv(authorNamesFile)
    Afflst = []
    authorNames=authorsDF['Name'].tolist()
    
    for authName in authorNames:
        driver = webdriver.Chrome() # wen need to check Phantom js which is hidden and may be faster...
        driver.get(ACM_SEARCH_URL+""+authName)
        link = driver.find_element_by_link_text(authName)
        link.click()

        affHistElems=driver.find_elements_by_xpath("/html/body/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr/td/div/a")
        affHist=[]
        for aff in affHistElems:
            affHist.append(aff.text)
        Afflst.append(affHist)
        
    return authorNames,Afflst    

def main():
    names,affs=query_Acm()
    co_auths= get_co_Authors()
    print(len(names), len(affs), len(co_auths[0]),len(co_auths[1]))
    a={"Names":names,"Affiliations":affs,"Co_Authors":co_auths}
    myDF=pd.DataFrame.from_dict(a)
    myDF.transpose()
    myDF.to_csv('Auhors_Affs_coauths.csv', index=False)
    
    
if __name__ == '__main__':
        main()