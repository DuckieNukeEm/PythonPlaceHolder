'''
This python file is used to take the values from the scrapper tool, and then run then formate it into a
db layout
'''
import sqlite3
from re import findall
from datetime import datetime

def get_numbers(in_s):
    in_s = in_s.replace(',', '').upper()
    in_s = findall(r'\d+\.?\d*', in_s)
    return(in_s)

def now():
    fmt = '%Y-%m-%d'
    today = datetime.today()
    return(today.strftime(fmt))

def connect_to_storage_db(loc):
    # Connect to a location to store the data in SQLLiteDB
    conn = sqlite3.connect(loc)
    cursor = conn.cursor()

    #Now I'm going to attemp to create the tables if they don't exists
    #I DO EXPECT THIS TO FAIL IF THEY ALREADY EXISTS hence the try and all that crap

    try:
        create_job_posting_table(cursor)
        print('Created Job Posting Table')
    except:
        print('Job posting table already exists')

    try:
        create_stats_table(cursor)
        print('create states table')
    except:
        print('Stats table already exists')
    return (conn, cursor)

def commit(cursor = None):
    #allows a commit to happen and caputes all the erros for me :D
    if cursor == None:
        print("Can't commit, their is no connection open")
    else:
        try:
            cursor.commit()
        except sqlite3.Error as e:
            print("an error occurred while attempting to commit:", e.args[0])

def create_job_posting_table(cursor):
    cursor.execute('''create table job_posting(
					SearchKey Text,
					SearchDate Date,
					JobID  Text,
	 				PostedDate Date,
					JobRole Text,
					Wage Text,
					Location Text,
					Employer Text,
					Summary Text,
					Experience Text,
					Sponsored_Ad Text,
					OnSite Text,
					CompanyURL Text,
					PRIMARY KEY (JobID, SearchKey)
					)'''
                   )
    commmit(cursor)

def lisf_of_list(in_l):
    #Checks if a list is a list of list or just a list
    if any(isinstance(s, list) for s in in_l):
        return(True)
    else:
        return(False)

def insert_into_job_posting(data, cursor):
    #a function that will drop the data into
    try:
        if(list_of_list(data)):
            for l in data:
                input_data = l[0] + [now()] + l[:len(l)] #inserting current date
                cursor.execute('insert into job_posting (?,?,?,?,?,?,?,?,?,?,?,?,?', input_data)
        else:
            input_data = data[0] + [now()] + data[:len(data)]
            cursor.execute('insert into job_posting (?,?,?,?,?,?,?,?,?,?,?,?,?', input_data)
    except:
        print("insert didn't work :(")

        
    commit(cursor)


def create_stats_table(cursor):
    cursor.execute('''
					crate table stats(
					SearchKey Text,
					SearchDate Date,
					stats_Group,
					stats_variable,
					stats_value_num,
					stats_value_txt,
					PRIMARY KEY (SearchKey, Stats_Group, Stats_Variable)
					)
	''')
    commmit(cursor)

def create_searchKey_ref_table(cursor):
    #create a refrence table so we can look up across various SearchKeys
    cursor.execute(''' 
                CREATE TABLE SearchKey_ref(
                SearchKey text,
                Job text,
                Salary int,
                Location text,
                JobType text,
                Company text,
                Experience text,
                Redius int,
                PRIMARY KEY (SearchKey)                
                )''')
    commit(cursor)

def insert_new_searchKey(Key, cursor):
    #takes a Key and inserts it into the SearchKey Ref Table
    Key_split = Key + Key.split('|')

    if(len(Key_split) != 7 ):
        print('Couldnt insert new Key, not enough elements')
        return(False)

    cursor.execute('insert into SearchKey_ref (?,?,?,?,?,?,?,?)', Key_split)
    commit(cursor)


def drop_main_tables(cursor):
    #easy function to drop the two main tables
    cursor.execute('drop table job_posting')
    cursor.execute('drop table stats')
    commit(cursor)

def sql(SQL_STATEMENT, cursor):
    #easy function to pass sql statement to the db at hand
    #ideally, I would use this as as age way to interact with the db
    cursor.execute(SQL_STATEMENT)
    commit(cursor)

def generate_base_stats_list(num_of_rows = 4):
    #makes the base list of list, remeber this is the formate
    #stats_Group,Stats_Var, stat_val,Stats_text
    out_list =  [['','','',''] for _ in range(num_of_rows)]
    return(out_list)

def remove_blank_rows(ltc):
    #this goes through the list of list (MUsT be a list of list) and removes any blank rows
    #walking down the list in reverse so that I can delete an element right there and befine
    if (any(isinstance(s, list) for s in ltc)):
        for l in range(len(ltc)-1,0,-1):
            #if the last two element are blank, then that row is empty
            if(ltc[i][len(ltc[i])-2:len(ltc[i])-1]==[[],[]]):
                del ltc[i]
    return(ltc)

def remove_previous_vers(Key ='', db = 'job_posting', cursor=''):
    #This function will remove data from the file of the previoul key so we can add new data to it (call if you want)
    sql_statement = 'delete from ' + db + ' where SearchKey=' + Key
    cursor.execute(sql_statement)
    commit(cursor)


def format_similar_jobs(sj):
    #formats the similar job statistics
    output_list = generate_base_stats_list(len(sj) - 1)
    for i in xrange(len(output_list)):
        j = jt[i + i]
        if j!=None:
            output_list[i][0] = 'Similar Jobs'
            output_list[i][1] = 'Similar Jobs'
            output_list[i][3] = j
    output_list = remove_blank_rows(output_list)
    return output_list

