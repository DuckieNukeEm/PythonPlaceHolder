

import requests
import sqlite3
import csv
import re
import os
from datetime import datetime, timedelta
from time import sleep
from bs4 import BeautifulSoup

#note
#any function starting with a 'get' pulls data from a subset of div:{class:row}
#any function starting with extract pulls directly on the return result
indeed_URL = 'https://www.indeed.com/jobs?q='
job_url = "title:warehouse company:amazon" #''cashier'
location_url = '&l='
limit_num = 50
jobtype_url = None #''&jt=parttime'
filter_url = None #'&filter=0'
sort_url = '&sort=date'


def create_url(base_url = 'https://www.indeed.com/jobs?q=', job = None, location = None, limit = 50, jobtype = None, sort=None, filter = None, start = None, explvl = None, return_key = False):
	# URL = 'https://www.indeed.com/jobs?q=data+scientist&l=New+York&limit=50'
	# &limit is the number of results to return, it maxes out at 50
	# &l is location (either city, city state, state, zipcode, or national)
	# &jt is job type (parttime, fulltime, contract,temporary,internship,commission)
	# &rbc is company (follows directly location)
	# &explvl is experince level (mid_level,entry_level,senior_level)
	# &filter do we want to hide similar results?
	# &sort sorts by date or relevance
	url_key = ['','','','','','','','']
	if(job != None):
		base_url = base_url + job
		url_key[0] = job
	if(location != None):
		base_url = base_url + '&l=' + location
		url_key[1] = location
	if(limit != None):
		if(limit not in [10,20,30,40,50]):
			limit = 50
		base_url = base_url + '&limite' + str(limit)
		url_key[2] = str(limit)
	if(jobtype != None):
		if(jobtype in ['parttime','fulltime','contract','temporary','internship','commission']):
			base_url = base_url + '&jt=' + jobtype
			url_key[3] = jobtype
		else:
			print('JobType isnt in the standard list of job types')
	if(sort != None and sort in ['date','relevance']):
		base_url = base_url + '&sort=' + sort
		url_key[4] = sort
	if(filter != None and filter in [0,1]):
		base_url = base_url + '&filter=' + str(filter)
		url_key[5] = str(filter)
	if(explvl != None and explvl in ['mid_level','entry_level','senior_level']):
		base_url = base_url + '&explvl=' + explvl
		url_key[6] = explvl
	if(start != None):
		base_url = base_url + '&start=' + str(start)
		url_key[7] = str(start)

	if(return_key):
		return(([base_url], '-'.join(url_key)))
	else:
		return([base_url])

#URL = 'https://www.indeed.com/jobs?q=data+scientist&l=New+York&limit=50'
#&limit is the number of results to return, it maxes out at 50
#&l is location (either city, city state, state, zipcode, or national)
#&jt is job type (parttime, fulltime, contract,temporary,internship,commission)
#&rbc is company (follows directly location)
#&explvl is experince level (mid_level,entry_level,senior_level)
#&filter do we want to hide similar results?
#&sort sorts by date or relevance

def call_website(URL, counter = 0):
	#hits a weburl and convert it's using BS
	if(counter == 2):
		return(False)
	try:
		site = requests.get(URL)
		soup_obj = BeautifulSoup(site.text,"html.parser") #from gobly-gook to site info
		if(soup_obj.find(name = 'div', attrs = {'class':'bad_query'})):
			soup_obj = False

	#catching all the errors, and allowing a few for retries
	except requests.Timeout:
		sleep(5)
		soup_obj = call_website(URL, counter + 1)
	except requests.RequestException:
		soup_obj = False
	except requests.HTTPError:
		soup_obj = False
	except requests.ConnectionError:
		soup_obj = False
	except requests.URLRequired:
		soup_obj = False
	except requests.TooManyRedirects:
		soup_obj = False

	return(soup_obj)

#http://blog.nycdatascience.com/student-works/web-scraping/glassdoor-web-scraping/

def cln_txt(soup):
	try:
		soup = soup.getText().strip()
		return(soup)
	except:
		return(soup)

def get_date_posted(div_v, default = None):
	# Get the date the job was posted
	try:
		out_p = div_v.find("span", { "class" : "date" })
	except:
		out_p = default

	out_p = cln_txt(out_p)
	return(out_p)

