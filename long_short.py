#Jacob Carroll Long/Short Trading Strategy on Nike and Footlocker
from scipy import stats
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta, date
import numpy as np
from scipy.stats import linregress
import math

def getData(start, end): 
    FL_ticker = 'FL'
    NKE_ticker = 'NKE'
    fltickerData = yf.Ticker(FL_ticker)
    nketickerData = yf.Ticker(NKE_ticker)

    #Call data from yfinance
    fldf = fltickerData.history(interval='1d', start=start, end=end)
    nkedf = nketickerData.history(interval='1d', start=start, end=end)
    fldf = fldf[['Open']] 

    #Convert fldf, nkedf to readable pandas dataframe
    fldf.rename(columns={'Open': 'FLOPEN'}, inplace=True) 
    fldf.reset_index(inplace=True)
    fldf['Date'] = fldf['Date'].dt.strftime('%Y-%m-%d')
    fldf.to_dict(orient='records')
    nkedf = nkedf[['Open']]
    nkedf.rename(columns={'Open': 'NKEOPEN'}, inplace=True)
    nkedf.reset_index(inplace=True)
    nkedf['Date'] = nkedf['Date'].dt.strftime('%Y-%m-%d')
    nkedf.to_dict(orient='records')
    fldf.Date = pd.to_datetime(fldf.Date) 
    fldf.set_index("Date", inplace = True) 
    nkedf.Date = pd.to_datetime(nkedf.Date) 
    nkedf.set_index("Date", inplace = True)
    
    #Merge the two dataframes
    jointdf = pd.concat([nkedf, fldf], join='inner', axis=1)

    #Make daily chane metric
    jointdf['FL_Daily_Change'] = jointdf['FLOPEN'].pct_change() * 100
    jointdf['NKE_Daily_Change'] = jointdf['NKEOPEN'].pct_change() * 100

    # Calculate cumulative percent change for both FL and NKE
    jointdf['FL_Cumulative_Change'] = jointdf['FL_Daily_Change'].cumsum()
    jointdf['NKE_Cumulative_Change'] = jointdf['NKE_Daily_Change'].cumsum()

    # Plot cumulative percent changes
    plt.figure(figsize=(12, 6))
    plt.plot(jointdf.index, jointdf['FL_Cumulative_Change'], label='FL Cumulative Percent Change', color='blue')
    plt.plot(jointdf.index, jointdf['NKE_Cumulative_Change'], label='NKE Cumulative Percent Change', color='orange')
    
    plt.legend()
    plt.title("Cumulative Percent Change of FL and NKE", fontsize=20)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Cumulative Percent Change", fontsize=12)
    plt.grid(True)
    #plt.show()
    
    return(jointdf)

def long_short(jointdf):
    #Want to find the divergence of some tolerance in cum sum
    diverge_array, rolling_array, value, sNKE, sFL = [], [], 0, False, False

    for index, row in jointdf.iterrows():
        #Finding all the places where NKE and FL cum change differ by at least 25 percent. 
        if abs(row['NKE_Cumulative_Change'] - row['FL_Cumulative_Change']) >= 25:
            if row['NKE_Cumulative_Change'] - row['FL_Cumulative_Change'] >= 0:
                diverge_array.append((index, row['NKE_Cumulative_Change'], row['FL_Cumulative_Change'], True))
                if not rolling_array:
                    fl_price = row['FLOPEN']
                    nke_price = row['NKEOPEN']
                    sNKE = True
                    rolling_array.append([-1000/nke_price, 1000/fl_price, index, True])
                    print("Short loaded at ", index)
            else: 
                diverge_array.append((index, row['NKE_Cumulative_Change'], row['FL_Cumulative_Change'], False))
                if not rolling_array:
                    fl_price = row['FLOPEN']
                    nke_price = row['NKEOPEN']
                    sFL = True
                    rolling_array.append([1000/nke_price, -1000/fl_price, index, False])
                    print("Short loaded at ", index)
        #Checks if we are short NKE
        if rolling_array and sNKE==True: 
            if row['NKE_Cumulative_Change']-row['FL_Cumulative_Change'] <= 0:
                #Unwind position
                fl_price = row['FLOPEN']
                nke_price = row['NKEOPEN']
                print(rolling_array)
                nkeshare, flshare, date, temp = rolling_array.pop()
                value += round(fl_price*flshare + nke_price*nkeshare, 2)
                sNKE = False
                print("Unwound on ", date, "value added ", round(fl_price*flshare + nke_price*nkeshare, 2), " Balance ", round(value, 2))

                pass
        #Checks if we are short FL
        elif rolling_array and sFL==True: 
            if row['FL_Cumulative_Change']-row['NKE_Cumulative_Change'] <= 0:
                #Unwind position
                fl_price = row['FLOPEN']
                nke_price = row['NKEOPEN']
                print(rolling_array)
                nkeshare, flshare, date, temp = rolling_array.pop()
                value += round(fl_price*flshare + nke_price*nkeshare, 2)
                sFL = False
                print("Unwound on ", date, "value added ", round(fl_price*flshare + nke_price*nkeshare, 2), " Balance ", round(value, 2))
                pass

    plt.figure(figsize=(12, 6))
    plt.plot(jointdf.index, jointdf['FL_Cumulative_Change'], label='FL Cumulative Percent Change', color='blue')
    plt.plot(jointdf.index, jointdf['NKE_Cumulative_Change'], label='NKE Cumulative Percent Change', color='orange')

    for diverge_point in diverge_array:
        date = diverge_point[0]
        plt.axvline(x=date, color='grey', linestyle='--', alpha=0.3)


    plt.legend()
    plt.title("Cumulative Percent Change of FL and NKE with Divergence Points", fontsize=20)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Cumulative Percent Change", fontsize=12)
    plt.grid(True)
    plt.show() 

#Driver Code
start = date(2019, 8, 3)
end = date(2024, 8, 11)
jointdf = getData(start, end)
long_short(jointdf)