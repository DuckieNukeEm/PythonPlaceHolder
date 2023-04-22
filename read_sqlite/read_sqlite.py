import sqlite3
import io


def connect(Path: str):
    try:
        conn = sqlite3.connect(Path)
        print("Connection is established successfully!")
        print("'originaldatabase.db' is created ")
        return conn

    except Exception as E:
        print(E)

    finally:
        conn.close()


class SQL():
    def __init__(self, Path: str):
        self.Con = connect(Path)
        self.Cursor()

    def Cursor(self):
        self.Cur = self.Con.cursor()

    def commit(self):
        self.Cur.commit()

    def list_tables(self):
        return(self.sqlf('select name from sqlite_master where type="table"'))

    def sql(self, SQL_str: str):
        return(self.Cur.execute(SQL_str))

    def sqlf(self, SQL_str: str):
        return(self.Cur.execute(SQL_str).fetchall())
    
    def table_schema(self, table: str, return_str: bool = False):
        if return_str:
            print(self.sqlf(f"select sql from sqlite_master where type='table' and name = '{table}'")[0][0])

