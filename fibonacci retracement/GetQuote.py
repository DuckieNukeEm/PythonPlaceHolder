import urllib.request
import os
import numpy as np
import csv

base_url = "http://ichart.finance.yahoo.com/table.csv?s="
def make_url(ticker_symbol):
    return base_url + ticker_symbol

def path_exists(f):
    if not os.path.exists(f):
        os.makedirs(f)

def make_filename(ticker_symbol, output_path, directory="Quote" ):
    return output_path + "/" + directory + "/" + ticker_symbol + ".csv"

def pull_historical_data(ticker_symbol, output_path, directory="Quote"):
    try:
        path_exists(output_path + directory)
        urllib.request.urlretrieve(make_url(ticker_symbol),
                                   make_filename(ticker_symbol, output_path = output_path, directory=directory))
        return('Downloaded')
    except urllib.error.HTTPError as e:
        return(e)
    except urllib.error.URLError as e:
        return(e)
    except urllib.ContentTooShortError as e:
        outfile = open(make_filename(ticker_symbol, directory), "w")
        outfile.write(e.content)
        outfile.close()
        return('Not all data returned')

def get_all_stock_symbols(directory = "List", output_path = "C:/Scripts/Python" ):
    path_exists(output_path + "/" + directory)
    urllib.request.urlretrieve("http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE&render=download",
                               make_filename('CompanyList',output_path=output_path, directory = directory))

def get_quotes(ticker_dir = "Quote", master_list = 'List',output_path = "C:/Scripts/Python" ):
    #getting a fresh list of all the stocks
    get_all_stock_symbols(directory = master_list, output_path = output_path);

    #reading in that list
    with open(output_path+"/"+master_list+"/CompanyList.csv", 'r') as f:
        all_stocks = list(csv.reader(f))
    all_stocks[0][9] = "Download Results"

    #checking the location of where I'm going to save my files
    path_exists(output_path + "/" + ticker_dir  )

    #getting historic stock information from all stocks on the company lists
    for i in range(1,len(all_stocks[1:])):
       all_stocks[i][9]  = pull_historical_data(all_stocks[i][0], output_path = output_path)
       print("Stock we are looking at:" , all_stocks[i][0], '\t results is:', all_stocks[i][9])

    #writing results to the file again
    with open(output_path+"/"+master_list+"/CompanyList.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(all_stocks)



get_quotes()
