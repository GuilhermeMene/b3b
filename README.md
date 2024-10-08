## B3B
A free and open source backtesting tool designed for use in stocks listed on B3 Brazil

The B3B offers a set of tool for implement and testing strategies on stocks candles.

The B3B strategy file calculate and populate the *entry* and *exit* points on the candle dataframe.

The backtesting have a simulated wallet with R$ 10.000,00 and place the order according the strategy.


### Default strategy
The defautl strategy was based in the combination of RSI and Bollinger Bands using the follow condition:
```
The backtest will make a long if:
    rsi < 30 AND
    lower band > low price

The backtest will make a short if:
    Have done a long before AND
    rsi > 70 AND
    upper band < high price

```
#### It is strongly recommended that you edit the strategy file for your own testing!
The strategy indicators can be calculated using the [pandas-ta](https://github.com/twopirllc/pandas-ta).

### Quickstart
With the Docker installed:

```
# Clone the github repository:

>> git clone https://github.com/GuilhermeMene/b3b.git

>> cd b3b

# Build the Docker image and run the default backtesting (ticker=B3SA3.SA timeframe=1d timerange=2024-01-01-2024-08-01 price=Close):

>> docker compose up
```

### Basic usage of the tool
```
>> docker compose run --rm b3b sh -c "python main.py TICKER TIMEFRAME TIMERANGE PRICE"

# Example of usage for PETR4 using 1d timeframe, calculating the last 3 mounths, and using the close price:

>> docker compose run --rm sh -c "python main.py PETR4.SA 1d 3mo Close"
```

### Standalone Python distribution

Make sure that have the installed dependencies:
```
pandas-ta >= 0.3.14b
pandas >= 2.2.1
numpy >= 1.26 and <2.0
yfinance >= 0.2.40
setuptools > 0.72
tabulate > 0.8.9

# To install the dependencies using pip:
>> pip install -r requirements.txt
```

The B3B is licensed under [MIT License](https://github.com/GuilhermeMene/b3b/blob/main/LICENSE)