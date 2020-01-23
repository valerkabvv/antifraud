from scipy.stats import vonmises_line
import numpy as np
from datetime import datetime
import pandas as pd


def hours_diff(t1, t2):
    pattern = '%Y-%m-%d %H:%M:%S'
    tdelta = datetime.strptime(t1, pattern) - datetime.strptime(t2, pattern)
    return tdelta.days*24 + tdelta.seconds//3600


def sec_diff(t1, t2):
    pattern = '%Y-%m-%d %H:%M:%S'
    tdelta = datetime.strptime(t1, pattern) - datetime.strptime(t2, pattern)
    return tdelta.days*24*3600 + tdelta.seconds


def calculate_hours(time_list):

    '''
    Функция возвращает список моментов времени в часах, от 0:00, отображенный на отрезок [-Pi;Pi]
    '''

    pattern = '%Y-%m-%d %H:%M:%S'
    starting_time = datetime.strptime('2019-01-01 0:0:0', pattern)
    dtime_list = []
    for time in time_list:
        d = starting_time - time
        dtime_list.append(d.seconds / 3600)
    return (np.array(dtime_list) / 12 * np.pi) - np.pi


def return_hours(time):

    '''
    Функция возвращает список моментов времени в часах, от 0:00, отображенный на отрезок [0;24], принимая [-2Pi;2Pi]
    '''
    if time>0:
        return time*12/np.pi
    return (time+2*np.pi)*12/np.pi


def is_in_interval(mu, std, values):
    values = calculate_hours(values)
    counter=0
    vonmises = vonmises_line(kappa = 1/std, loc= mu)
    interval = vonmises.interval(0.8)
    l = interval[0]
    r = interval[1]

    if l<r:
        for v in iter(values):
            if v> l and v < r:
                counter += 1
    else:
        for v in iter(values):
            if v > l or v < r:
                counter += 1
    return counter/len(values)


def calculate_periodic_mean(dtime_list):
    dtime_list = np.array(dtime_list)
    sin = np.sin(dtime_list).sum()
    cos = np.cos(dtime_list).sum()
    mean = sin/(np.sqrt(np.power(sin, 2)+np.power(cos, 2))+cos)
    return 2*np.arctan(mean)


def calculate_periodic_std(dtime_list):
    dtime_list = np.array(dtime_list)
    sin = np.sin(dtime_list).mean()
    cos = np.cos(dtime_list).mean()
    std = np.sqrt(np.log(1/(np.power(sin, 2)+np.power(cos, 2))))
    return std


def mu_std_calculation(path):

    '''

    :param path: path to transaction history
    :return: DataFrame, with columns: user_id, mu, std
    '''

    tr_hist = pd.read_csv(path)
    tr_hist.date_time = pd.to_datetime(tr_hist.date_time, format='%Y%m%d %H:%M:%S.%f')
    tr_hist = tr_hist[["user_id", "date_time"]]
    mu = tr_hist.groupby("user_id").agg(lambda x: calculate_periodic_mean(calculate_hours(x)))
    std = tr_hist.groupby("user_id").agg(lambda x: calculate_periodic_std(calculate_hours(x)))
    data = pd.concat([mu, std], axis=1)
    data.columns = ["mu", "std"]

    return data

