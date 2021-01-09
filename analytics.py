# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 17:09:18 2021

@author: Leon
"""
import sys
from base import load_obj, save_obj
import pandas as pd
from base import calculate_series_return

SPCOMPANIES = load_obj("SandP_Tickers")

calc_dict = load_obj("calc_dict")


# Calculate return if you buy on start date and sell on end date
def calc_simple_return(ticker):
    data = pd.read_csv(f"s_and_p_stock_data/{ticker}.csv", index_col = 0, parse_dates = True)
    data = data.sort_values(by = "Date")
    return calculate_series_return(data["Adj Close"][199:])
    

def calc_lw_sw_perf(calc_dict, q):
    sw_dict = {}
    lw_dict ={}
    sw_lw_dict = {}
    for each, cmp in zip(calc_dict.values(), calc_dict):
        try:
            n_quant = each[each["return"] >= each["return"].quantile(q)]
            for el in n_quant.iterrows():     
                el = el[1]
                if str(el.sw) in sw_dict.keys():
                    sw_dict[str(el.sw)] += 1
                else:
                    sw_dict[str(el.sw)] = 1
                    
                if str(el.lw) in lw_dict.keys():
                    lw_dict[str(el.lw)] += 1
                else:
                    lw_dict[str(el.lw)] = 1
                    
                if f"{el.sw}/{el.lw}" in sw_lw_dict.keys():
                    sw_lw_dict[f"{el.sw}/{el.lw}"] += 1
                else:
                    sw_lw_dict[f"{el.sw}/{el.lw}"] = 1
        except Exception as e:
            print(e)
            print(cmp)
            pass
    return sw_dict, lw_dict, sw_lw_dict


if __name__ == "__main__":
    sw_dict, lw_dict, sw_lw_dict = calc_lw_sw_perf(calc_dict, 0.9)
    cnt = 0
    cnt_strat = 0
    cnt_neg =0
    sum_s = 0
    sum_strat = 0
    for cmp in SPCOMPANIES:
        if cmp == "VNT":
            pass
        else:
            a = calc_simple_return(cmp)
            a_i = calc_dict[cmp]["return"].max()
            sum_s += a
            print(a_i)
            sum_strat += a_i
            
            if a < 1:
                cnt_neg += 1
                if a < a_i:
                    print(a, a_i)
                    cnt +=1
                
    

