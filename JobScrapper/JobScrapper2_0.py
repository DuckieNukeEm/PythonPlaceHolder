

import requests
import re
from time import sleep
from bs4 import BeautifulSoup

#note
#any function starting with a 'get' pulls data from a subset of div:{class:row}
#any function starting with extract pulls directly on the return result
indeed_URL = “https://www.indeed.com/jobs?q="
job_url = 'data+scientist'
location_url = '&l'
limit_url = '&limit=50'


URL = “https://www.indeed.com/jobs?q=data+scientist&l=New+York&limit=50"
#&limit is the number of results to return, it maxes out at 50
#&l is location (either city, city state, state, zipcode, or national)
#&jt is job type (parttime, fulltime, contract,temporary,internship,commission)
#&rbc is company (follows directly location)
#&explvl is experince level (mid_level,entry_level,senior_level)

def call_website(URL):
	#hits a weburl and convert it's using BS
    try:
        site = requests.get(URL) #connecting to job posting
        soup_obj = BeautifulSoup(site.text,"html.parser") #from gobly-gook to site info
    except:
        soup_obj = False
    return(soup_obj)


#https://jessesw.com/Data-Science-Skills/
#https://medium.com/@msalmon00/web-scraping-job-postings-from-indeed-96bd588dcb4b
#http://blog.nycdatascience.com/student-works/web-scraping/glassdoor-web-scraping/

def cln_txt(soup):
	try:
		soup = soup.getText().strip()
		return(soup)
	except:
		return(soup)

def get_date_posted(div_v, defualt = "N/A"):
	# Get the date the job was posted
	try:
		out_p = div_v.find("span", { "class" : "date" })
    except:
		out_p = defualt
	
	out_p = cln_txt(out_p)
	return(out_p)

def get_wage_posted(div_v, defualt = "N/A"):
	# get the wage of the job
	try:
		out_p =  div_v.find("nobr")
		if(not out_p):
			div_two = div_v.find(name='div', attrs={'class':'sjcl'})
			out_p = div_two.find('div')
			if(not out_p):
				out_temp = div_v.find_all("div")
				for temp in out_temp:                    
                    if ("$" in clean_txt(temp) and len(str(temp))<90):
                        out_p = temp
				if(not out_p):
					out_p = default
	except:
		out_p = default
		
	out_p = cln_txt(out_p)
	return(out_p)
	
def get_role_posted(div_v, default = "N/A"):
	# Get the job title of the job
	try:
		out_p = div_v.find("a", {"data-tn-element" : "jobTitle"})
	except:
		out_p = default
		
	out_p = cln_txt(out_p)
	return(out_p)	

def get_location_posted(div_v, default = 'N/A'):
	#Get the location of the job
	try:
		out_p = div_v.find("span", {"class":"location"})
    except:
         out_p = default
    out_p = cln_txt(out_p)
    return(out_p)

def get_employer_posted(div_v, default = "N/A"):
	#get employer information
	try:
		out_p = div_v.find("a", {"data-tn-element" : "companyName"})
		if(not out_p):
			out_p = div_v.find("span", {"class" : "company"})
			if(not out_p):
				out_p = div_v.find("span", {"itemprop" : "name"})
				if(not out_p):
					out_p = default
	except:
		out_p = default
		
	out_p = cln_txt(out_p)
	return(out_p)

def get_summary_posted(div_v, defualt = 'N/A'):
	#Get Job summary
	try:
		out_p = div_v.find("span", {"class":"summary"})
	except:
		out_p = default
	out_p = cln_txt(out_p)
	return(out_p)

def get_sponsore_posted(div_v, default = 'N/A'):
	#get the spongsor(???)
	try:
		out_p = div_v.find("span",{'class':'sdn'})
    except:
		out_p = default
	out_p = cln_txt(out_p)
	return(out_p)

def get_onsite_posted(div_v, default = 'N/A'): 
	#get how people sign up for it
	try:
		out_p = div_v.find("span", {"class":"iaLabel"})
	except:
		out_p = default
	out_p = cln_txt(out_p)
	return(out_p)
	
def get_addurl_posted(div_v, default = 'N/A'):
	#get the address of the job posting
	try:
		out_p = "http://www.indeed.com"+div_v.find("a", {"data-tn-element":"jobTitle"})['href']           
	except:
		out_p = default
	return(out_p)	

def get_companyurl_posted(div_v, defualt = 'N/A'):
	try:
		out_p = "http://www.indeed.com"+div_v.find("a", {"data-tn-element":"companyName"})['href']  
	except:
		out_p = default
	return(out_p)	
			
def get_jobid_posted(div_v, default = 'N/A'):
	#gets the unique id of the job posting
	try:
		out_p = div_v.find("h2")['href']  
	except:
		out_p = default
	return(out_p)	

def get_experince_posted(div_v, default = 'N/A'):
	#find the experince people are looking for
	try:
		out_p = div_v.find("span",{'class':'experienceList'})
	except:
		out_p = default
	out_p = cln_txt(out_p)
	return(out_p)
	
