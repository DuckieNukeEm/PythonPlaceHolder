import csv
from sodapy import Socrata
from calendar import monthrange
from datetime import datetime
from os import path


def connect_to_iowa_api():
    """connects to the iowa data portal via the socrata method"""
    return Socrata("data.iowa.gov", None)


def last_month():
    """calculates what last month is"""
    LastMonth = datetime.now().month - 1
    currentYear = datetime.now().year

    if LastMonth == 0:
        LastMonth = 12
        currentYear = currentYear - 1

    return currentYear, LastMonth


def month_start_end(year, month):
    """figures out the start date and end date for a given month, and
    returns it"""
    start_date = datetime(year, month, 1).strftime("%Y-%m-%d")
    end_date = datetime(year, month, monthrange(year, month)[1])
    end_date = end_date.strftime("%Y-%m-%d")

    return [start_date, end_date]


def pull_ils_data(
    client, start_date: str = None,
    end_date: str = None,
    limit: int = 200000000
):
    """pulls back the ils data set for a given start and end date"""
    return client.get(
        "m3tr-qhgy", where=f"date between '{start_date}' and '{end_date}'",
        limit=limit
    )


def fix_point(data):
    """convert the sub segement from "{type: point, coordinates: [lat, long]}"
     from the store_location field"""
    for i in data:
        if "store_location" not in i:
            continue
        if "coordinates" not in i["store_location"]:
            continue
        coord = " ".join([str(x) for x in i["store_location"]["coordinates"]])
        i["store_location"] = coord


def remove_time(Data):
    """removes the T00:00:00.000 from the date field"""
    for i in Data:
        if "date" not in i:
            continue
        else:
            str_date = i["date"]
            str_date = str_date.replace("T", "").replace("00:00:00.000", "")
            i["date"] = str_date


def write_to_csv_dict(Data, Path: str, headers: list = None):
    if not headers:
        headers = Data[0].keys()
    with open(Path, "w", newline="") as f:
        dw = csv.DictWriter(f, headers)
        dw.writeheader()
        dw.writerows(Data)


def write_to_csv_list(Data, Path: str, headers: list = None):
    with open(Path, "w", newline="") as f:
        dw = csv.writer(f)
        if headers:
            dw.writerow(headers)
        dw.writerows(Data)


def pull_ils(
    year: int = None,
    month: int = None,
    last_month: bool = True,
    save_loc: str = None,
    file_name: str = None
):

    if year and month:
        pass
    else:
        year, month = last_month()

    date_range = month_start_end(year, month)

    if file_name is None:
        file_name = 'ils_' + str(year) + '_' + str(month) + '.csv'
    if file_name.startswith('/') or file_name.startswith("\\"):
        file_name = file_name[1:]

    if save_loc is None:
        save_loc = '.'

    save_path_file = path.join(save_loc, file_name)

    # connecting to client
    client = connect_to_iowa_api()

    data = pull_ils(client, date_range[0], date_range[1])

    if len(data) == 0:
        return None

    # fixing the data
    fix_point(data)
    remove_time(data)

    orig_data_headers = [
        "invoice_line_no",
        "date",
        "store",
        "name",
        "address",
        "city",
        "zipcode",
        "store_location",
        "county_number",
        "county",
        "category",
        "category_name",
        "vendor_no",
        "vendor_name",
        "itemno",
        "im_desc",
        "pack",
        "bottle_volume_ml",
        "state_bottle_cost",
        "state_bottle_retail",
        "sale_bottles",
        "sale_dollars",
        "sale_liters",
        "sale_gallons",
    ]
    data_headers = [
        "item_invoice_nbr",
        "order_dt",
        "store_nbr",
        "store_name",
        "store_address",
        "store_city",
        "zip_code",
        "store_location",
        "county_nbr",
        "county_name",
        "category_nbr",
        "category_name",
        "vendor_nbr",
        "vendor_name",
        "item_nbr",
        "item_desc",
        "pack",
        "bottle_vol",
        "state_bottle_cost",
        "state_bottle_retail",
        "bottles_sold",
        "sale",
        "volume",
        "volume_gallons",
    ]
    # fixing headers
    data_fix = [[i.get(header) for header in orig_data_headers] for i in data]
    data_fix = [data_headers] + data_fix

    if save_loc:

        write_to_csv_list(
            data_fix,
            save_path_file,
        )
        return True
    else:
        return data_fix

    return None


if __name__ == "main":
    pull_ils()
