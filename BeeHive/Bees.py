import pyodbc
import getpass
import socket
class bee:
    '''This is the working bee, which is given a single item to manange and work through'''
    def __init__(self, bee_number, location = "~", info = []):
        self.name = socket.gethostname() + ":" + getpass.getuser()
        self.WorkerNumber = bee_number
        self.alive = True
        self.pollen = self.add_pollen()

    def unpack_info(self):
        "This takes the info provided and unpacks it into a way thats easily readable by the system and hu-mans"
        "Struct of list is [Type, "
        len_of_info = len(self.info)

    class Flower:
        "flower class: (basically what type of thing the be is going to do"
        def __init__(self, info):
            if info[0] == "query":
                self.type = "query"
                self.db = info[1]
                self.delim = info[2]
                self.to = info[3]
                self.pw_loc = info[4]

            elif info[0] == "script":
                self.type = "script"
                self.location = info[1]
                self.interperter = info[2]
            elif info[0] == "scrapper"
                self.type = "scrapper"
                self.http_loc = info[1]
                self.save_loc = info[2]
            else:
                self.type = "cmd"
                self.cmd_string = ""
        def add_
        def land_on_flower(self):
            "figure out what to do when the bee lands on the flower"
            if self.type == "query":
                self.callqueryrun()
            elif self.type == "script":
                self.scriptrunner()
            elif self.type == "scrapper"
            else:
                self.cmd_command()

        def callqueryrun(self):
            "runs a query"
            if left(self.db,2) == 'WM':
                cnxn_string = 'DSN='+self.db
            else cnxn_string = "DSN="+self.db +";UID" = seld.user + ";PWD=" self.pw
                cnxn = pyodbc.conection('DSN=' + self.db)


'''Notes:
    *Working bee just caries around information and tasks
    *Flowers are what execute the tasks (bee's bring them the infromation, flowers execute, bee's return to diposate
        everything else or to move to the next tasks on that list
    *Pollen are the tasks themselves
    *Hive is a centralized location of all the tasks, the run dates, and so forth (thinking sqllight db) a hive should have
        Multiple machiens should hit one hive at a time. for reduancdy sake
        -Name of the tasks
        -When it should be run
        -What the tasks is
        -Did it run
        -who last was running it
        -the next step in the process
    *Queen bee
        She makes  delegates tasks to the workers
        updates the hive (And checks in on it every 5 or 10 minutes)
        each machine will have one queen bee!
        
        https://www.programiz.com/python-programming/class'''
        
    
