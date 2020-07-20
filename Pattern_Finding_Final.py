#!/usr/bin/env python
# coding: utf-8

# In[9]:


# library
import pandas as pd
import numpy as np
import os
import glob


# # Pattern Definition

# # Three Line Strike Pattern

# ![three_line_strike.png](attachment:three_line_strike.png)

# In[10]:


## Pattern Illustration

## Bullish Three Line Strike
# First, an uptrend must be in progress. 
# Second, a white (or green) candle must appear on the first day. 
# Third, another white candle must appear on the second day, closing higher than the previous day. 
# Fourth, a third white candle must appear on the third day, again closing higher than the previous day's close. 
# These candles continue the established uptrend. 
# Fifth, those three escalating white candles should be followed by a black (or red) candle, which opens higher than the previous candles but then dips down, closing below the first candle's opening price. 
# In the end, this fourth candle should contain the real bodies of the three previous candles within its length.

## Bearish Three Line Strike
# A bearish three line strike is the reverse with three strong falling candles that close increasingly lower followed by a single bullish strike candle. 
# The strike candle should open at or lower than the close of the third candle and close above the open of the first candle. 
# In the bearish three line strike, the high of the strike candle should retrace up to at least the open of the first candle. 
# Some tolerance is normally given around the levels.


# In[11]:


# matching function for Bullish Three Line Strike pattern
Bullish_Three_Line_Strike_Appearance = 0
BullTLS_Uptrend = 0
BullTLS_Eventrend = 0
BullTLS_Downtrend = 0
def is_Three_Line_Strike_Bullish(df):
    stick_needed = 4 # This pattern needs 4 candlestick 
    # index 0-3 is for pattern, index 4-7 is for following trend
    # df.iloc[i] represents for the (i-1)th candlestick in the pattern
    if(
        
        (df.iloc[0]["open"] < df.iloc[0]["close"]) &
        (df.iloc[1]["open"] < df.iloc[1]["close"]) &
        (df.iloc[2]["open"] < df.iloc[2]["close"]) & # the first three candlesticks are white, which is open < close
        (df.iloc[3]["open"] > df.iloc[3]["close"]) & # the fourth(strike) candlestick is black, which is open > close
        # a uptrend should be checked for the first three candlesticks
        (df.iloc[0]["open"] < df.iloc[1]["open"]) & 
        (df.iloc[1]["open"] < df.iloc[2]["open"]) &
        (df.iloc[0]["close"] < df.iloc[1]["close"]) &
        (df.iloc[1]["close"] < df.iloc[2]["close"]) &
        # the fourth candle should contain the real bodies of the three previous candles within its length
        (df.iloc[3]["close"] <= df.iloc[0]["open"]) &
        (df.iloc[3]["open"] >= df.iloc[2]["close"])
        ):
         global Bullish_Three_Line_Strike_Appearance
         global BullTLS_Uptrend
         global BullTLS_Eventrend
         global BullTLS_Downtrend 
         # Calculate the following stock trend
         following_max = (df["high"].iloc[4:4+stick_needed].max() - df.iloc[3]["high"]) / df.iloc[3]["high"]
         if (following_max > 0.01):
             BullTLS_Uptrend+=1
         elif (following_max > -0.01):
             BullTLS_Eventrend+=1
         else:
             BullTLS_Downtrend+=1
         Bullish_Three_Line_Strike_Appearance+=1            
         print("Bullish Three Line Strike Spotted! Number of Apperance: " + str(Bullish_Three_Line_Strike_Appearance))


# In[12]:


# matching function for Bullish Three Line Strike pattern
Bearish_Three_Line_Strike_Appearance = 0
BearTLS_Uptrend = 0
BearTLS_Eventrend = 0
BearTLS_Downtrend = 0
def is_Three_Line_Strike_Bearish(df):
    stick_needed = 4 # This pattern needs 4 candlestick 
    # index 0-3 is for pattern, index 4-7 is for following trend
    # df.iloc[i] represents for the (i-1)th candlestick in the pattern (i is in [0,3])
    if((df.iloc[0]["open"] > df.iloc[0]["close"]) &
        (df.iloc[1]["open"] > df.iloc[1]["close"]) &
        (df.iloc[2]["open"] > df.iloc[2]["close"]) & # the first three candlesticks are white, which is open < close
        (df.iloc[3]["open"] < df.iloc[3]["close"]) & # the fourth(strike) candlestick is black, which is open > close
        # a downtrend should be checked for the first three candlesticks
        (df.iloc[0]["open"] > df.iloc[1]["open"]) & 
        (df.iloc[1]["open"] > df.iloc[2]["open"]) &
        (df.iloc[0]["close"] > df.iloc[1]["close"]) &
        (df.iloc[1]["close"] > df.iloc[2]["close"]) &
        # the fourth candle should contain the real bodies of the three previous candles within its length
        (df.iloc[3]["close"] >= df.iloc[0]["open"]) &
        (df.iloc[3]["open"] <= df.iloc[2]["close"])
        ):
         global Bearish_Three_Line_Strike_Appearance
         global BearTLS_Uptrend
         global BearTLS_Eventrend
         global BearTLS_Downtrend 
         # Calculate the following stock trend
         following_max = (df["high"].iloc[4:4+stick_needed].max() - df.iloc[3]["high"]) / df.iloc[3]["high"]
         if (following_max > 0.01):
             BearTLS_Uptrend +=1
         elif (following_max > -0.01):
             BearTLS_Eventrend+=1
         else:
             BearTLS_Downtrend+=1
         Bearish_Three_Line_Strike_Appearance+=1            
         print("Bearish Three Line Strike Spotted! Number of Apperance: " + str(Bearish_Three_Line_Strike_Appearance))


# # Two Black Gapping

# ![Two-Black-Gapping.png](attachment:Two-Black-Gapping.png)

# In[13]:


## Two Black Gapping Pattern Illustration

# This pattern is constructed by two black candles
# First candle:
# 1) a candle in a downtrend
# 2) black body
# 3) opening price gaps lower from the previous candle

# Second candle:
# 1) black body
# 2) the opening below the prior candle's opening but higher than its low
# 3) the closing below the prior candle's closing

## Addition 
# – Normally it should be a signal of continuation of the current Trend.
# – It occurs during a Downtrend; confirmation is required by the candles that follow the Pattern.
# – There is a Gap Down between the First Candle and the Previous one.
# – The First Candle is black.
# – The Second Candle is black, it has the High below the High of the Previous Candle.


# In[14]:


# matching function for Bearish Two Black Gapping pattern 
Two_Black_Gapping_Appearance = 0
TBG_Uptrend = 0
TBG_Eventrend = 0
TBG_Downtrend = 0
def is_Two_Black_Gapping(df):
    stick_needed = 2 * 2 # This pattern needs 2 candlestick charts, and another two is for checking whether the first candlestick in the pattern is in a downtrend or not
    # index 0-1 is for previous trend check, index 2-3 is for the pattern 
    if( 
        ## First candlestick:
        #  black body
        (df.iloc[2]["open"] > df.iloc[2]["close"]) &
        # check if there is a preceding downtrend  \\\\0.98?
        (df.iloc[0]["close"] > df.iloc[1]["close"]) &
        (df.iloc[0]["open"] > df.iloc[1]["open"])&
        # check if there is a gap between the first pattern candlestick and prior one 
        (df.iloc[2]["high"] < df.iloc[1]["low"]) &
        ## Second candlestick:
        #  black body
        (df.iloc[3]["open"] > df.iloc[3]["close"]) &
        #  relation with prior candlestick: the opening below the prior candle's opening but higher than its low
        (df.iloc[3]["open"] < df.iloc[2]["open"]) &
        (df.iloc[3]["open"] > df.iloc[2]["low"]) &
        #  the closing below the prior candle's closing
        (df.iloc[3]["close"] < df.iloc[2]["close"]) &
        #  its high below the high of previous one
        (df.iloc[3]["high"] < df.iloc[2]["high"])):
         global Two_Black_Gapping_Appearance
         global TBG_Uptrend
         global TBG_Eventrend
         global TBG_Downtrend
         # Calculate the following stock trend
         following_min = (df["low"].iloc[4:4+stick_needed].min() - df.iloc[3]["low"]) / df.iloc[3]["low"]
         if (following_min > 0.005):
             TBG_Uptrend+=1
         elif (following_min > -0.005):
             TBG_Eventrend+=1
         else:
             TBG_Downtrend+=1
         Two_Black_Gapping_Appearance+=1
         print("Bearish Two Black Gapping Spotted! Number of Apperance: " + str(Two_Black_Gapping_Appearance))


