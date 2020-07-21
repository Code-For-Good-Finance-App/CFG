# -*- coding: utf-8 -*-
"""
Runs on a daily basis and identifies every candlestick pattern of the stock 
data of the considered companies


"""

import pandas as pd
import yfinance as yf

# Identifying function for Bullish Three Line Srike
def find_Three_Line_Strike_Bullish(df):
    if( 
        (df.iloc[2]["Open"] < df.iloc[2]["Close"]) &
        (df.iloc[3]["Open"] < df.iloc[3]["Close"]) &
        (df.iloc[4]["Open"] < df.iloc[4]["Close"]) & # the first three candlesticks are white, which is Open < Close
        (df.iloc[5]["Open"] > df.iloc[5]["Close"]) & # the fourth(strike) candlestick is black, which is Open > Close
        # a uptrend should be checked for the first three candlesticks
        (df.iloc[2]["Open"] < df.iloc[3]["Open"]) & 
        (df.iloc[3]["Open"] < df.iloc[4]["Open"]) &
        (df.iloc[2]["Close"] < df.iloc[3]["Close"]) &
        (df.iloc[3]["Close"] < df.iloc[4]["Close"]) &
        # the fourth candle should contain the real bodies of the three previous candles within its length
        (df.iloc[5]["Close"] <= df.iloc[2]["Open"]) &
        (df.iloc[5]["Open"] >= df.iloc[4]["Close"])
        ):
        return True    
    else:
        return False
    
# Identifying function for Bearish Three Line Srike
def find_Three_Line_Strike_Bearish(df):
    if( 
        (df.iloc[2]["Open"] > df.iloc[2]["Close"]) &
        (df.iloc[3]["Open"] > df.iloc[3]["Close"]) &
        (df.iloc[4]["Open"] > df.iloc[4]["Close"]) & # the first three candlesticks are white, which is Open < Close
        (df.iloc[5]["Open"] < df.iloc[5]["Close"]) & # the fourth(strike) candlestick is black, which is Open > Close
        # a downtrend should be checked for the first three candlesticks
        (df.iloc[2]["Open"] > df.iloc[3]["Open"]) & 
        (df.iloc[3]["Open"] > df.iloc[4]["Open"]) &
        (df.iloc[2]["Close"] > df.iloc[3]["Close"]) &
        (df.iloc[3]["Close"] > df.iloc[4]["Close"]) &
        # the fourth candle should contain the real bodies of the three previous candles within its length
        (df.iloc[5]["Close"] >= df.iloc[2]["Open"]) &
        (df.iloc[5]["Open"] <= df.iloc[4]["Close"])
        ):
        return True    
    else:
        return False
        
# Identifying function for Two Black Gapping
def find_Two_Black_Gapping(df):
    if( 
        ## First candlestick:
        #  black body
        (df.iloc[4]["Open"] > df.iloc[4]["Close"]) &
        # check if there is a preceding downtrend  \\\\0.98?
        (df.iloc[2]["Close"] > df.iloc[3]["Close"]) &
        (df.iloc[2]["Open"] > df.iloc[3]["Open"])&
        # check if there is a gap between the first pattern candlestick and prior one 
        (df.iloc[4]["High"] < df.iloc[3]["Low"]) &
        ## Second candlestick:
        #  black body
        (df.iloc[5]["Open"] > df.iloc[5]["Close"]) &
        #  relation with prior candlestick: the Opening beLow the prior candle's Opening but Higher than its Low
        (df.iloc[5]["Open"] < df.iloc[4]["Open"]) &
        (df.iloc[5]["Open"] > df.iloc[4]["Low"]) &
        #  the closing beLow the prior candle's closing
        (df.iloc[5]["Close"] < df.iloc[4]["Close"]) &
        #  its High beLow the High of previous one
        (df.iloc[5]["High"] < df.iloc[4]["High"])
        ): 
        return True    
    else:
        return False


# Identifying function for Three Black Crows
def find_Three_Black_Crows(df):
    if( 
        # check the three candlesticks in the pattern are black and long
        ((df.iloc[3]["Close"] / df.iloc[3]["Open"]) < 0.985) & # original rate 0.965
        ((df.iloc[4]["Close"] / df.iloc[4]["Open"]) < 0.985) & 
        ((df.iloc[5]["Close"] / df.iloc[5]["Open"]) < 0.985) & 
        # candlesticks Open within the real body of the previous candle and Closed Lower than the previous candle.
        (df.iloc[4]["Open"] < df.iloc[3]["Open"]) &
        (df.iloc[4]["Open"] > df.iloc[3]["Close"]) &
        (df.iloc[4]["Close"] < df.iloc[3]["Close"]) &
        (df.iloc[5]["Open"] < df.iloc[4]["Open"]) &
        (df.iloc[5]["Open"] > df.iloc[4]["Close"]) &
        (df.iloc[5]["Close"] < df.iloc[4]["Close"]) &
        # check if there is a preceding uptrend
        # (df.iloc[2]["Close"] > 1.02 * df["Close"].iloc[0:2].mean()))
        (df.iloc[0]["High"] < df.iloc[1]["High"])&
        (df.iloc[0]["Low"] < df.iloc[1]["Low"])&
        (df.iloc[1]["High"] < df.iloc[2]["High"])&
        (df.iloc[1]["High"] < df.iloc[2]["High"])
        ):
        return True    
    else:
        return False

