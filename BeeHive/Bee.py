import getpass
import socket
class bee:
    '''This is the working bee, which is given a single tasks (pollen) to move between the flower, queen bee, and the
    hive. '''
    def __init__(self, bee_number = 1, location = "~", info = []):
        self.name = socket.gethostname() + ":" + getpass.getuser() + ":" + bee_number
        self.Queen = "Miss Piggy"
        self.WorkerNumber = bee_number
        self.alive = True
        self.pollen = ''
        self.Completed_Tasks = 0

    def PickUpPollen(self, tasks_type=[], task_location = [], ):
    def unpack_info(self):
        "This takes the info provided and unpacks it into a way thats easily readable by the system and hu-mans"
        "Struct of list is [Type, "
        len_of_info = len(self.info)


class pollen:
    '''This are the little nuggets that Bee's carry around: Bee's need to figure out where to bring it to/from
    Pollen needs to format itself to be usable by all systems'''
    def __init__(self, info ):
