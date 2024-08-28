"""
Logging all errors and results from backtesting
"""

import os

def set_path(path):
    """
    Method for set the log path in system environment
    """
    try:
        os.environ['LOGPATH'] = path
    except Exception as e:
        print('An error occurred. The log path cannot be defined.')

def log(logtext:str):
    """
    Method for save the log in text file
    """
    try:
        filedir = os.environ.get('LOGPATH')
        filepath = os.path.join(filedir, 'Log.txt')

        with open(filepath, 'a') as logfile:
            logfile.write(logtext + '\n')
            logfile.close()

    except Exception as e:
        print('An error occurred.The log path is inaccessible \
              or the the log path not in os environment.')

def save_trade(order, filepath:str, pricetype='High'):
    """
    Method for save the trades from backtesting
    """

    try:
        header = 'Datetime,Price,Quantity,Total,Type'

        if not os.path.exists(filepath):
            with open(filepath, 'w') as tfile:
                tfile.write(header + '\n')
                tfile.write(str(order) + '\n')
                tfile.close()
        else:
            with open(filepath, 'a') as tfile:
                tfile.write(str(order) + '\n')
                tfile.close()
    except Exception as e:
        print('An error occurred. The trades files is not acessible, and the trade result cannot be saved.')
