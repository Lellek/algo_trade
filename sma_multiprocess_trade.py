# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 20:48:52 2021

@author: Leon
"""

from base import load_obj, save_obj, getsma, calculate_series_return
import pandas as pd
import multiprocessing as mp
import time
import logging
import math
import datetime

SPCOMPANIES = load_obj("SandP_Tickers")
logging.basicConfig(filename='Multi.log', level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())

# beide Ranges auch niedriger starten lassen nächstes mal
SW_RANGE = range(50,51,5)
LW_RANGE = range(200,201,10)


    
def create_Trade_df(df, shortwindow, longwindow):
    dfTrade = pd.DataFrame(df["Adj Close"])
    dfTrade["short"] = getsma(dfTrade, shortwindow)
    dfTrade["long"] = getsma(dfTrade, longwindow)
    dfTrade = dfTrade[199:]  # Anstatt größt möglichen Zeitraum lieber konstant wegschneiden für bessere Vergleichbarkeit
    # dfTrade = dfTrade[longwindow-1:]
    return dfTrade


def buy(price, money, trade_fee):
    stock = math.floor(money/price)
    new_money = money-stock*price-(stock*price*trade_fee)
    while new_money < 0:
        stock += - 1
        new_money = money-stock*price-(stock*price*trade_fee)
        
    return stock, new_money

def sell(price, money, stock, trade_fee):
    money += price * stock-(stock*price*trade_fee)
    return money


# Trading strat: sell if sma_sw < sma_lw 
def smatrade(stock_history , shortWindow, longWindow, money, trade_fee):
    dfTrade = create_Trade_df(stock_history, shortWindow, longWindow)
    capital = [[money, 0]]
    bought = False
    stock = 0    
    for index, row in dfTrade.iterrows():
        traded = 0
        if bought:    
            if row["short"] < row["long"]:
                money = sell(row["Adj Close"], money, stock, trade_fee)
                stock = 0
                bought = False
                traded = 1
        else:
            if row["short"] > row["long"]:
                stock, money = buy(row["Adj Close"], money, trade_fee)
                bought = True
                traded = 2            
        capital.append([stock*row["Adj Close"]+money, traded])
    ind = list(dfTrade.index)
    first_date = ind[0] - datetime.timedelta(1)
    ind = [first_date] + ind
    capitalindexed = pd.DataFrame(index=ind, data = capital, columns = ["capital", "trade"])
    
    return capitalindexed


def perform_trade(ticker, sw_range = SW_RANGE, lw_range= LW_RANGE, money= 10000, trade_fee = 0.0025):
    start = time.time()
    l = []
    try:
        stock_history = pd.read_csv(f"s_and_p_stock_data/{ticker}.csv", index_col = 0, parse_dates = True)
        for sw in sw_range:
            for lw in lw_range:               
                capital = smatrade(stock_history, sw, lw, money, trade_fee)
                l.append({"return": calculate_series_return(capital["capital"]), "capital": capital, "sw": sw, "lw": lw})
        logging.info(f"{ticker}: Done DURATION: {time.time()-start}")
        return pd.DataFrame(l)
    except Exception as e:
        logging.error(f"{ticker} macht Faxxen \n {e}")
        pass
 
    
def single_process():
    return [perform_trade(ticker) for ticker in SPCOMPANIES]

def multi_process_map():
    with mp.Pool() as p:               
        return p.map(perform_trade, SPCOMPANIES[:1])


if __name__ == "__main__":
    start = time.time()
    multi_ret = multi_process_map()
    multi_ret_dict= {}
    # for ticker, data in zip(SPCOMPANIES,multi_ret):
    #     multi_ret_dict[ticker] = data
    # save_obj(multi_ret_dict, "S_P500_sma_calculation")
    duration_multi = time.time()-start
    logging.info(f"Multi Process map: {duration_multi}")
    