def get_wage_posted(div_v, default = None):
	# get the wage of the job
	try:
		out_p =  div_v.find("nobr")
		if(out_p == None or '$' not in cln_txt(out_p)):
			div_two = div_v.find(name='div', attrs={'class':'sjcl'})
			if(div_two != None):
				out_p = div_two.find('div')
			else:
				out_temp = div_v.find_all(["div","span"])
				for temp in out_temp:
					if ("$" in clean_txt(temp) and len(str(temp))<90):
						out_p = temp
				if(not out_p):
					out_p = default
		else:
			out_p = out_p.text
	except:
		out_p = default

	out_p = cln_txt(out_p)
	return(out_p)

def get_role_posted(div_v, default = None):
	# Get the job title of the job
	try:
		out_p = div_v.find("a", {"data-tn-element" : "jobTitle"})
	except:
		out_p = default

	out_p = cln_txt(out_p)
	return(out_p)

def get_location_posted(div_v, default = None):
	#Get the location of the job
	try:
		out_p = div_v.find("span", {"class":"location"})
	except:
		out_p = default
	out_p = cln_txt(out_p)
	return(out_p)

def get_employer_posted(div_v, default = None):
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

def get_summary_posted(div_v, default = None):
	#Get Job summary
	try:
		out_p = div_v.find("span", {"class":"summary"})
	except:
		out_p = default
	out_p = cln_txt(out_p)
	return(out_p)

def get_sponsore_posted(div_v, default =  'Yes'):
	out_p = 'Yes'
	try:
		for temp in div_v.find_all('a'):
			try:
				if('jobmap' in temp['onclick']):
					out_p = 'No'
			except:
				next
	except:
		out_p = default
	return(out_p)

def get_onsite_posted(div_v, default = None):
	#get how people sign up for it
	try:
		out_p = div_v.find("span", {"class":"iaLabel"})
	except:
		out_p = default
	out_p = cln_txt(out_p)
	return(out_p)

def get_addurl_posted(div_v, default = None):
	#get the address of the job posting
	try:
		out_p = "http://www.indeed.com"+div_v.find("a", {"data-tn-element":"jobTitle"})['href']
	except:
		out_p = default
	return(out_p)

def get_companyurl_posted(div_v, default = None):
	try:
		out_p = "http://www.indeed.com"+div_v.find("a", {"data-tn-element":"companyName"})['href']
	except:
		out_p = default
	return(out_p)

def get_jobid_posted(div_v, default = None):
	#gets the unique id of the job posting
	out_p = default
	try:
		#if(div_v.find_all('h2')):
		#	for temp in div_v.find_all('h2'):
		#		if(temp['id']):
		#			out_p = temp['id']
	except:
		out_p = default

	return(out_p)

def get_experince_posted(div_v, default = None):
	#find the experince people are looking for
	try:
		out_p = div_v.find("span",{'class':'experienceList'})
	except:
		out_p = default
	out_p = cln_txt(out_p)
	return(out_p)

def extract_jobposting_from_soup(div_v, default = 'N/A'):
	#extracts the relevant information from each job posting
	job =[get_jobid_posted(div_v),				#JobID
	find_date_posted(get_date_posted(div_v)),	#PostedDate
	get_role_posted(div_v),						#Job Role
	get_wage_posted(div_v),						#wage
	get_location_posted(div_v),					#Location
	get_employer_posted(div_v),					#Employer
	get_summary_posted(div_v),					#Job Summary
	get_experince_posted(div_v),				#Job experince
	get_sponsore_posted(div_v),					#Sponsor
	get_onsite_posted(div_v),					#on site?
	#get_addurl_posted(div_v),					#add URL
	get_companyurl_posted(div_v)]				#CompanyURL

	job = check_for_wages(job)
	return(job)

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
	except:
		n_count = 0
	count_list.append(n_count)
	return(count_list)

def extract_salary_groups(soup):
	#pulls salary counts by groupings
	salary_group = ['Salary Group']
	if(soup.find(name = 'div', attrs = {'id':'SALARY_rbo'})):
		for temp1 in soup.find_all(name = 'div', attrs = {'id':'SALARY_rbo'}):
			for temp2 in temp1.find_all('a'):
				salary_group.append(temp2['title'])
	return(salary_group)

