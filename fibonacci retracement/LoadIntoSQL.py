__author__ = 'Asmodi'

import csv
import sqlite3 as sq
import os

connection = 'C:/scripts/Stock.sqlite'

conn = sq.connect(connection)
c = conn.cursor()

#drop and create table:
c.execute("Drop Table Stock")
c.execute(
    """CREATE TABLE Stock
    (Stock CHAR NOT NULL ,
    Date DATETIME NOT NULL ,
	Open Double,
     High DOUBLE,
     Low DOUBLE,
     Close DOUBLE,
     Volume DOUBLE,
    Adj_Close DOUBLE,
    PRIMARY KEY (Stock, Date))"""
)
execute_script = "insert into Stock(Stock, Date, Open, High, Low, Close, volume, Adj_Close) VALUES (?,?,?,?,?,?,?,?)"

stock_source = "c:/scripts/Python/Quote/"
Quote_List = os.listdir(stock_source)
for q in Quote_List:
	print("Working on Stock %s" % q)
	stock_name = q.split(".")[0]
	header = 1
	with open(stock_source + q, 'r') as f:
		s = csv.reader(f)
		next(s)
		for row in s:
			row.insert(0,stock_name)
			print(row)
			try:
				print("Good \n")
				c.execute(execute_script, row)
			except:
				print("Unable to load data")
	conn.commit()
			
			

