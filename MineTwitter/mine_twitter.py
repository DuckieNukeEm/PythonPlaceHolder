import sys
import os
import tweepy
from tweepy import OAuthHandler

def fig_auth_path():
	if sys.platform == 'win32':
		ret = 'c:/scripts/twitter_auth.txt'
	elif sys.playform == 'linux2':
		ret = '~/.auth/twitter_auth.txt'
	else:
		pass
	if os.path.isfile(ret):
		return(res)
	else:
		raise ValueError("This system doesn't have a twitter authentication file")

def  authenticate_this_bird(path, open_type ='rb', delimiter =":"):
	""" takes a path to the file that holds the authentication data to mine twitter
	and then loads it into a dictionary and authenticats it.
	used for security purposes"""

	auth_ring = {} # a dictionary to hold all the values
	with open(path, open_type) as f:
		r = f.readline().split(delimiter)
		r[0] = r[0].lower().replace(" ","")
		if  r[0] == 'consumerkey':
			auth_ring[r[0]] = r[1]
		elif r[0] == 'consumersecret':
			auth_ring[r[0]] = r[1]
		elif r[0] == 'accesstoken'
			auth_ring[r[0]] = r[1]
		elif r[0] == 'accesssecret':
			auth_ring[r[0]] = r[1]
		else:
			pass
	if  len(auth_ring) < 4 :
		raise  ValueError("The authentication file did not contain all the needed elements")
	auth = OAuthHandler(auth_ring[consumerkey],auth_ring[consumersecret])
	auth.set_access_token(auth_ring[accesstoken],auth_ring[accesssecret])

	return(auth)


def main():
	"""The main function of python"""
	
	auth = authenticate_this_bird(fig_auth_path())
	api = tweepy.API(auth)




if __name__=="__main__":
	main()


