
import time
import json
import Review
import JobPost2
import os.path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

myJobSearchItem = "'Deli Manager'"
myJobSearchLoc = "Nation"
with open('./all_zip.txt') as f:
    myZipCode = f.read().splitlines()
myIndeedURL = "https://www.indeed.com/jobs?q=="
pages = 3
data = []
myOverWrite = 0 # 0 for not overwrite
if myOverWrite == 0:
    myJSONcounter = 1
    while (os.path.isfile(myJobSearchItem + "_" + myJobSearchLoc+ "_"+str(myJSONcounter)+".json")):
            myJSONcounter = myJSONcounter + 1
            print myJSONcounter


def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError(
            "Unserializable object {} of type {}".format(obj, type(obj))
        )
        #json.JSONENcoder.default(self,obj)

def obj_dict(obj):
    return obj.__dict__
#enddef

def json_export(data,myDataname):
    jsonFile = open(myDataname,"w")
    jsonFile.write(json.dumps(data, indent=4, separators=(',', ': '), default=obj_dict))
    jsonFile.close()
    
def init_driver():
    driver = webdriver.Chrome(executable_path = "./chromedriver")
    driver.wait = WebDriverWait(driver, 10)
    return driver

def parse_jobposting(jobposts, data,zipcode ): 
    for Jobpost in jobposts:
        myPlace = "N/A"
        myWage = "N/A"
        myPosting = "N/A"
        myOnsite = "N/A"
        mySponsored = "N/A"
        myAdURL = "N/A"
        myCompanyURL = "N/A"
        #self, date, role, employer, place, wage, posting, onsite, sponsored, AdURL, companyURL
        try:
            myDate = Jobpost.find("span", { "class" : "date" }).getText().strip()
        except:
            myDate = "N/A"
        try:
            myRole = Jobpost.find("a", {"data-tn-element" : "jobTitle"}).getText().strip()
        except:
            myRole = "N/A"
        try:
            myEmployer = Jobpost.find("a", {"data-tn-element" : "companyName"}).getText().strip()
        except:
            try:
                myEmployer = Jobpost.find("span", {"class" : "company"}).getText().strip()
            except:
                try:
                    myEmployer = Jobpost.find("span", {"itemprop" : "name"}).getText().strip()
                except:
                    myEmployer = "N/A"
        try:
            myPlace = Jobpost.find("span", {"class":"location"}).getText().strip()        
        except:
            myPlace = "N/A"
        try:
            myWage =  Jobpost.find("nobr").getText().strip()
        except:
            try:                
                myTemp = Jobpost.find_all("div")
                for myTemp2 in myTemp:                    
                    if ("$" in myTemp2.getText().strip()) and len(str(myTemp2))<90 :
                        myWage = myTemp2.getText().strip()                       
            except:
                myWage = "N/A"
        try:
            myPosting = Jobpost.find("span", {"class":"summary"}).getText().strip()
        except:
            myPosting = "N/A"
        try:
            if (Jobpost.find("span", {"class":"sdn"})):
                mySponsored = Jobpost.find("span", {"class":"sdn"}).getText().strip()
            else:
                mySponsored = "No"
        except:
            mySponsored = "No"
        try:
            if (Jobpost.find("span", {"class":"iaLabel"})):
                myOnsite = Jobpost.find("span", {"class":"iaLabel"}).getText().strip()
            else:
                myOnsite = "No"
        except:
            myOnsite = "No"        
        try:
            myAdURL = "http://www.indeed.com"+Jobpost.find("a", {"data-tn-element":"jobTitle"})['href']           
            
        except:
            myAdURL = "N/A"
        try:
            myCompanyURL = "http://www.indeed.com"+Jobpost.find("a", {"data-tn-element":"companyName"})['href']  
        except:
            myCompanyURL = "N/A"
        myDate = myDate.replace(",","-")
        myRole = myRole.replace(",","-")
        myEmployer = myEmployer.replace(",","-")
        myPlace = myPlace.replace(",","-")
        myWage = myWage.replace(",","-")
        myPosting = myPosting.replace(",","-")
        myOnsite = myOnsite.replace(",","-")
        mySponsored = mySponsored.replace(",","-")
        r = JobPost2.JobPost2(myDate, myRole, myEmployer, myPlace, myWage, myPosting, myOnsite,mySponsored, myAdURL, myCompanyURL,zipcode)
        data.append(r)
        
    return data

