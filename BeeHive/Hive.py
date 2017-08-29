'''This is to help create, update, delete and maintain the Hive, and sqldb that holds all the tasks
their next location, as well as '''
import sqlite3

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
            self.conn =  sqlite3.connect(hive_loc)
    







#https://docs.python.org/2/library/sqlite3.html
