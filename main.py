"""
B3B class file
"""

import os
import re
import sys
from datetime import datetime
import pandas as pd
from b3b import logger
from b3b import strategy
import yfinance as yf
from tabulate import tabulate


class B3B:
    def __init__(self, ticker, timeframe, timerange, pricetype):

        #Set the initial parameters
        self.timeframe = timeframe
        self.timerange = timerange
        self.ticker_name = ticker

        self.pricetype = pricetype

        #Set the date
        self.date = datetime.today().strftime('%Y-%m-%d-%H:%M')

        #Set the balance
        self.money_balance = 10000.0

        #Set the ticker
        self.ticker = yf.Ticker(str(ticker))

        #Set the log path
        logger.set_path(os.getcwd())

    def runTask(self):
        """
        Method for automate the backtesting process
        """
        try:
            #Get the data
            self.get_data()

            #Get the strategy
            self.get_strategy()

            #Run the backtest using high price
            self.run_backtesting()

            #Make the report of the backtest runned using the High
            self.make_report()

        except Exception as e:
            logger.log(f'An error occurred running the backtest. Error: {e}')

    def get_data(self):
        """
        Method for download stock data
        """
        try:
            print(' +++ Getting data')
            if len(self.timerange) > 3:
                reg = "[0-9]{4}\\-[0-9]{2}\\-[0-9]{2}"
                daterange = re.findall(reg, self.timerange)

                start = daterange[0]
                end = daterange[1]
                self.hist_data = self.ticker.history(
                    interval=self.timeframe,
                    start=start,
                    end=end
                )
            else:
                self.hist_data = self.ticker.history(
                    interval=self.timeframe,
                    period=self.timerange
                )
        except Exception as e:
            logger.log(f'Error getting data: {e}')

    def get_strategy(self):
        """
        Method for get strategies
        """
        try:
            self.tickerdata, self.stoploss = strategy.get_entry_exit(self.hist_data)
        except Exception as e:
            logger.log(f'Error getting strategy: {e}')

    def run_backtesting(self):
        """
        Method for run the backtesting
        """
        try:
            #Set the path of trades
            self.trade_path = f'Trades_{self.ticker_name}_{self.pricetype}_{self.date}.csv'

            print('Running the bot...')
            self.qty = 0
            self.long = False
            self.lastLongPrice = 0
            for i, row in self.tickerdata.iterrows():
                #Set the long order
                if row['entry'] == 1 and self.long == False and self.money_balance > row[self.pricetype]:
                    print(' *** Making long')
                    price = row[self.pricetype]
                    self.qty = int(self.money_balance/price)
                    total = float(self.qty * price)
                    datetime = row.name

                    print(' ---Saving the order')
                    trade = f'{datetime},{round(price,2)},{self.qty},{round(total,2)},LONG'
                    logger.save_trade(trade, self.trade_path, pricetype=self.pricetype)

                    self.money_balance = float(self.money_balance % price)
                    self.long = True
                    self.lastLongPrice = price

                # Set the short order
                elif row['exit'] == 1 and self.long == True and self.qty > 0:
                    print(' *** Making short')
                    price = row[self.pricetype]
                    total = float(price * self.qty)
                    datetime = row.name

                    print(' ---Saving the order')
                    trade = f'{datetime},{round(price,2)},{self.qty},{round(total,2)},SHORT'
                    logger.save_trade(trade, self.trade_path, pricetype=self.pricetype)

                    self.long = False
                    self.money_balance = total
                    self.qty = 0

                # Set the stop loss
                elif self.long == True and row[self.pricetype] < (self.lastLongPrice - (self.lastLongPrice * self.stoploss)):
                    print(' *** Making short - STOPLOSS')
                    price = row[self.pricetype]
                    total = float(price * self.qty)
                    datetime = row.name

                    print(' ---Saving the order')
                    trade = f'{datetime},{round(price,2)},{self.qty},{round(total,2)},STOPLOSS'
                    logger.save_trade(trade, self.trade_path, pricetype=self.pricetype)

                    self.long = False
                    self.money_balance = total
                    self.qty = 0

        except Exception as e:
            logger.log(f'Backtesting running error: {e}')

    def make_report(self):
        """
        Method for make backtesting reports
        """
        try:
            filepath = f'Trades_{self.ticker_name}_{self.pricetype}_{self.date}.csv'
            if os.path.exists(filepath):

                data = pd.read_csv(filepath, delimiter=',')

                #Get the number of each trade type
                long = len(data['Type'][data['Type'] == 'LONG'])
                short = len(data['Type'][data['Type'] == 'SHORT'])
                stop = len(data['Type'][data['Type'] == 'STOPLOSS'])

                first = data.head(1)
                last = data.tail(1)

                tdiff_pc = ((last['Total'].values - first['Total'].values) / first['Total'].values) * 100.0
                tdiff = (last['Total'].values - first['Total'].values)
                profit = last['Total'].values - 10000.0
                minb = min(data['Total'])
                maxb = max(data['Total'])

                print(f' *** Reporting the results using the *{self.pricetype}* prices.')
                table = [['Nº of trades:', len(data)],
                        ['Total Difference:', round(tdiff[0], 2)],
                        ['Total Diff (%):', round(tdiff_pc[0], 2)],
                        ['Profit (R$):', round(profit[0], 2)],
                        ['Max balance (R$):', round(maxb, 2)],
                        ['Min balance (R$):', round(minb, 2)],
                        ['Long:', long],
                        ['Short:', short],
                        ['Stoploss:', stop]]

                #Print the report
                print(tabulate(tabular_data=table, tablefmt='outline', numalign='right'))
            else:
                print('The backtesting did not result in any trades to report...')

        except Exception as e:
            logger.log(f'An error occurred making the report. Error: {e}')


if __name__ == '__main__':

    #Check the length of the sys argvs
    if len(sys.argv) != 5:
        print("The usage of the tool is: python b3b.py ticker timeframe timerange price")
        sys.exit(1)
    else:
        b3b = B3B(
            ticker=sys.argv[1],
            timeframe=sys.argv[2],
            timerange=sys.argv[3],
            pricetype=sys.argv[4]
        )
        b3b.runTask()