def get_data(driver, myIndeedURL, startPage, endPage, data, refresh, zipcode,searchTerm,myNexturl):
    if (startPage > endPage):
        return data
    
    if refresh != False:
        if startPage == 1:
            currentURL = myIndeedURL + searchTerm+"&l="+str(zipcode)+"&start="+str((startPage-1)*10)+"&jt=fulltime"
        else:
            currentURL = myNexturl+"&jt=fulltime"
            
    #print currentURL
    time.sleep(2)
    #endif
    if (refresh):
        driver.get(currentURL)
        #print "Getting " + currentURL
    #endif
    time.sleep(2)
    HTML = driver.page_source
    soup = BeautifulSoup(HTML, "html.parser")
    myJobpostPage = soup.find_all("div", { "class" : ["row", "result"]})
    if (myJobpostPage):
        data = parse_jobposting(myJobpostPage, data, zipcode)
        #print "Page " + str(startPage) + " scraped."
        if (startPage % 10 == 0):            
            print "\nTaking a breather for a few seconds ..."
            time.sleep(2)
        if (startPage % 301 ==0):
            print "\nSo many pages ... I can't even.... what are you doin'?"
            global myJSONcounter
            json_export(data,myJobSearchItem + "_" + myJobSearchLoc+ "_"+str(myJSONcounter)+".json")
            del data[:]
            myJSONcounter = myJSONcounter + 1
        try:  
            myPagination = soup.find("div", { "class" : ["pagination"]})
            if (myPagination):
                for mySpans in myPagination.find_all("a"):
                    if ("Next" in mySpans.getText().strip()):
                        myNextURLExtract = "http://indeed.com"+mySpans['href']
                        get_data(driver, myIndeedURL, startPage + 1, endPage, data, True,zipcode, searchTerm,myNextURLExtract)
            else:
                return data
        except:
            json_export(data,myJobSearchItem + "_" + myJobSearchLoc+ "_"+str(myJSONcounter)+".json")
            myJSONcounter = myJSONcounter + 1
            print zipcode
        
    else:
        if (soup.find_all("div", {"class": ["bad_query"]})):
            return data
        else:
            print "Waiting ... page still loading or CAPTCHA input required"
            time.sleep(3)
            get_data(driver, currentURL, startPage, endPage, data, False,zipcode, searchTerm)
	#endif
    return data
#enddef


if __name__ == "__main__":
    myPreviousZip = '00010'
    driver = init_driver()
    time.sleep(3)
    print "Starting ..."
    print "\nStarting data scraping ..."
    myLoopZipCounter = 0
    myPrintCounter = 0
    for myLoopZip in  myZipCode:
        try:
            if myLoopZip != myPreviousZip:
                data = get_data(driver, myIndeedURL[:-1], 1, pages, data, True,myLoopZip,myJobSearchItem,'')
                #def get_data(driver, myIndeedURL, startPage, endPage, data, refresh, zipcode,searchTerm):
                myPreviousZip = myLoopZip
                myLoopZipCounter = myLoopZipCounter + 1
                myPrintCounter =+ 1
            if myPrintCounter > 100:
                print "Near "+myLoopZip
                myPrintCounter = 0
            if myLoopZipCounter > 100:                
                global myJSONcounter
                json_export(data,myJobSearchItem + "_" + myJobSearchLoc+ "_"+str(myJSONcounter)+".json")
                del data[:]
                myJSONcounter = myJSONcounter + 1
                myLoopZipCounter=0
        except:
                json_export(data,myJobSearchItem + "_" + myJobSearchLoc+"_"+str(myJSONcounter)+"_Before_Crash.json")
                myJSONcounter = myJSONcounter + 1
                del data[:]
                myLoopZipCounter=0
    json_export(data,myJobSearchItem + "_" + myJobSearchLoc+ "_"+str(myJSONcounter)+"_Final.json")
    
    #driver.quit()
#endif