def extract_jobposting_from_soup(div_v, default = 'N/A'):
	#extracts the relevant information from each job posting
	return(
	[get_jobid_posted(div_v), 					#JobID
	get_date_posted(div_v),						#PostedDate
	get_role_posted(div_v),						#Job Role
	get_wage_posted(div_v),						#wage
	get_location_posted(div_v),					#Location
	get_employer_posted(div_v),					#Employer
	get_summary_posted(div_v),					#Job Summary
	get_experince_posted(div_v),				#Job experince
	get_sponsore_posted(div_v),					#Sponsor
	get_onsite_posted(div_v),					#on site?
	get_addurl_posted(div_v),					#add URL
	get_companyurl_posted(div_v)]				#CompanyURL
	)
	
def extract_similar_jobs(soup):	
	#get similar jobs to the one we just searched for
	#for rel in  soup_obj.find_all(name ='div',attrs = {'class':'related_searches'}):
    #	for rr in  rel.find_all(name = 'li', attrs = {'class':'relatedQueries-listItem-pageFirst'}):
    #		print(rr.text)	
    job_list = ['Similar Jobs']
	lvl_1 = 'related_searches'
	lvl_2 = 'relatedQueries-listItem-pageFirst'
	try:
		for rel in  soup.find_all(name ='div',attrs = {'class':lvl_1}):
			for rr in  rel.find_all(name = 'li', attrs = {'class':lvl_2}):
				job_list.append(rr.text)
	except:
		return(job_list)
	
	return(job_list)

def extract_num_of_jobs_listing(soup):
	#pulls the number of jobs posted for the job at this location
	count_list = ['Number of Job Listings']
	try:
		n_count = soup.find(name = 'div',attrs = {'id':'searchCount'})
		n_count = cln_txt(n_count)
		if(n_count):
			n_count = n_count.split(' ')
			n_count = n_count[-1]
	except
		n_count = 0
	count_list.append(n_count)
	return(count_list)

def extract_job_salary_range(soup):
	#pulling out salary range if indeed shows it
	salary_list = ['Salary Range']
	try:
		#getting the title
		title_v = soup.find(name = 'div', attrs = {'id':'univsrch-salary-title'})
		title_v = cln_txt(title_v)
		
		#getting min
		min_v = soup.find(name = 'div', attrs = {'class':'float-left'})
		min_v = cln_txt(min_v)
		try:
			min_v = min_v.replace("Min$","")
		except:
			True
		#getting current salary
		current_salary = soup.find(name = 'p', attrs = {'id':'univsrch-salary-currentsalary'})
		current_salary = cln_txt(current_salary)
		#getting max salary
		max_v = soup.find(name = 'div', attrs = {'class':'float-right'})
		max_v = cln_txt(max_v)
		try:
			max_v = max_v.replace("Max$","")
		except:
			True
		#max number of response
		num_v = soup.find(name = 'p', attrs = {'id':'univsrch-salary-stats-para'})
		
		return([salary_list + [title_v,min_v,current_salary,max_v,num_v]])
	except:
		return

def extract_jobtype_counts(soup):
	#extracts count for full time, part time, temp, contractor, etc of the job positiosn
	out_l = ['JobType Count']
	if(soup_obj.find(name = 'div', attrs = {'id':'JOB_TYPE_rbo'})):
		for ttt in  soup_obj.find_all(name = 'div', attrs = {'id':'JOB_TYPE_rbo'}):
			for aaa in ttt.find_all("a"):
				out_l.append(aaa['title'])
	return(out_l)
	
def extract_next_links(soup, NEXT = False, start_URL = 'http://indeed.com'):
	#find what the next links will be
	next_links = []
	try:
		if(soup.find(name = 'div', attrs = {'class':['pagination']})):
			next_pages = soup.find('div',{'class':['pagination']})
			if(next_pages.find_all("a")):
				for sub_pages in next_pages.find_all("a"):
					if(NEXT and "Next" in cln_txt(sub_pages)):
						next_links.append(start_URL + sub_pages['href'])
					if(not NEXT and not "Next" in cln_txt(sub_pages) ):
						next_links.append(start_URL + sub_pages['href'])
	except:
		return(next_links)
	
	return(next_links)
			
			
			
if __name__ == "__main__":
	Zip_l = ['72758']
    print "Starting ..."
    print "\nStarting data scraping ..."
    myLoopZipCounter = 0
    myPrintCounter = 0
    page_limit = 10
    
    for Zip in Zip_l:
		current_page = 0
		URL_ID = job_url + location_url + Zip + limit_url
		URL = [indeed_URL + URL_ID]
		
		return_data = []
		while current_page < page_limit and len(URL) > 0:
			for cur_url in URL:
				#calling website
				soup_obj = call_website(cur_url)
				# is it good?
				if (soup_obj.find_all("div", {"class": ["bad_query"]})):
					break #breaking while loop
					
				if(current_page == 0 and cur_url == URL[0]):
					basic_stats = []
					basic_stats.append(extract_similar_jobs(soup_obj))
					basic_stats.append(extract_job_salary_range(soup_obj))
					basic_stats.append(extract_jobtype_counts(soup_obj))
					basic_stats.append(extract_num_of_jobs_listing(soup_obj))
					
				#breaking down soup to div
				soup_div = soup_obj.find_all('div', attrs = {'class':'row'})
				for div in soup_div:
					return_data.append(extract_jobposting_from_soup(div))
			#getting next round of URL's to use
			URL = extract_next_links(soup_obj)
			current_page = current_page + 1
