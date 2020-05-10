import json

#all can be found here 
# https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.pdf

census_dict = {
'returntype' : ['geographies','locations'],
'searchtype' : ['onelineaddress','address','coordinates'],
'benchmark' : ['Public_AR_Current','Public_AR_ACS2017','Public_AR_Census2010'],
'vintage' : {'Public_AR_Current' : ['Current_Current','Census2010_Current','ACS2013_Current','ACS2014_Current','ACS2015_Current','ACS2016_Current','ACS2017_Current'],
			 'Public_AR_ACS2017' : ['Current_ACS2017','Census2010_ACS2017','ACS2013_ACS2017','ACS2014_ACS2017','ACS2015_ACS2017','ACS2016_ACS2017','ACS2017_ACS2017'],
			 'Public_AR_Census2010' : ['Census2010_Census2010','Census2000_Census2010']
			 },
'format' : ['json','html'],
'layers' : {'All':'All', '0':'2010 Census Public Use Microdata Areas',
'2':'2010 Census ZIP Code Tabulation Areas','4':'Tribal Census Tracts',
'6':'Tribal Block Groups','8':'Census Tracts',
'10':'Census Block Groups','12':'2010 Census Blocks',
'14':'Unified School Districts','16':'Secondary School Districts',
'18':'Elementary School Districts','20':'Estates',
'22':'County Subdivisions','24':'Subbarrios',
'26':'Consolidated Cities','28':'Incorporated Places',
'30':'Census Designated Places','32':'Alaska Native Regional Corporations',
'34':'Tribal Subdivisions','36':'Federal American Indian Reservations',
'38':'Off-Reservation Trust Lands','40':'State American Indian Reservations',
'42':'Hawaiian Home Lands','44':'Alaska Native Village Statistical Areas',
'46':'Oklahoma Tribal Statistical Areas','48':'State Designated Tribal Statistical Areas',
'50':'Tribal Designated Statistical Areas','52':'American Indian Joint-Use Areas',
'54':'116th Congressional Districts','56':'2016 State Legislative Districts - Upper',
'58':'2016 State Legislative Districts - Lower','60':'Census Divisions',
'62':'Census Regions','64':'2010 Census Urbanized Areas','66':'2010 Census Urban Clusters',
'68':'Combined New England City and Town Areas','70':'New England City and Town Area Divisions',
'72':'Metropolitan New England City and Town Areas','74':'Micropolitan New England City and Town Areas',
'76':'Combined Statistical Areas','78':'Metropolitan Divisions',
'80':'Metropolitan Statistical Areas','82':'Micropolitan Statistical Areas','84':'States',
'86':'Counties'} }




def call_parts():
	"""returns a disctionary for the parts of the census call"""
	census_dict =
	{ "Base_Call":"https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress?address=",
	  "benchmak":"Public_AR_Current",
	  "vintage":"ACS2017_Current",
	  "layers": "all",
	  "format" : "json"	
	}
	return(census_dict)
	
	
def special_char_dict(to_ascii = False):
	"""A Normal dictionary that has the asci/'hex' of special characters"""
	df = { '!' : '21', '#' : '23','$' : '24',
		'%' : '25','&' : '26',"'" : '27','(' : '28',')' : '29',
		'*' : '2A','+' : '2B',',' : '2C','-' : '2D','.' : '2E',
		'/' : '2F',':' : '3A',';' : '3B','<' : '3C','=' : '3D',
		'>' : '3E','?' : '3F','[' : '5B',']' : '5D',
		'^' : '5E','_' : '5F','`' : '60','{' : '7B','|' : '7C',
		'}' : '7D','~' : '7E'} #'“' : '22',  "\\" : '5C' '' : '20',
	
	if to_ascii:
		df = dict((v,k) for k,v in df.iteritems())
	return(df)

def returntype(Prf = None):
	""" Populate the return type for the URL"""
	returntype_list = census_dict['returntype']
	if(Prf in returntype_list):
		rt = Prf
	else:
		rt = returntype_list[0]
		
	return(rt)

def searchtype(Prf = None):
	"""Return the type of search being done"""
	st_list = census_dict['searchtype']
	if(Prf in st_list):
		rt = Prf
	else:
		rt = st_list[0]
	
	return(rt)

def benchmark(Prf = None):
	"""Selects the correct benchmark"""
	bm_list = census_dict['benchmark']
	if(Prf in bm_list):
		rt = Prf
	else:
		rt = bm_list[0]
	
	return(rt)

def vintagetype(Prf = None, Benchmark = 'Public_AR_Current'):
	"""This will probably have to be updated every year
	pulls back what vintage of the benchmark you want to do"""
	
	vintage_list = census_dict['vintage'] #this returns a dict, not a list
	if Benchmark not in vintage_list.keys():
		Benchmark = vintage_list.keys[0]
		
	vintage_list = vintage_list[Benchmark] #now getting the list from the above dict
	
	if(Prf in vintage_list):
		rt = Prf
	else:
		rt = vintage_list[0]
	
	return(rt)
		
def formattype(Prft = None):
	"""selects the right return format"""
	fm_list = census_dict['format']
	if(Prf in fm_list):
		rt = Prf
	else:
		rt = fm_list[0]
	
	return(rt)
	
def layerstype(Prft = None):
	"""picks the approp layers. THis one is intrestings as I need to go
	through and check that they map properly
	actually...fuck it, we're going to defualt to all"""
	return('all')	
	
def prep_address(Addy, SearchType):
	"""Cleans and preps the address - based on the SearchType"""
	return_addy = ''
	return_list =['street', 'city', 'state', 'zip']

	if(SearchType == 'coordinates' and isinstance(Addy, dict)):
		return_addy = 'x=' + str(Addy.get('x')) + "&y=" + str(Addy.get('y'))
		
	elif(SearchType == 'address' and isinstance(Addy, dict)):
		for l in return_list:
			new_add_value = Addy.get(l)
			if new_add_value != None:
				return_addy = return_addy + l + "=" + str(new_add_value) + "&"
			
		return_addy = return_addy.replace(' ','+') 
	elif(SearchType == 'onelineaddress' and isinstance(Addy, str)):
		for sc, rp in special_char_dict().items():
			Addy = Addy.replace(sc, '%' + rp)	
			return_addy = Addy.replace(' ','+') 
	else:
		print('was not able to translate address')
		
	return(return_addy)
	
	
	
	
def build_Census_line(Addy, ReturnType = None, Search = None, Benchmark = None, Vintage = None, Format = None, Layers = None):
	""" builds the actual HTML line to call the base format of the string
	is
	https://geocoding.geo.census.gov/geocoder/returntype/searchtype?parameters
	"""
	if(ReturnType != None):
		
	
	
	
	
	base_htm = "https://geocoding.geo.census.gov/geocoder/"
	base_html = base_html + returntype(ReturnType) + "/"
	base_html = base_html + searchtype(Search)
	Addy = clean_addy()
	



def make_census_call(address, text_block = None):
	"""This makes the actual census call based on an an address"""
	if text_block == None:
		census_txt = call_parts()
	address = prep_address(address)
	census_txt = "https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress?address="
	#3709+West+Cherokee+Rd%2C+Rogers%2C+AR+72758&benchmark=Public_AR_Current&vintage=ACS2017_Current&layers=all&format=json




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
