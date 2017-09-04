'''This is to help create, update, delete and maintain the Hive, and sqldb that holds all the tasks
their next location, as well as '''
import sqlite3
import datetime
import timedelta

class hive:
    def __init__(self, hive_loc = ''):
        if hive_loc == '':
            self.hiv_loc =''
            self.conn = ''
        else:
            try:
                self.conn = sqlite3.connect(hive_loc)
            except sqlite3.Error as e:
                print("an error occurred while attempting to connect to the hive:", e.args[0])
                self.conn = ''
            self.hiv_loc = hive_loc

    def make_hive(self,hive_loc):

        self.hive_loc = hive_loc
        try:
            #connectging to the datbase at a location
            self.conn =  sqlite3.connect(hive_loc)
            self.cusor = self.conn.cursor()

            self.make_hive_db()
            self.make_honeycomb_db()
            self.make_log_db()
            self.make_id_db()

        except sqlite3.Error as e:
            print("an error occurred while attempting to connect to the hive:", e.args[0])

    def commit_hive(self):
        if self.conn == '':
            print("Can't commit, their is no connection open")
        else:
            try:
                self.cursor.commit()
            except sqlite3.Error as e:
                print("an error occurred while attempting to commit:", e.args[0])

    def make_hive_db(self):
        '''create the hive db'''
        try:
            self.cursor.execut('''create table hive (
                                     task_id int,
                                     tasks_owner text,
                                     tasks_desc text,
                                     run_freq text,
                                     start_date date,
                                     start_time time,
                                     end_date date,
                                     update_date dat,
                                     next_tasks_id int,
                                     prev_tasks_id int,
                                     honeycomb_id int,
                                     PRIMARY KEY (task_id, honeycomb_id)
                                     )''')
            self.commit_hive()
        except sqlite3.Error as e:
            print("an error occurred while attempting to create the hive db:", e.args[0])
    def make_id_db(self):
        try:
            self.cursor.execut('''create table id_ref(
                                        id int,
                                        tasks_type text,
                                        PRIMARY KEY (id)
                                        ) on commit
                                        '''

    def make_honeycomb_db(self):
        '''create the honeycomb db'''
        try:
            self.cursor.execut('''create table honeycomb(
                                        honeycomb_id int,
                                        tasks_owner text,
                                        tasks_desc text,
                                        run_freq text,
                                        start_date date,
                                        end_date date,
                                        taks_info text,
                                        PRIMARY KEY (honeycomb_id)
                                        )
                            ''')
            self.commit_hive()
        except sqlite3.Error as e:
            print("an error occurred while attempting to create the honeycomb db:", e.args[0])

    def make_log_db(self):
        '''create the log db'''
        try:
            self.cursor.execut('''create table honey(s
                                    task_id int,
                                    honeycomb_Id int,
                                    queen_bee_id text,
                                    bee_name text,
                                    start_ts datetime,
                                    end_ts datetime,
                                    rerun_flag text,
                                    result text,
                                    error text,
                                    PRIMARY KEY (task_id, honeycomb_id)
                                    )''')

            self.commit_hive()

        except sqlite3.Error as e:
            print("an error occurred while attempting to create the log db:", e.args[0])

    def del_tasks(self, tasks_id, destory_honeycomb = True):
        #Delete a task sform the task db
        try:
            if destory_honeycomb:
                # getting the honeycomb ID
                self.cursor.execut("select honeycomb_id from hive where task_id = ?", tasks_id)
                honeycomb_id = self.cursor.fetchone()
                self.cursor.execut('delte from honeycomb where honeycomb_id = ?, honeycomb_id')

            self.cursor.execut("delete from hive where task_id = ?", tasks_id)
            self.commit_hive()

        except sqlite3.Error as e:
            print("an error occurred while attempting to delete the tasks db:", e.args[0])

    def create_tasks(self, id_dict):
        #A method to create a tasks in the Hive DB
        #I'm using a dict to copy the information over
        input_list = []

        #first is there a tasks id
        tasks_id = id_dict.get('tasks', 0)
        if tasks_id == 0:
            try:
                self.cursor.execut("select max(id) from id_ref where tasks_type = 'Task'")
                tasks_id =  self.cursor.fetchone() + 1
                self.cursor.execut("insert into id_ref ?,?", (tasks_id, "Task"))
                self.commit_hive()
            except sqlite3.Error as e:
                print("an error occurred while attempting to create a tasks id", e.args[0])

        input_list.append(tasks_id) # Tasks Id
        input_list.append(id_dict.get('owner', 'UNKNOWN')) # Owner
        input_list.append(id_dict.get("desc", '')) # Tasks Description
        input_list.append(id_dict.get('freq', "once")) #frequency
        #start time
        now = id_disct.get("start", 0)
        if now == 0:
            now = datetime.datetime.now()
            now = now + datetime.timedelta(hours=1)
        input_list.append(now.strftime("%Y-%m-%d")) #start Date
        input_list.append(now.strftime("%H:%M")) #Start Time
        input_list.append(id_dict("end", now + datetime.timedelta(days=1)).strftime("%Y-%m-%d")) #end date
        input_list.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        input_list.append(id_dict.get('next', None)) # Next Tasks
        Prev = id_dict.get('next', None)
        if Prev is not None:
            #lets see if the previous tasks exists
            self.conn.execute("select task_id where task_id = ?", Prev)
            if(len(self.conn.fetchone()) == 0):
                print("No Previous tasks with that tasks ID exists exists, just FYI")
        input_list.append(Prev) # Prev Tasks
        Honey = id_dect.get("honeycomb",None)
        if Honey is not None:
            self.conn.execute("select honeycomb_id where honeycomb_id = ?", Honey)
            if (len(self.conn.fetchone()) == 0):
                print("No Honeycomb with that tasks ID exists exists, just FYI")
        input_list.append(Honey)

        #okay, got the list all laid out, lets insert it into
        try:
            self.conn.execute('insert into hive ?,?,?,?,?,?,?,?,?,?,?', input_list)

        except sqlite3.Error as e:
            print("an error occurred while attempting to create a tasks id", e.args[0])

        return(0)

    def create_comb(self, comb_dict):
