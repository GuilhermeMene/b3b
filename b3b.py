"""
B3B class file 
"""
import sys 
import pandas as pd 

class B3B:
    def __init__(self, timeframe, timerange, strategy, pricetype):
        self.timeframe = timeframe
        self.timerange = timerange
        self.strategy = strategy
        self.pricetype = pricetype

    def get_data(self):
        """
        Method for download stock data
        """

    def get_indicators(self):
        """
        Method for calculate and populate the dataframe
        with indicators 
        """

    def run_backtesting(self):
        """
        Method for run the backtesting calling the backtesting file
        """

    def make_report(self):
        """
        Method for make backtesting reports 
        """