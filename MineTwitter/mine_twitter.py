#loading the required packages that are needed to get up and loaded
import sys
import os
import twitter as ty
import json
#import twitt_db as td
from sets import Set
import unicodecsv as csv


#Now  defining functions  that I need to get this bad bow running

def fig_auth_path():
	"""function to figure out the OS and where the twitter authorization file is"""
	if sys.platform == 'win32':
		ret = 'c:/scripts/twitter_auth.txt'
	elif sys.platform == 'linux2':
		ret = os.path.expanduser('~')+'/.auth/twitter_auth.txt'
	else:
		pass
	if os.path.isfile(ret):
		return(ret)
	else:
		raise ValueError("This system doesn't have a twitter authentication file")

def  authenticate_this_bird(path, open_type ='rb', delimiter =":"):
	""" takes a path to the file that holds the authentication data to mine twitter
	and then loads it into a dictionary and authenticats it.
	used for security purposes"""

	auth_ring = {} # a dictionary to hold all the values
	with open(path, open_type) as f:
		for r in f:
			r = r.split(delimiter)
			r[0] = r[0].lower().replace(" ","")
			r[1] =r[1].strip()
			if  r[0] == 'consumerkey':
				auth_ring[r[0]] = r[1]
			elif r[0] == 'consumersecret':
				auth_ring[r[0]] = r[1]
			elif r[0] == 'accesstoken':
				auth_ring[r[0]] = r[1]
			elif r[0] == 'accesssecret':
				auth_ring[r[0]] = r[1]
			else:
				pass
	if  len(auth_ring) < 4 :
		raise  ValueError("The authentication file did not contain all the needed elements")
	auth = ty.OAuth(auth_ring['accesstoken'], \
			auth_ring['accesssecret'],\
			auth_ring['consumerkey'],\
			auth_ring['consumersecret'])
	return(auth)

def twitter_search(twitter_api, q, max_results=200, **kw):
	"""Itterare through batch of results by following the cursor until we 
		reach the desired number of results, keepign in mind that OAuth uses
	can only make 180 serach querires per 15-minu interval"""

	search_results = twitter_api.search.tweets(q=q, count = 100, **kw)
	statuses = search_results['statuses']

	#iterate through batch of results by following the cursor until we 
	#reach the desired number of results, roughly 1k is reasonable

	max_results = min(1000,max_results)

	for _ in range(10):
		try:
			next_results = search_results['search_metadata']['next_results']
		except KeyError, e: #if nor emore reuslt when next resuldes DNE
			break

		#creating a dictionary from next_results
		kwargs = dict([kv.split('=')
				for kv in next_results[1:].split("&") ])

		search_reults = twitter_api.search.tweets(**kwargs)
		statuses += search_results['statuses']

		if len(statuses) > max_results:
			break

	return statuses

def flatten_json(j, current_key = '', outerdict = None):
	"""becuase jason can be in this horible layout where we have dicts in dicts in dicts
	in dicts, but it's not his mother, and my roomate ate my frog and aye aye aye
	this flattens out a json file so that each column is the deepest root of every node"""
	if outerdict is None:
		outerdict = {}
	for key, value in j.iteritems():
		newkey = current_key + "." + key if current_key else key
		if type(value) is not dict:
			if isinstance(value, basestring):
				outerdict[newkey] =  value.replace('\n',' ') #getting ride of returns
			else:
				outerdict[newkey] = value
		else:
			flatten_json(value, current_key = newkey, outerdict = outerdict)
	return outerdict


def listify(j):
	"""standardize all the jason files in  j, so they they flatten out into 
	a tableular format, for easy view in and research"""
	out_list = []
	s = Set([])
	#flatten each of the json files
	for l in range(len(j)):
		out_list.append(flatten_json(j[l]))
		for key in out_list[l].keys():
			if key not in s:
				s.add(key)
	set_list = list(s)
	#squaring it so that all flattened files have common output
	for l in range(len(out_list)):
		d = out_list[l]
		temp = []
		for s_ in set_list:
			temp.append(d.get(s_,None))
		out_list[l] =  temp
	return out_list,set_list


def main():
	"""The main function of python"""
	auth = authenticate_this_bird(fig_auth_path())
	tapi = ty.Twitter(auth = auth)

	print(tapi)
	hashtag_list = ['Walmart','#WalMart','\"Wal-Mart\"',"@walmart"]
#	hashtag_buys = ['\"out of stock\"','\"Did not have\"','\"have it\"']
	hashtag_buys =[' ']
	t =  []
	for hash in hashtag_list:
		for bash in hashtag_buys:
			start_t = len(t)
			t += twitter_search(tapi, q = ' AND '.join([hash,
								bash,
							   '-filter:retweets',
							  '-filter:replies'
							 ]),\
				 max_results = 1000, since = '2016-11-01',lang = 'en')
			print("after adding hash %s, bash %s we are now  %i big" % (hash,bash,len(t) - start_t))

	flatten_t, header  = listify(t)
	csvfile = os.path.expanduser("~") + '/twitterout.csv'
	with open(csvfile, "w") as f:
		writer = csv.writer(f,delimiter ="|", lineterminator = '\n', encoding = 'utf-8')
		writer.writerow(header)
		for item in flatten_t:
		#writer.writerows(flatten_t)
			writer.writerow(item)
if __name__=="__main__":
	main()


