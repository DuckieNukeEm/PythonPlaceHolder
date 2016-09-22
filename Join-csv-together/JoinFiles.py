__author__ = 'ccfinch'

import os
import csv
import string
import sys
import datetime as dt

##############################
#
# defining control paramseters
#
###############################

File_location = os.path.dirname(os.path.realpath(__file__)) 
file_save = os.path.dirname(os.path.realpath(__file__)) + "\\combined file.csv"
header = []
file_type = 'csv'
out_delim = ","
in_delim = ","
list_of_files = []
replace_dict = {}

##############################
#
# Defining Functions
#
###############################

def get_list_of_files(files_loc):
    r = os.listdir(files_loc)
    map(string.strip, r )
  #  r.remove('Python Control File.csv') #geting ride of the command file
    for rr in r: #removing the control file and the output file
        if rr == file_save.split('\\')[-1] or rr == file_save.split('/')[-1] or rr == 'Python Control File.csv' :
            r.remove(rr)

    return(r)

def get_only_filetypes(file_list, file_type = 'csv'):
    o_list = []
    for l in file_list:
        try:
            if l.split(".")[1] == file_type:
                o_list.append(l)
        except:
            print('FAIL: %s') % l
    return(o_list)

def load_file(head, file_name, open_type = 'rb', delimiter = ","):
    #opens a file, and reads in the file
    #then scrapes off any data before a row matching the header is received
    with open(file_name, open_type) as f:
        r = csv.reader(f, delimiter = delimiter)
        o_list = list(r)
    #Now finding the start of the data from the list provided to us

    if len(head) >= 1 and not isinstance(head, (int, long)): #if we actually have a header
        for l in xrange(len(o_list)):
            if o_list[l] == header:
                break
        if l == (len(o_list)):
            o_list = []
        else:
            o_list = o_list[l+1:]
    elif isinstance(head, (int, long)): #if the header is a number (start on row header)
        o_list = o_list[head:]
    else:
        1==1
    return o_list

def check_column_size(file, header = 0):
    #returns a list of all indexies that are not the same size as
    #the specified row (default, header
    col_length = file[header]
    bad_lengths = []
    for l in file:
        if(len(l)) != col_length:
            bad_lengths.append(file.index(l))
    return(bad_lengths)

def replace_values(in_list, value_to_find, value_to_replace):
    for j in range(len(in_list)):
        in_list[j] = [value_to_replace if x == value_to_find else x for x in in_list[j]]
        #in_list[j] = map(lambda x:x if x != value_to_find else value_to_replace,  in_list[j])
    return in_list

def check_for_date_IO(file_path):
    ###simple function that will replace certain key words ($PPE$,$TODAY$) with the proper date
    file_path = file_path.split("$")
    if file_path[1].upper() == "PPE":
       file_path[1] = str(dt.date.today() - dt.timedelta(days = (dt.date.today() - dt.date(1900,01,12)).days % 14))
       file_path = ''.join(file_path)
    elif file_path[1].upper() == "TODAY":
       file_path[1] = str(dt.date.today())
       file_path = ''.join(file_path)
    else:
        1==1
    return(file_path)

##############################
#
# Running the main loop
#
###############################


os.path.dirname(os.path.realpath(__file__))

#reading in Control File
with open(File_location + "\\Python Control File.csv","rb") as f:
    con = csv.reader(f)
    con = list(con)

#setting parameters from the control file
for l in con:
    if len(l) == 0:
        continue
    v = l[0].lower()
    if v == 'header':                # if the control parameter has a header
        header = l[1:]
     #   print(header)
    elif v == 'directory location':       # if the control parameter has file location
        File_location = l[1]
    #    print(File_location)
    elif v == 'file type':           # if the control parameter has a file type (csv, txt, etc.)
        file_type = l[1].lower()
      #  print(file_type)
    elif v == 'save location':       # if the control parameter has a save location for the output
        file_save = l[1]
      #  print(file_save)
    elif v == 'in delimiter':           # if the control parameter has a delimiter for the input files
        in_delim = l[1].strip()
      #  print(in_delim)
    elif v == 'out delimiter':             #if the control paramter has a delimiter for the output files
        out_delim = l[1].strip()
    elif v =='delimiter':                 # if you want a general delimiter
        out_delim = l[1].strip()
        in_delim = l[1].strip()
    elif v == 'file':                # if the control parameter has a file it would like to use (more than one)
        list_of_files.append(File_location + l[1])
     #   print(list_of_files)
    elif v == 'replace':               # if there is a value we would like to replace
        replace_dict[l[1]] = l[2]
    #    print(replace_dict)
    elif v == 'run after':               #if you want to run a script after this scripts runs
        run_das_script = l[1]
     #   print(run_dats_script)
    else:
        continue
print(in_delim)
# getting and cleaning the list of files
if(len(list_of_files) == 0):
    list_of_files = get_list_of_files(File_location)
    list_of_files = get_only_filetypes(list_of_files, file_type)

#making sure there are files in that location
if(len(list_of_files) == 0):
    sys.exit("Sorry buddy, but the location you gave for where the files are, there are no csv files there")

#checking to see if we need to 'modify' the save location string
file_save = check_for_date_IO(file_save)

#overwriting saved file
if isinstance(header, (int, long)) or len(header) == 0:
    open(file_save, "w").close()
else:
    with open(file_save, "wb") as f:
        csv_writer = csv.writer(f, delimiter = out_delimdelim)
        csv_writer.writerow(header)

for filez in list_of_files:
    print("working on file %s, %i of %i") % (filez, list_of_files.index(filez), len(list_of_files))

    l_filez = load_file(header, filez, delimiter = in_delim)
    if len(l_filez) > 0:
        if len(replace_dict) > 0:
            for k, v in replace_dict.items():
                l_filez = replace_values(l_filez, k, v)
        with open(file_save, 'ab') as you_such_a_foo:
            csv_writer = csv.writer(you_such_a_foo,  delimiter = out_delim)
            for o in l_filez:
                csv_writer.writerow(o)


try:
    os.system(run_das_script)
except:
    print("No Other Script to run.....JOB DONE!")
