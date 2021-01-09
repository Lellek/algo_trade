# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 22:57:48 2021

@author: Leon
"""
import pickle


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
    
def getsma(df, window):
    d = df["Adj Close"].rolling(window = window).mean()
    return d   

# tbd: auf gewissen Zeitraum normen
def calculate_series_return(series):
    try:
        return series[-1]/series[0]
    except:
        return None