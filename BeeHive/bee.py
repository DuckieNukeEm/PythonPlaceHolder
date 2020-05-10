import pyodbc
import getpass
import socket


dict_of_format = { "QUERY": [['DATABASE','SQL_STATEMENT'],
                             {'EXPORT_LOCATION': 'c:/scripts/export.txt',
                              'DELIMITER' : '|',
                              'HEADER' : 'Y',
                              'APPEND': False}
                             ],
                   "SCRIPT" : [['RUN_LOCATION'],
                               {'APPLICATION': 'python'}
                   }

class bee:
    '''This is the working bee, which is given a single item to manange and work through'''
    def __init__(self, Queen, bee_number, location = "~", tasks = []):
        self.name = socket.gethostname() + ":" + getpass.getuser() + ":"
        self.WorkerNumber = bee_number
        self.queen_beee = Queen
        self.alive = True
        self.pollen = ''
        self.add_pollen(task)

    def add_pollen(self, task):
        "This takes the info provided and unpacks it into a way thats easily readable by the system and hu-mans"
        if not isinstance(task, dict):
            task = convert_to_dict(task)
        if task['type'].upper() == 'QUERY':
            try:
                list_values_in_dict[dict_of_format['QUERY'][0],task]:
                task = set_default_values(task, dict_of_format['QUERY'][1])
                if task['DATABASE'][0:1] not in ('WM'):
                     PW = ,
                    if 'USERID' not in task:
                        task['USERID'] = self.name.split(":")[1]
                    if 'PASSWORD' not in task:
                        task['PASSWORD'] = find_pw(self.queen.info_loc['PASSWORD LOC'],task['DATABASE'])

        if tasks['type'].upper() == 'SCRIPT':
            try:
                list_values_in_dict[dict_of_format['QUERY'][0], task]:
            except ValueError as Err:
                bee_error(Err)


ef bee_error(the_Error):
    print(the_Error)

def load_list(path, delim = ","):
    d = {}
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                (key, val) = line.split(',')
                d[key] = val
        return d
    else:
        print("Path to password directory doesn't exists")


def convert_to_dict(str):
    '''
    WORKING ON THIS:
    Will take a string then formate it into a dict, right now the assumption is that it is a duct
    :inpurt: a string
    :return:  a dict
    '''
    return(str)
def format_dict_for_x(task, query_list, type = 'query')

def set_default_values(dict1, defualt_dict):
    #Set the defualt values of the dictornary if they don't exists
    for k in dict1.keys():
        dict1[k] = dict1.get(k, defualt_dict[k])
    return(dict1)


def list_values_in_dict(list1, dict1):
    for l in list1:
        if dict1.get(l, False) == False:
            raise ValueError(l + " Wasn't in the list of values")
    return(True)

def find_pw(path_to_dict, PW_to_find, delim = '|'):
    '''
    Takes a dict and pulls out the correct password
    :param dict_to_dict:
    :param PW_to_find:
    :return:
    '''
    d = load_list(path, delim)
    return()

def load_list(path, delim=","):
    '''
    takes a path and loads the file into a dictonary
    :param path:  the path to the file
    :param delim:  the seperator in the file
    :return d: the dictonary that is returned
    '''

    d = {}
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                (key, val) = line.split(',')
                d[key] = val
        return d
    else:
        print("Path to password directory doesn't exists")