def extract_job_salary_range(soup):
	#pulling out salary range if indeed shows it
	salary_list = ['Salary Range']
	try:
		#getting the title
		title_v = soup.find(name = 'div', attrs = {'id':'univsrch-salary-title'})
		salary_list.append(cln_txt(title_v))

		#getting min
		min_v = soup.find(name = 'div', attrs = {'class':'float-left'})
		min_v = cln_txt(min_v)

		salary_list.append(min_v)
		#getting current salary
		current_salary = soup.find(name = 'p', attrs = {'id':'univsrch-salary-currentsalary'})
		salary_list.append(cln_txt(current_salary))
		#getting max salary
		max_v = soup.find(name = 'div', attrs = {'class':'float-right'})
		max_v = cln_txt(max_v)

		salary_list.append(max_v)
		#max number of response
		num_v = soup.find(name = 'p', attrs = {'id':'univsrch-salary-stats-para'})
		salary_list.append(cln_txt(num_v))

		return(salary_list)
	except:
		return

def extract_jobtype_counts(soup):
	#extracts count for full time, part time, temp, contractor, etc of the job positiosn
	out_l = ['JobType Count']
	if(soup.find(name = 'div', attrs = {'id':'JOB_TYPE_rbo'})):
		for ttt in  soup.find_all(name = 'div', attrs = {'id':'JOB_TYPE_rbo'}):
			for aaa in ttt.find_all("a"):
				out_l.append(aaa['title'])
	return(out_l)

def commit(cursor = None):
	if cursor == None:
		print("Can't commit, their is no connection open")
	else:
		try:
			cursor.commit()
		except sqlite3.Error as e:
			print("an error occurred while attempting to commit:", e.args[0])

def check_for_wages(in_list, wage_index = 3):
	#a function that runs through a list, and looks for $, then does a check and moves that into wages (if wages is null
	sum_values = []
	if in_list[wage_index] == None:
		for i in xrange(len(in_list)):
			if(in_list[i] == None):
				continue
			if( '$' in in_list[i]):
				temp = clean_for_wages(in_list[i])
				if temp != 0:
					sum_values.append(temp)
		if(len(sum_values) == 0):
			return(in_list)
		else:
			in_list[wage_index] = '$' + str(sum(sum_values)/float(len(sum_values)))

	else:
		in_list[wage_index] = '$' + str(clean_for_wages(in_list[wage_index]))

	return(in_list)

def clean_for_wages(in_s, auto_clean = True, upper_limit = 90, lower_limit = 8, method = 'first'):
	#cleans a string and only pulls out hte wage amount
	#wage_Type = 'H' is hourly wages, 'S" is salaried wages
	#method = first pulls the first occurence of wage, or method - average averages all occurens together
	if type(in_s) in [int,float]:
		return(in_s)

	in_s = in_s.replace(',','').upper()
	#removing some common issues with the data
	if('BILLION' in in_s or 'MILLION' in in_s):
		return(0)
	if('$' not in in_s):
		return(0)
	#print(in_s)
	found =[]
	for i in re.findall(r'\$+\s*\d+\.?\d*',in_s): #I've added the '$' to make SURE IT"S A DOLLAR AMOUNT!!!
		try:
			i = float(i.replace('$',''))
		except:
			print(i)
			ValueError('oops')
		if(auto_clean):
			if(i < 80 and i > 8.0):
				found.append(i)
			elif(i < 200000 and i > 10000):
				found.append(i)
		else:
			if(i < upper_limit and i > lower_limit):
				found.append(i)

	#now taking the average and returning the results
	if method == 'first':
		if(len(found) == 0):
			return(0)
		else:
			return(found[0])

	if method == 'average':
		return(sum(found)/float(len(found)))

def find_date_posted(in_s):
	#converts from 'posted 4 days ago' to the date it was actually posted
	fmt = '%Y-%m-%d'
	today = datetime.today()
	#if it's empty, assume it was pulled today
	try:
		if(in_s == None):
			posted = today
		elif('+' in in_s):
			posted = today - timedelta(days=31)
		else:
			delta = re.findall(r'\d+', in_s)
			delta = int(delta[0])
			if ('hour' in in_s):
				posted = today - timedelta(hours=delta)
			else:
				posted = today - timedelta(days=delta)
		return(posted.strftime(fmt))
	except:
		return(today.strftime(fmt))

