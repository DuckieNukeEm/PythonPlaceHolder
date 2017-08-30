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