# # Three Black Crows

# ![Three_black_crows.png](attachment:Three_black_crows.png)

# In[15]:


## Three Black Crows Illustration
#  First, there should be a prevailing uptrend in progress. 
#  Second, there must be three long and bearish (i.e., black or red) candlesticks in a row. 
#  Third, each of those candles must open below the previous day's open. Ideally, it will open in the middle price range of the previous day. 
#  Fourth, each candle must close progressively downward, establishing a new short-term low. 
#  Fifth and finally, it is important that the candles have very small (or nonexistent) lower wicks.

## Uptrend Definition in stocks
# An uptrend describes the price movement of a financial asset when the overall direction is upward. 
# In an uptrend, each successive peak and trough is higher than the ones found earlier in the trend. 
# The uptrend is therefore composed of higher swing lows and higher swing highs. 


# In[16]:


# matching function for Bearish Three Black Crows pattern 
Three_Black_Crows_Appearance = 0
TBC_Uptrend = 0
TBC_Eventrend = 0
TBC_Downtrend = 0
def is_Three_Black_Crows(df):
    stick_needed = 3 * 2 # This pattern needs 3 candlestick to check the pattern, and 3 for prior trend check 
    # index 0-2 is for prior trend, index 3-5 is for the pattern
    if( 
        # check the three candlesticks in the pattern are black and long
        ((df.iloc[3]["close"] / df.iloc[3]["open"]) < 0.985) & # original rate 0.965
        ((df.iloc[4]["close"] / df.iloc[4]["open"]) < 0.985) & 
        ((df.iloc[5]["close"] / df.iloc[5]["open"]) < 0.985) & 
        # candlesticks open within the real body of the previous candle and closed lower than the previous candle.
        (df.iloc[4]["open"] < df.iloc[3]["open"]) &
        (df.iloc[4]["open"] > df.iloc[3]["close"]) &
        (df.iloc[4]["close"] < df.iloc[3]["close"]) &
        (df.iloc[5]["open"] < df.iloc[4]["open"]) &
        (df.iloc[5]["open"] > df.iloc[4]["close"]) &
        (df.iloc[5]["close"] < df.iloc[4]["close"]) &
        # check if there is a preceding uptrend
        # (df.iloc[2]["close"] > 1.02 * df["close"].iloc[0:2].mean()))
        (df.iloc[0]["high"] < df.iloc[1]["high"])&
        (df.iloc[0]["low"] < df.iloc[1]["low"])&
        (df.iloc[1]["high"] < df.iloc[2]["high"])&
        (df.iloc[1]["high"] < df.iloc[2]["high"])
         ):
         global Three_Black_Crows_Appearance
         global TBC_Uptrend
         global TBC_Eventrend
         global TBC_Downtrend
         # Calculate the following stock trend
         following_min =(df["low"].iloc[6:6+stick_needed].min() - df.iloc[5]["low"]) / df.iloc[5]["low"]
         if (following_min > 0.005):
             TBC_Uptrend+=1
         elif (following_min > -0.005):
             TBC_Eventrend+=1
         else:
             TBC_Downtrend+=1
         Three_Black_Crows_Appearance+=1
         print("Bearish Three Black Crows Spotted! Number of Apperance: " + str(Three_Black_Crows_Appearance))


# # Evening Star

# ![Evening%20Star.png](attachment:Evening%20Star.png)

# In[17]:


## Evening Star Illustration
# The bearish evening star reversal pattern starts with a tall white bar that carries an uptrend to a new high. 
# The market gaps higher on the next bar, but fresh buyers fail to appear, yielding a narrow range candlestick. 
# A gap down on the third bar completes the pattern, which predicts that the decline will continue to even lower lows, perhaps triggering a broader-scale downtrend.
# Large Bullish Candle (Day 1) 
# Small Bullish or Bearish Candle (Day 2) 
# Large Bearish Candle (Day 3)


# In[18]:


# matching function for Bearish Evening Star pattern
Evening_Star_Appearance = 0
ES_Uptrend = 0
ES_Eventrend = 0
ES_Downtrend = 0
def is_Evening_Star(df):
    stick_needed = 3 * 2 # This pattern needs 3 candlestick charts for pattern check, 2 for prior trend check
    # index 0-2 is for prior trend, index 3-5 is for the pattern 
    if(
        # check if there is a downtrend previously
        (df.iloc[0]["high"] > df.iloc[1]["high"])&
        (df.iloc[0]["low"] > df.iloc[1]["low"])&
        (df.iloc[1]["high"] > df.iloc[2]["high"])&
        (df.iloc[1]["low"] > df.iloc[2]["low"])&
        (df.iloc[0:2]["high"].max() < df.iloc[3]["high"])&  
        # First candlestick: white long body check
        ((df.iloc[3]["close"] / df.iloc[3]["open"]) > 1.03) & 
        # Second candlestick: small bullish or small bearish body
        ((df.iloc[4]["close"] / df.iloc[4]["open"]) > 0.985) &
        ((df.iloc[4]["close"] / df.iloc[4]["open"]) < 1.015) &
        # Third candlestick: large bearish candlestick
        ((df.iloc[5]["close"] / df.iloc[5]["open"]) < 0.97) &
        # Relations between candlesticks
        # gap up 
        (df.iloc[4]["close"] > df.iloc[3]["close"]) &
        (df.iloc[4]["open"] > df.iloc[3]["close"]) &
        # gap down
        (df.iloc[4]["close"] > df.iloc[5]["open"]) &
        (df.iloc[4]["open"] > df.iloc[5]["open"]) 
        ):
         global Evening_Star_Appearance
         global ES_Uptrend
         global ES_Eventrend
         global ES_Downtrend
         # Calculate the following stock trend
         following_min =(df["low"].iloc[6:6+stick_needed].min() - df.iloc[5]["low"]) / df.iloc[5]["low"]
         if (following_min > 0.005):
             ES_Uptrend+=1
         elif (following_min > -0.005):
             ES_Eventrend+=1
         else:
             ES_Downtrend+=1
         Evening_Star_Appearance+=1
         print("Bearish Evening Star Spotted! Number of Apperance: " + str(Evening_Star_Appearance))


# # Abandoned Baby

# ![abandoned%20baby.png](attachment:abandoned%20baby.png)

# In[19]:


## Abandoned Baby Illustration
# The bullish abandoned baby reversal pattern appears at the low of a downtrend, after a series of black candles print lower lows. 
# The market gaps lower on the next bar, but fresh sellers fail to appear, yielding a narrow range doji candlestick with opening and closing prints at the same price.
# A bullish gap on the third bar completes the pattern, which predicts that the recovery will continue to even higher highs, perhaps triggering a broader-scale uptrend.

## doji candle 
# A doji is a name for a session in which the candlestick for a security has an open and close that are virtually equal and are often components in patterns.


# In[20]:


# matching function for Bullish Abandoned Baby pattern 
Abandoned_Baby_Appearance = 0
AB_Uptrend = 0
AB_Eventrend = 0
AB_Downtrend = 0
def is_Abandoned_Baby(df):
    stick_needed = 3 * 2 # This pattern needs 3 candlestick, another 3 for prior pattern check 
    # index 0-2 is for prceding trend, index 3-5 is for the pattern     
    if(
        # check if there is a downtrend previously
        (df.iloc[0]["high"] > df.iloc[1]["high"])&
        (df.iloc[0]["low"] > df.iloc[1]["low"])&
        (df.iloc[1]["high"] > df.iloc[2]["high"])&
        (df.iloc[1]["low"] > df.iloc[2]["low"])&
#         (df.iloc[2]["high"] > df.iloc[3]["high"])&
#         (df.iloc[3]["low"] > df.iloc[3]["low"])&   whether the first candle is included the trend or not
        # make sure the pattern's 1st candle appears at the low of a downtrend
        (df.iloc[3]["close"] < df.iloc[2]["close"])&
        (df.iloc[3]["open"] < df.iloc[2]["open"]) & 
        # check if the second candlestick is doji
        ((df.iloc[4]["close"] / df.iloc[4]["open"]) > 0.995) & 
        ((df.iloc[4]["close"] / df.iloc[4]["open"]) < 1.005) & 
        # gaps lower between 2nd and 3rd candle
        (df.iloc[4]["high"] < df.iloc[3]["low"]) &
        # 3rd candle is white
        (df.iloc[5]["close"] > df.iloc[5]["open"]) &
        # bullish gap finish the pattern
        (df.iloc[5]["low"] > df.iloc[4]["high"])):
         global Abandoned_Baby_Appearance
         global AB_Uptrend
         global AB_Eventrend
         global AB_Downtrend
         # Calculate the following stock trend
         following_min =(df["high"].iloc[6:6+stick_needed].max() - df.iloc[5]["high"]) / df.iloc[5]["high"]
         if (following_min > 0.01):
             AB_Uptrend+=1
         elif (following_min > -0.01):
             AB_Eventrend+=1
         else:
             AB_Downtrend+=1
         Abandoned_Baby_Appearance+=1
         print("Bullish Abandoned_Baby Spotted! Number of Apperance: " + str(Abandoned_Baby_Appearance))


