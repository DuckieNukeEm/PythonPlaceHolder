#loading the required packages that are needed to get up and loaded
import sys
import os
import twitter as ty
import json
import pymongo

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

def twitter_search(twitter_api, q, max_results=220, **kw):
	"""Itterare through batch of results by following the cursor until we 
		reach the desired number of results, keepign in mind that OAuth uses
	can only make 180 serach querires per 15-minu interval"""
	search_results = twitter_api.search.tweets(q=q, count = 100, **kw)
	statuses = search_results['statuses']


def main():
	"""The main function of python"""
	auth = authenticate_this_bird(fig_auth_path())
	tapi = ty.Twitter(auth = auth)
	print(tapi)
	t = tapi.search.tweets(q="#WM",count = 3)
	print json.dumps(t['statuses'][0], indent = 1)



if __name__=="__main__":
	main()