# Identifying function for Evening Stars
def find_Evening_Stars(df):
    if( # check if there is a downtrend previously
        (df.iloc[0]["High"] > df.iloc[1]["High"])&
        (df.iloc[0]["Low"] > df.iloc[1]["Low"])&
        (df.iloc[1]["High"] > df.iloc[2]["High"])&
        (df.iloc[1]["Low"] > df.iloc[2]["Low"])&
        (df.iloc[0:2]["High"].max() < df.iloc[3]["High"])&  
        # First candlestick: white long body check
        ((df.iloc[3]["Close"] / df.iloc[3]["Open"]) > 1.03) & 
        # Second candlestick: small bullish or small bearish body
        ((df.iloc[4]["Close"] / df.iloc[4]["Open"]) > 0.985) &
        ((df.iloc[4]["Close"] / df.iloc[4]["Open"]) < 1.015) &
        # Third candlestick: large bearish candlestick
        ((df.iloc[5]["Close"] / df.iloc[5]["Open"]) < 0.97) &
        # Relations between candlesticks
        # gap up 
        (df.iloc[4]["Close"] > df.iloc[3]["Close"]) &
        (df.iloc[4]["Open"] > df.iloc[3]["Close"]) &
        # gap down
        (df.iloc[4]["Close"] > df.iloc[5]["Open"]) &
        (df.iloc[4]["Open"] > df.iloc[5]["Open"])
        ):
        return True    
    else:
        return False
    
# Identifying function for Abandoned Baby
def find_Abandoned_Baby(df):
    if(
        # check if there is a downtrend previously
        (df.iloc[0]["High"] > df.iloc[1]["High"])&
        (df.iloc[0]["Low"] > df.iloc[1]["Low"])&
        (df.iloc[1]["High"] > df.iloc[2]["High"])&
        (df.iloc[1]["Low"] > df.iloc[2]["Low"])&
#         (df.iloc[2]["High"] > df.iloc[3]["High"])&
#         (df.iloc[3]["Low"] > df.iloc[3]["Low"])&   whether the first candle is included the trend or not
        # make sure the pattern's 1st candle appears at the Low of a downtrend
        (df.iloc[3]["Close"] < df.iloc[2]["Close"])&
        (df.iloc[3]["Open"] < df.iloc[2]["Open"]) & 
        # check if the second candlestick is doji
        ((df.iloc[4]["Close"] / df.iloc[4]["Open"]) > 0.995) & 
        ((df.iloc[4]["Close"] / df.iloc[4]["Open"]) < 1.005) & 
        # gaps Lower between 2nd and 3rd candle
        (df.iloc[4]["High"] < df.iloc[3]["Low"]) &
        # 3rd candle is white
        (df.iloc[5]["Close"] > df.iloc[5]["Open"]) &
        # bullish gap finish the pattern
        (df.iloc[5]["Low"] > df.iloc[4]["High"])
        ):
        return True    
    else:
        return False

# Read the Nasdaq company list
# Use your own file path
df = pd.read_csv(r"C:\Users\ASUS\.spyder-py3\Code For Good\Nasdaq_Company_List.csv")

# Iterate over the company list, and identify patterns one by one  
row_size = len(df)
appearance = 0
for row_number in range(row_size):
    # get historical data of past 6 trading days
    company_name = df['Symbol'][row_number]
    ticker = yf.Ticker(company_name)
    hist = ticker.history(period="6d")
    hist.reset_index(drop = True, inplace = True)
    
    # if the passed dataframe has missing rows, pass it and go to the next ticker
    if(hist.size != 42): # 6 rows * 7 columns = 42
        continue
    # find patterns
    if(find_Three_Line_Strike_Bullish(hist)):
        print("Bullish Three Line Strike is spotted in " + company_name + ". Recommendation: Short")
        appearance+=1
    elif(find_Three_Line_Strike_Bearish(hist)):
        print("Bearish Three Line Strike is spotted in " + company_name + ". Recommendation: Long")
    elif(find_Two_Black_Gapping(hist)):
        print("Two Black Gapping is spotted in " + company_name + ". Recommendation: Short")
        appearance+=1
    elif(find_Three_Black_Crows(hist)):
        print("Three Black Crows is spotted in " + company_name + ". Recommendation: Short")
        appearance+=1        
    elif(find_Evening_Stars(hist)):
        print("Evening Stars is spotted in " + company_name + ". Recommendation: Short")
        appearance+=1
    elif(find_Abandoned_Baby(hist)):
        print("Abandoned Baby is spotted in " + company_name + ". Recommendation: Long")
        appearance+=1
        
print(str(appearance) + " patterns are spotted today.")