# # Data 

# In[21]:


processed = 0
total_CS_Chart = 0
def process_csv(csv_filename):
    data = pd.read_csv(csv_filename) # Get data
    reverse_data = data.iloc[::-1]  # sort data from oldest to newest
    row_size = len(reverse_data) # Number of rows in dataframe
    # Iterate over the CSV file and look for the 5 patterns
    global total_CS_Chart
    for row_number in range(row_size - 12):
        total_CS_Chart+=1
        is_Three_Line_Strike_Bullish(reverse_data[row_number:row_number+8])
        is_Three_Line_Strike_Bearish(reverse_data[row_number:row_number+8])
        is_Two_Black_Gapping(reverse_data[row_number:row_number+8])
        is_Three_Black_Crows(reverse_data[row_number:row_number+12])
        is_Evening_Star(reverse_data[row_number:row_number+12])
        is_Abandoned_Baby(reverse_data[row_number:row_number+12])        
    # print a message to the terminal when a file has been processed
    global processed
    processed+=1
    print("file " + str(processed) + " processed.")


# In[22]:


# Iterate over all the CSV files
# Use your own file path
INPUT_PATH = r"C:\Users\ASUS\Downloads\Data\Data"

for csv_filename in glob.glob(os.path.join(INPUT_PATH, "*.csv")):
    process_csv(csv_filename)    

print("Total Candlestick Chart Scanned: " + str(total_CS_Chart))
    
print("Bullish Three Line Strike Appearance: " + str(Bullish_Three_Line_Strike_Appearance))
print("Uptrend: " + str(BullTLS_Uptrend))
print("Eventrend: " + str(BullTLS_Eventrend))
print("Downtrend: " + str(BullTLS_Downtrend))
print("Accuracy: " + str(BullTLS_Downtrend /Bullish_Three_Line_Strike_Appearance))

print("Bearish Three Line Strike Appearance: " + str(Bearish_Three_Line_Strike_Appearance))
print("Uptrend: " + str(BearTLS_Uptrend))
print("Eventrend: " + str(BearTLS_Eventrend))
print("Downtrend: " + str(BearTLS_Downtrend))
print("Accuracy: " + str(BearTLS_Uptrend / Bearish_Three_Line_Strike_Appearance))

print("Bearish Two Black Gapping Appearance: " + str(Two_Black_Gapping_Appearance))
print("Uptrend: " + str(TBG_Uptrend))
print("Eventrend: " + str(TBG_Eventrend))
print("Downtrend: " + str(TBG_Downtrend))
print("Accuracy: " + str(TBG_Downtrend / Two_Black_Gapping_Appearance))

print("Bearish Three Black Crows Appearance: " + str(Three_Black_Crows_Appearance))
print("Uptrend: " + str(TBC_Uptrend))
print("Eventrend: " + str(TBC_Eventrend))
print("Downtrend: " + str(TBC_Downtrend))
print("Accuracy: " + str(TBC_Downtrend / Three_Black_Crows_Appearance))

print("Bearish Evening Star Appearance: " + str(Evening_Star_Appearance))
print("Uptrend: " + str(ES_Uptrend))
print("Eventrend: " + str(ES_Eventrend))
print("Downtrend: " + str(ES_Downtrend))
print("Accuracy: " + str(ES_Downtrend / Evening_Star_Appearance))

print("Bullish Abandoned Baby Appearance: " + str(Abandoned_Baby_Appearance))
print("Uptrend: " + str(AB_Uptrend))
print("Eventrend: " + str(AB_Eventrend))
print("Downtrend: " + str(AB_Downtrend))
print("Accuracy: " + str(AB_Uptrend / Abandoned_Baby_Appearance))


# In[23]:


from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)


# In[ ]:




