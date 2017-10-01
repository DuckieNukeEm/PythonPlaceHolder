

import requests
import csv
import re
import os
from datetime import datetime, timedelta
from time import sleep
from bs4 import BeautifulSoup
import JobScrapperDB as db

#note
#any function starting with a 'get' pulls data from a subset of div:{class:row}
#any function starting with extract pulls directly on the return result

#http://blog.nycdatascience.com/student-works/web-scraping/glassdoor-web-scraping/
indeed_URL = 'https://www.indeed.com/jobs?q='
job_url = 'cashier' #"title:warehouse company:amazon"
limit_num = 50
jobtype_url = None #''&jt=parttime'
filter_url = None #'&filter=0'
sort_url = '&sort=date'


def create_url(base_url = 'https://www.indeed.com/jobs?q=', job = None, location = None, limit = 50, jobtype = None, company = None, salary = None, explvl = None, radius = None, sort = None, filter = None, start = None, return_key = False):
	# URL = 'https://www.indeed.com/jobs?q=data+scientist&l=New+York&limit=50'
	# &limit= is the number of results to return, it maxes out at 50
	# &l= is location (either city, city state, state, zipcode, or national)
	# &jt= is job type (parttime, fulltime, contract,temporary,internship,commission)
	# &rbc= is company (follows directly location)
	# &explvl= is experince level (mid_level,entry_level,senior_level)
	# &filter= do we want to hide similar results?
	# &sort= sorts by date or relevance
	# &radius= sets the radius of how far to search (natural default is 25mi

	url_key = ['','','','','','','']
	if(job != None):
		base_url = base_url + job
		url_key[0] = job

	if(salary != None):
		base_url = base_url + '+' + salary
		salary = salary.replace('$','').replace(',','')
		url_key[1] = int(salary)

	if(location != None):
		base_url = base_url + '&l=' + location
		url_key[2] = location

	if(jobtype != None):
		if(jobtype in ['parttime','fulltime','contract','temporary','internship','commission']):
			base_url = base_url + '&jt=' + jobtype
			url_key[3] = jobtype
		else:
			print('JobType isnt in the standard list of job types')

	if(company != None):
		base_url = base_url + '&rbc=' + company
		url_key[4] = company

	if (explvl != None and explvl in ['mid_level', 'entry_level', 'senior_level']):
		base_url = base_url + '&explvl=' + explvl
		url_key[5] = explvl

	if (radius != None and radius in [5, 10, 15, 25, 50, 100]):
		base_url = base_url + '&radius=' + str(radius)
		url_key[6] = radius

	if(sort != None and sort in ['date','relevance']):
		base_url = base_url + '&sort=' + sort

	if(filter != None and filter in [0,1]):
		base_url = base_url + '&filter=' + str(filter)

	if(start != None):
		base_url = base_url + '&start=' + str(start)

	if (limit != None):
		if(limit not in [10, 20, 30, 40, 50]):
			limit = 50
		base_url = base_url + '&limit=' + str(limit)
	if(return_key):
		return(([base_url], '|'.join(url_key)))
	else:
		return([base_url])

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
					if ("$" in cln_txt(temp) and len(str(temp))<90 and 'http' not in cln_txt(temp)):
						out_p = temp
				if(out_p == None):
					#I'm going to scan through ALL the text looking for a wage rate!
					out_p = clean_for_wages(cln_txt(div_v))
					if(out_p == 0):
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
		#Damn, that's pretty f'cking simple
		out_p = div_v['id']
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

def is_bool(item):
	#simple thing to check if a thing is a boolian object
	if(isinstance(item, bool)):
		return(True)
	else:
		return(False)

def extract_jobposting_from_soup(div_v, default = 'N/A', search_for_wages = False):
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
	if(search_for_wages):
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

def extract_salary_groups(soup, return_value = 'title'):
	#pulls salary counts by groupings
	if return_value == 'title':
		salary_group = ['Salary Group']
	else:
		salary_group = []
	if (is_bool(soup)):
		return (out_l)
	if(soup.find(name = 'div', attrs = {'id':'SALARY_rbo'})):
		for ttt in soup.find_all(name = 'div', attrs = {'id':'SALARY_rbo'}):
			for aaa in ttt.find_all('a'):
				salary_group.append(aaa[return_value])
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

def extract_jobtype_counts(soup, return_value = 'title'):
	#extracts count for full time, part time, temp, contractor, etc of the job positiosn
	if return_value == 'title':
		out_l = ['JobType Count']
	else:
		out_l = []
	if (is_bool(soup)):
		return (out_l)
	try:
		if(soup.find(name = 'div', attrs = {'id':'JOB_TYPE_rbo'})):
			for ttt in  soup.find_all(name = 'div', attrs = {'id':'JOB_TYPE_rbo'}):
				for aaa in ttt.find_all("a"):
					out_l.append(aaa[return_value])
		return(out_l)
	except:
		return (out_l)