def connect_to_storage_db(loc):
	#Connect to a location to store the data in SQLLiteDB
	conn = sqlite3.connect(loc)
	cursor = self.conn.cursor()
	return(conn, cursor)

def create_job_posting_table(cursor):
	cursor.execute('''create table job_posting(
					SearchKey Text,
					Date_Searched Date,
					JobID  Text,
	 				PostedDate Date,
					JobRole Text,
					Wage Text,
					Location Text,
					Employer Text,
					Summary Text,
					Experince Text,
					Sponsored_Ad Text,
					OnSite Text,
					AddURL Text,
					CompanyURL Text,
					PRIMARY KEY (JobID, SearchKey)'''
				   )
	commmit(cursor)


def create_stats_table(cursor):
	#creates the cursor table
	cursor.execute

def extract_next_links(soup, NEXT = False, start_URL = 'http://indeed.com', addurl = ''):
	#find what the next links will be
	next_links = []
	try:
		if(NEXT):
			if(soup.find_all(name = 'link', attrs = {'rel':'next'})):
				next_pages = soup.find(name = 'link', attrs = {'rel':'next'})
				next_links.append(start_URL + next_pages['href']+addurl)
		else:
			if(soup.find(name = 'div', attrs = {'class':'pagination'})):
				next_pages = soup.find('div',{'class':'pagination'})
				print('soup next pages')
				if(next_pages.find_all("a")):
					for sub_pages in next_pages.find_all("a"):
						if("Next" not in cln_txt(sub_pages)):
							next_links.append(start_URL + sub_pages['href'] + addurl)
	except:
		print('error')
		return(next_links)
	return(next_links)



if __name__ == "__main__":
	temp_start = 'c:/scripts/' # '/home/asmodi/'
	write_path = temp_start + 'output.txt'
	write_stats = temp_start + 'stats.txt'
	Zip_l = ['90210','10001',]
	print "Starting ..."
	print "\nStarting data scraping ..."
	myLoopZipCounter = 0
	myPrintCounter = 0
	page_limit = 100

	#clearing the data files
	try:
		os.remove(write_path)
		os.remove(write_stats)
	except:
		print('couldnt deleter the file, oh well')

	for Zip in Zip_l:
		current_page = 0
		basic_stats=[]
		URL,URL_ID = create_url(job = job_url, location = Zip, limit = limit_num, jobtype  = jobtype_url, return_key=True)
		print(URL)
		return_data = []
		while current_page < page_limit and len(URL) > 0:

			for cur_url in URL:
				#calling website
				sleep(0.1)
				print('working on %r of %r, with URl %r' %(current_page, page_limit,cur_url))
				soup_obj = call_website(cur_url)

				if(soup_obj == False or soup_obj.find_all("div", {"class": "bad_query"})):
					#is the dat agood
					break
				if(current_page == 0 and cur_url == URL[0]):
					basic_stats.append([URL_ID,extract_similar_jobs(soup_obj)])
					basic_stats.append([URL_ID,extract_job_salary_range(soup_obj)])
					basic_stats.append([URL_ID,extract_jobtype_counts(soup_obj)])
					basic_stats.append([URL_ID,extract_num_of_jobs_listing(soup_obj)])
					basic_stats.append([URL_ID,extract_salary_groups(soup_obj)])

				#breaking down soup to div
				soup_div = soup_obj.find_all('div', attrs = {'class':['row','request']})
				for div in soup_div:
					return_data.append([URL_ID,extract_jobposting_from_soup(div)])
			#getting next round of URL's to use
			URL = extract_next_links(soup_obj, NEXT = True)
			current_page = current_page + 1

		#now time to write that dats somewhere
		with open(write_path,'a') as c:
			writer = csv.writer(c, lineterminator='\n', delimiter = '|')
			writer.writerows(return_data)
		with open(write_stats, 'a') as c:
			writer = csv.writer(c, lineterminator='\n', delimiter = '|')
			writer.writerows(basic_stats)



