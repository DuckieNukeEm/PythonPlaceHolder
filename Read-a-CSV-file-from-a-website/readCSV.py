import urllib2
import csv

f = open("~/Documents/Congressional District.csv", "w")


with open("c:/scripts/CSVforcensus.csv") as fp:
    for line in fp:
        #the line we are using
        print(line)
        try:
            #getting the file
            response = urllib2.urlopen(line)
            #printing the row as well as writing it
            for row in response:
                print(row)
                f.write(row)
        except urllib2.URLError:
            print("error")
            continue
f.close()