def extract_experience_counts(soup, return_value = 'title'):
	#extracts the experience level (entry, mid,	and on other one
	if return_value == 'title':
		out_l = ['experience level Count']
	else:
		out_l = []
	if (is_bool(soup)):
		return (out_l)
	try:
		if (soup.find(name='div', attrs={'id': 'EXP_LVL_rbo'})):
			for ttt in soup.find_all(name='div', attrs={'id': 'EXP_LVL_rbo'}):
				for aaa in ttt.find_all("a"):
					out_l.append(aaa[return_value])
		return (out_l)
	except:
		return (out_l)

def extract_company_counts(soup, return_value = 'title'):
	#This will pull out the companys that are available with the counts for each
	if return_value == 'title':
		out_l = ['Company Counts']
	else:
		out_l = []

	if(is_bool(soup)):
		return(out_l)
	if (soup.find(name='div', attrs={'id': 'COMPANY_rbo'})):
		for ttt in soup.find_all(name='div', attrs={'id': 'COMPANY_rbo'}):
			for aaa in ttt.find_all("a"):
				out_l.append(aaa[return_value])
	return (out_l)

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

def clean_for_wages(in_s, auto_clean = True, upper_limit = 90, lower_limit = 8, method = 'first', exclude_http = True):
	#cleans a string and only pulls out hte wage amount
	#wage_Type = 'H' is hourly wages, 'S" is salaried wages
	#method = first pulls the first occurence of wage, or method - average averages all occurens together
	if type(in_s) in [int,float]:
		return(in_s)

	in_s = in_s.replace(',','').upper()
	#removing some common issues with the data
	if('BILLION' in in_s or 'MILLION' in in_s ):
		return(0)
	if('$' not in in_s):
		return(0)
	if(exclude_http):
		if('HTTP' in in_s):
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
			elif(i < 300000 and i > 10000):
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

def link_to_linkid(URL):
	#this takes a link and extracts the link ID on it
	#doing splits on the ?
	order_dict = {'q':0,
				  '+':1, #This is the odd man out, becuase they drop thew ages directly into the searchURL
				  'l':2,
				  'jt':3,
				  'rbc':4,
				  'explvl':5,
				  'radius':6
				  }

	if(type(URL)!=str):
		return(str(URL))

	URL_split = ['','','','','','','']

	#splitting off the original 'hhtps://www.indeed.com crap
	URL = URL.replace('+',' ')
	URL = URL.split('?')
	if(len(URL) == 2):
		URL = URL[1].split('&')
	else:
		URL = URL[0].split('&')

	for u in URL:
		u_split = u.split('=')
		index = order_dict.get(u_split[0],99)
		if(index < len(order_dict)):
			URL_split[index] = u_split[1]

	#Now  pulling out salary from Job Code (if it exists)
	if(URL_split[0] != ''):
		wage = clean_for_wages(URL_split[0], exclude_http=False)
		if(wage!=''):
			URL_split[1] = str(int(wage))
			jobsplit = URL_split[0].split('$')
			if(len(jobsplit) == 1):  #there's no job, it's just a salary search
				URL_split[0] = ''
			else:
				URL_split[0] = ' '.join(jobsplit[:(len(jobsplit)-1)]).strip()
	return('|'.join(URL_split))

def walk_url_trees(START_URL, PREPEND_URL = 'http://indeed.com', cursor = None ):
	#this function will take the start URL, and then will cut the data by every option to get the deepest refinment of the data
	#it will be this we walk down the file
	#we will first walk it by Company, then by Job, then by Salary Group, then by experience
	sleep(1)
	print(START_URL)

	#if a list was passed, I just want to ttake the first element of the list
	if (isinstance(START_URL, list)):
		START_URL = START_URL[0]

	if(START_URL[0:4] == 'http'):
		soup_obj = call_website(START_URL)
	else:
		soup_obj = call_website(PREPEND_URL + START_URL)


	return_list = []
	#first, a list of compnay URLS
	COMPANY_URL_LIST =  extract_company_counts(soup_obj, return_value='href')
	#then JOB_LIST
	JOB_URL_LIST = extract_jobtype_counts(soup_obj, return_value='href')
	#then Salary
	SALARY_URL_LIST = extract_salary_groups(soup_obj, return_value='href')
	#and finally, experience level
	XP_URL_LIST = extract_experience_counts(soup_obj, return_value = 'href')
	if(COMPANY_URL_LIST != []):
		for l in COMPANY_URL_LIST:
			return_list = return_list + walk_url_trees(l, PREPEND_URL, cursor)
	elif(JOB_URL_LIST != []):
		for l in JOB_URL_LIST:
			return_list = return_list + walk_url_trees(l, PREPEND_URL, cursor)
	elif(SALARY_URL_LIST != []):
		for l in SALARY_URL_LIST:
			return_list = return_list + walk_url_trees(l, PREPEND_URL, cursor)
	elif(XP_URL_LIST != []):
		for l in XP_URL_LIST:
			return_list = return_list + walk_url_trees(l, PREPEND_URL, cursor)
	else:
		return([PREPEND_URL + START_URL])

	return(return_list)
	#now gotta flatten the list to pass up


