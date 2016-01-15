import csv
import xlrd
import string

dir_location = "~/Python/"

fp = [line.strip() for line in open("c:/scripts/excelfiles.csv", 'r')]

for fpline in fp:

    #creating the save string for the CSV file
    print(fpline)
    csvstring = string.split(string.split(fpline,"/")[-1], ".")[0]
    #opening Excel
    workbook = xlrd.open_workbook(fpline,)

    #copying Data from the DAta tab
    with open(''.join([dir_location,csvstring," Data.csv"]),'wb') as csvdatafile:
        sh = workbook.sheet_by_name('Data')
        wr = csv.writer(csvdatafile, quoting=csv.QUOTE_ALL)
        for rownum in xrange(sh.nrows):
            wr.writerow(sh.row_values(rownum))
    csvdatafile.close()


    #copying data from the Cobra tab
    with open(''.join([dir_location,csvstring," COBRA.csv"]),'wb') as csvdatafile:
        sh = workbook.sheet_by_name('Cobra')
        wr = csv.writer(csvdatafile, quoting=csv.QUOTE_ALL)
        for rownum in xrange(sh.nrows):
            wr.writerow(sh.row_values(rownum))
    csvdatafile.close()

    #cleaning everything up
    workbook.release_resources()
fp.close()
