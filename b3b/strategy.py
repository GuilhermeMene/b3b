"""
Method for calculate the strategy using the indicators
"""

import pandas as pd
import pandas_ta as ta
from main import logger


def get_entry_exit(data:pd.DataFrame):
    """
    Method for calculate and populate the dataframe with entry and exit points
    """

    try:
        #Set the stoploss
        stoploss = 0.02

        #Calculating the indicators
        bb_len = 14
        bb = ta.bbands(data['Close'], length=14)
        data['rsi'] = ta.rsi(data['Close'], length=5)

        #Calculating the entry point
        data.loc[
            (
                (bb[f'BBL_{bb_len}_2.0'] > data['Low']) &
                (data['rsi'] < 30)
        ),
        'entry'] = 1

        #Calculating the exit point
        data.loc[
            (
                (bb[f'BBU_{bb_len}_2.0'] < data['High']) &
                (data['rsi'] > 70)
        ),
        'exit'] = 1

        return data, stoploss

    except Exception as e:
        logger.log(f'An error occurred calculating and populating the entry and exit point. \
                    Error: {e}')