def formate_job_count(jc):
    out_list = generate_base_stats_list(len(jc)-1)
    for i in xrange(len(out_list)):
        j = jc[I+1]
        if j != None:
            out_list[i][0] = 'Job Count'
            out_list[i][1] = 'Job Count'
            out_list[i][2] = get_numbers(jc[j])
    output_list = remove_blank_rows(output_list)
    return(output_list)

def formate_salary_group(sg):
    #formats the salary group statistics
    output_list = generate_base_stats_list(len(sj) - 1)
    for i in xrange(len(output_list)):
        j = sg[i + 1]
        if j != None:
            j = j.replace('(',''),replace(')','').split(' ')
            if(len(j) == 2):
                output_list[i][0] = 'Salary Group'
                output_list[i][1] = j[0]
                output_list[i][2] = j[1]
            else:
                print('not enough job information')
    output_list = remove_blank_rows(output_list)
    return(output_list)

def formate_salary_range(sr):
    #formats the salary range ogroup statsicsts
    output_list = generate_base_stats_list(len(sr) - 1)

    for i in xrange(len(output_list)):
        j = i + 1 #adjusting the index up on (For the index of the sr)
        if sr[j] != None:
            output_list[i][0] = 'Salary Range'
            ''''['Salary Range', u'Cashier salaries in New York, NY', u'Min$7.25', u'$13.92 per hour', u'Max$34.50',
             u'Based on 2,342 salaries']'''
            if j == 1:
                output_list[i][1] = 'Salary Range Group'
                output_list[i][3] = sr[j]
            elif j ==2:
                temp = get_numbers(sr[j])
                output_list[i][1] = 'Min of Range'
                if(temp != []):
                    output_list[i][2] = float(temp[0])
            elif j == 3:
                output_list[i][1] = 'Mean of Range'
                temp = get_numbers(sr[j])
                if(temp != []):
                    output_list[i][2] = float(temp[0])
            elif j == 4:
                output_list[i][1] = 'Max of Range'
                temp = get_numbers(sr[j])
                if (temp != []):
                    output_list[i][2] = float(temp[0])
            elif j == 5:
                out_list[i][1] = 'Number of Subjects'
                temp = get_numbers(sr[j])
                if (temp != []):
                    output_list[i][2] = float(temp[0])
            else:
                print('there are more records in the salary range then expected...?')
    output_list = remove_blank_rows(output_list)
    return (output_list)

def formate_job_tpye(jt):
    output_list = generate_base_stats_list(len(jt) - 1)
    for i in xrange(len(output_list)):
        j = jt[i+i]
        if j != None:
            j = j.replace('(', ''), replace(')', '').split(' ')
            output_list[i][0] = 'Job Type Count'
            output_list[i][1] = j[0]
            output_list[i][2] = j[1]
    output_list = remove_blank_rows(output_list)
    return (output_list)

def stats_list_to_db(stats, searchDate = '1999-12-31', Key = '', cursor = None):
    #this takes a formate states list and drops it directly into the database, appending the key and serachdat to front
    if(cursor == None):
        print('No Cursor present')
        return(False)

    if (any(isinstance(s, list) for s in stats)):
        for s in stats:
            input_list = [Key, searchDate] + s
            if(len(input_list) ==6):
                cursor.execute('insert into stats (?,?,?,?,?,?)', input_list)
            else:
                print('couldnt input list into stats db, not enough elements')
    else:
        input_list = [Key, searchDate] + stats
        if (len(input_list) == 6):
            cursor.execute('insert into stats (?,?,?,?,?,?)', input_list)
        else:
            print('couldnt input list into stats db, not enough elements')
    commmit(cursor)

def insert_stats_data(stats, searchDate = '1999-12-31', Key = '', cursor=None):
    #this formate the output from the stats table into a usable format for the stats table
    if (cursor == None):
        print('No Cursor present')
        return (False)

    #check if it's a list OR a list of list (in which case we will need to work through each list seperatly:
    out_list = []
    if(any(isinstance(s, list) for s in stats)):
        for s in stats:
            insert_stats_data(s, searchDate, Key, cursor)
    else:
        if(stats[0] == 'Similar Jobs'):
            out_list = format_similar_jobs(stats)
        elif(stats[0] == 'Salary Range'):
            out_list = formate_salary_range(stats)
        elif(stats[0] == 'JobType Count'):
            out_list = formate_job_count(stats)
        elif(stats[0] == 'Number of Job Listings'):
            out_list = formate_job_type(stats)
        elif(stats[0] == 'Salary Group'):
            out_list = formate_salary_group(stats)
        else:
            print('the stats didnt confirm to one of the 5 types, so will not insert')

    if(out_list != []):
        stats_list_to_db(out_list, searchDate, Key, cursor)
    else:
        print('could not formate the data nor could I insert it, lo siento buddy')

def insert_into_job_posting2(jobposting, searchDate = '1999-12-31', Key = '', cursor=None):
    #insert job posting data into a db
    if (cursor == None):
        print('No Cursor present')
        return (False)

    key_header = [Key, searchDate]
    if (any(isinstance(j, list) for j in jobposting)):
        for j in jobposting:
            if(len(j)==12):
                cursor.execute('insert into job_posting (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', key_header + j)
            else:
                print('length of job posting is not the right size, was not inserted into db')
    else:
        if (len(jobposting) == 12):
            cursor.execute('insert into job_posting (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', key_header + jobposting)
        else:
            print('length of job posting is not the right size, was not inserted into db')
    commit(cursor)

