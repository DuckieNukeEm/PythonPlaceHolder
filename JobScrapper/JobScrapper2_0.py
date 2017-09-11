

import requests
import urllib2
import re
from time import sleep
from bs4 import BeautifulSoup
from collections uimport Counter


URL = “https://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=New+York&start=10"

def call_website(website):
    try:
        site = urllib2.urlopen(website).read() #connecting to job posting
    except:
        return
re.
    soup_obj = BeautifulSoup(site) #from gobly-gook to site info

page = requests.get(URL)


#https://jessesw.com/Data-Science-Skills/
#https://jessesw.com/Data-Science-Skills/
#https://medium.com/@msalmon00/web-scraping-job-postings-from-indeed-96bd588dcb4b
#http://blog.nycdatascience.com/student-works/web-scraping/glassdoor-web-scraping/

def get_job_title(soup):
  jobs = []
  for div in clean_soup.find_all(name='div', attrs={'class':'row'}):
      for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
          jobs.append(a['title'])
  return(jobs)

def get_date(soup):
    for div in soup.find_all(name = 'div')

def extract_company_from_result(soup):
  companies = []
  for div in soup.find_all(name='div', attrs={'class':'row'}):
    company = div.find_all(name='span', attrs={'class':'company'})
    if len(company) > 0:
        for b in company:
            companies.append(b.text.strip())
    else:
      sec_try = div.find_all(name='span', attrs={'class':'result-link-source'})
      for span in sec_try:
          companies.append(span.text.strip())

    if len(company) == 0:


    return(companies)

def get_wage(soup)


extract_company_from_result(soup)
