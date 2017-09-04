'''
This is for the Queen Bee Class,
The queen bee is what monitars the hive, determines what tasks need to be run, gives those tasks to workers
makes workers, checks in on the workers, and updates the Hive
'''
import datetime
import getpass
import socket
import os
info_dict = {'PASSWORD FILE': path('C:/SCRIPTS/USERPW.TXT')


}

class Queenbee:

    def __init__(self, name = 'BuzzKil', hive):
        dt_time = datetime.datetime.now()
        dt_time = 10000000000 * dt_time.year +100000000 * dt_time.month + 1000000 * dt_time.day * 10000 * dt_time.hour + 100 * dt_time.minute + dt_time.second
        self.bees_alive = 0
        self.bees_dead = 0
        self.tasks_complete = 0
        self.create_ts = dt_time
        self.name = socket.gethostname() + ":" + getpass.getuser() + ":" name
        self.hive = hive
        self.bees = []
        self.info_loc = info_dict

    def create_bee(self, task):
        bee_id = 1
        for b in self.bees:
            if b.bee_id >= bee_id:
                bee_id = b.bee_id +1
        self.bees_alive = self.bees_alive + 1
        new_bee = Bee(Queen = self.name,
                      bee_number = self.bees_alive + self.bees_dead + 1
                      task,)
        new_bee.tasks = task
        self.bees.append(new_bee)

        self.bees.append(new_bee)

    def check_bee(self,):

def figure_out_tasks(bee):
    if bee.alive ="F"


