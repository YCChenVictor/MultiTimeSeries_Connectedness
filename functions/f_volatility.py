# import required modules
import numpy as np
import datetime
import pandas as pd
# =================================


def yang_zhang_volatility(data, n=2, clean=False):
    """
    :param data: a list with Open, High, Low, Close price
    :param n: the periods to obtain the average volatilitys
    :param clean: If clean, then delete the NA values
    :return: A list of volatility data
    """
    # define required variables
    o_c = (data['Open'] / data['Close'].shift(1)).apply(np.log)
    c_o = (data['Close'] / data['Open']).apply(np.log)
    h_o = (data['High'] / data['Open']).apply(np.log)
    l_o = (data['Low'] / data['Open']).apply(np.log)

    # overnight volatility
    vo = o_c.rolling(window=n).apply(np.var, raw=True)

    # today(open to close) volatility
    vt = c_o.rolling(window=n).apply(np.var, raw=True)

    # rogers-satchell volatility
    rs_fomula = h_o * (h_o - c_o) + l_o * (l_o - c_o)
    rs = rs_fomula.rolling(window=n, center=False).sum() * (1.0 / n)

    # super parameter
    k = 0.34 / (1 + (n + 1) / (n - 1))

    # yang-zhang
    result = (vo + k * vt + (1 - k) * rs).apply(np.sqrt)

    if clean:
        return result.dropna()
    else:
        return result


def daterange(date1, date2):
    """
    :param date1: start date
    :param date2: end date
    :return: a list of date
    """
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + datetime.timedelta(n)


def date_format(date):
    list_date = date.split("-")
    year, month, day = list_date[0], list_date[1], list_date[2]
    return datetime.date(int(year), int(month), int(day))


class volatility:

    def __init__(self, names, csv_files, path, start_dt, end_dt):

        # The variables we need to launch this class
        # the names of the volatility
        self.names = names
        # the path filled timeseries data going to calculate volatility
        self.path = path
        # the names of the csv file in the given path
        self.csv_files = csv_files
        # the start date of the volatility data
        self.start_dt = date_format(start_dt)
        # the end date of the volatility data
        self.end_dt = date_format(end_dt)
        # Variable generated in price_data_to_volatility
        self.dict_data = None
        # Variable generated in periods_of_volatility
        self.dataframe = None

    # read the price data, set up dictionary and then calculate the volatility
    def price_data_to_volatility(self):

        names = self.names
        csv_files = self.csv_files

        dict_data = {}  # the dictionary
        for i in range(len(names)):
            dict_data[names[i]] = pd.read_csv(self.path + "/" + csv_files[i])

        # deal with the Non-data problem
        for i in range(len(dict_data)):
            dict_data[names[i]] = dict_data[names[i]].interpolate()

        for i in range(len(dict_data)):
            vol_name = names[i] + "_" + "volatility"
            dict_data[names[i]][vol_name] = yang_zhang_volatility(dict_data[names[i]])

        self.dict_data = dict_data

    # obtain specify periods of volatility
    def periods_of_volatility(self):

        list_date = []

        for dt in daterange(self.start_dt, self.end_dt):
            list_date.append(dt.strftime("%Y-%m-%d"))

        # specify date here, create specified Date data
        dataframe = pd.DataFrame({'Date': list_date})

        dict_data = self.dict_data
        names = self.names

        for i in range(len(dict_data)):
            volatility = dict_data[names[i]].iloc[:, [0, -1]]
            dataframe = dataframe.merge(volatility, on='Date')

        self.dataframe = dataframe