def scrape_indeed(URL, Get_Stats = True, Output_to_db = False, Next = True, Page_limit = 100, cursor = None, verbos = True, save_loc = "~", walk_tree = True):
	#This is the function that runs the will actuall scrap Indeed.com to find

	if(Output_to_db == False):
		write_path = save_loc + 'output.txt'
		write_stats = save_loc + 'stats.txt'

	#lets get the list of URL that we need to use:
	if(walk_tree):
		URL_list = walk_url_trees(URL)
	else:
		URL_list = URL
	print(URL_list)
	for url in URL_list:
		URL_ID = link_to_linkid(url)
		Page_Count = 0
		cur_url = url
		data = []
		basic_stats = []
		while(Page_limit > Page_Count):
			sleep(1)
			if(verbos):
				print('working on %r of %r, with URl %r' % (Page_Count, page_limit, cur_url))
			soup_obj = call_website(cur_url)

			if (soup_obj == False or soup_obj.find_all("div", {"class": "bad_query"})):
				# is the data good
				break
			if (Get_Stats and Page_Count == 0):
				basic_stats.append([URL_ID, extract_similar_jobs(soup_obj)])
				basic_stats.append([URL_ID, extract_job_salary_range(soup_obj)])
				basic_stats.append([URL_ID, extract_jobtype_counts(soup_obj)])
				basic_stats.append([URL_ID, extract_num_of_jobs_listing(soup_obj)])
				basic_stats.append([URL_ID, extract_salary_groups(soup_obj)])

			# breaking down soup to div
			soup_div = soup_obj.find_all('div', attrs={'class': ['row', 'request']})
			for div in soup_div:
				data.append([URL_ID, extract_jobposting_from_soup(div)])
			# getting next round of URL's to use
			if(Next):
				next_URL = extract_next_links(soup_obj, NEXT=True)
				if(next_URL != ''):
					break
				else:
					cur_url = next_URL[0]
			else:
				break
				Page_Count = Page_Count + 1
		if(Output_to_db == False): #If we don't want to save the infomariotn to da data base
			if(verbos):
				print("Now Saving dataa")
			#saving it to a tempory Location
			with open(write_path, 'a') as c:
				writer = csv.writer(c, lineterminator='\n', delimiter='|')
				writer.writerows(data)
			with open(write_stats, 'a') as c:
				writer = csv.writer(c, lineterminator='\n', delimiter='|')
				writer.writerows(basic_stats)




if __name__ == "__notmain__":
	save_loc = 'c:/scripts/' # '/home/asmodi/'
	write_path = save_loc + 'output.txt'
	write_stats = save_loc + 'stats.txt'
	Zip_l = ['90210','10001',]
	print "Starting ...\n"
	print "Starting data scraping ..."
	myLoopZipCounter = 0
	myPrintCounter = 0
	page_limit = 100

	job_cursor, job_conn = db.connect_to_storage_db('c:/scripts/job_posting.sqlite')

	#clearing the data files
	try:
		os.remove(write_path)
		os.remove(write_stats)
	except:
		print('couldnt deleter the file, oh well')

	for Zip in Zip_l:
		current_page = 0
		basic_stats=[]
		URL,URL_ID = create_url(job = job_url, location = Zip, limit = limit_num)


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

if __name__ == "__main__":
	save_loc = 'c:/scripts/'  # '/home/asmodi/'

	write_path = save_loc + 'output.txt'
	write_stats = save_loc + 'stats.txt'
	db_loc = save_loc + 'job_posting.sqlite'
	job_url = ['company%3A"Publix"',
			   'company%3A"Dollar+General"',
			   'company%3A"Target"',
			   'company%3A"Aldi"',
			   'company%3A"Kroger"',
			   'company%3A"Lowe%27s"',
			   'company%3A"McDonald%27s"']
				#the %27 is for the appostrofy (like in Lowe's)
				#the %3A is a colon

	print "Starting ...\n"
	print "Starting data scraping ..."
	myLoopZipCounter = 0
	myPrintCounter = 0
	page_limit = 100

	job_cursor, job_conn = db.connect_to_storage_db(db_loc)

	# clearing the data files
	try:
		os.remove(write_path)
		os.remove(write_stats)
	except:
		print('couldnt deleter the file, oh well')

	for job in job_url:
		print("working on %r" %job)
		URL = create_url(job=job, location='', limit = None)
		scrape_indeed(URL, save_loc=save_loc)
	for job in job_url: #yes, I'm doing this twice, once wehre I walk the tree, the second time where I just hit every job posting
		print("working on %r" % job)
		URL = create_url(job=job, location='', limit=None)
		scrape_indeed(URL, save_loc=save_loc, walk_tree=False)
		scrape_indeed(URL, save_loc=save_loc, walk_tree=False)

else:
	print("well.....poop")