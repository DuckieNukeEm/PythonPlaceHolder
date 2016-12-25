import re
from collections import Counter
from nltk.corpus import stopwords
from nltk import bigrams
import string as st


def create_regex_strings():
	emoticons_str = r"""
		(?:
		[:=;] # Eyes
		[oO\-]? # Nose (optional)
		[D\)\]\(\]/\\OpP] # Mouth
		)"""
	regex_str = [
		emoticons_str,
		r'<[^>]+>', # HTML tags
		r'(?:@[\w_]+)', # @-mentions
		r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
		r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
		r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
		r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
		r'(?:[\w_]+)', # other words
		r'(?:\S)' # anything else
		]
	regex_all = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
	regex_emoti = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 	return( (regex_all, regex_emoti))

def tokenize(s, reg_method, lower_case = False, second_token = None):
	token = reg_method.findall(s)
	if lower_case:
		if second_token != None:
			token = [token if second_token.search(token) else token.lower() for token in token]
	return token

def create_stopword_list():
	stop = stopwords.words('english') + list(st.punctuation) + ['rt','via']
	return(stop) 

def remove_stop(token, stop_list):
	term_stop = [term for term in token if term not in stop_list] #eh, is this really efficent?
	return(term)

def count_hashes(token):
	term_hash = [term for term in token if term.startswith("#")]
	return(term_hash)

def count_terms(token, stop):
	term_only = [term for term in token
				if term not in stop
				and not term.startswith(('#','@'))]
	return(term_only)
def count_bigrams(token):
	terms_bigram = bigrams(token)
	return(terms_bigrams)


if __name__== "__main__":
	(a,b) = create_regex_strings()
	r = tokenize("Poop PooP Cacho :P", a)
	st = create_stopword_list() 
