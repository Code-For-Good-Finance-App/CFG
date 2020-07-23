import webbrowser
from datetime import time
import threading
import time

def openURL(start_line):
    # open file
    nasdaqSym = open("NasdaqList.rtf")

    # skip the first line
    next(nasdaqSym)

    x = 0
    for line in nasdaqSym:
        if(x >= start_line and x < start_line + 5):
            print(x)
            symbol = line.split("|")
            symbol = symbol[0]
            url =  "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + symbol + "&outputsize=full&apikey=263H3BI6S24IY7IO&datatype=csv"
            print(url)
            webbrowser.open(url)
        x = x + 1
    nasdaqSym.close()


starttime=time.time()
start_line = 10
end = False
while (not end):
  openURL(start_line)
  time.sleep(60.0 - ((time.time() - starttime) % 60.0))
  if(start_line >= 450):
      end = True
  else:
      start_line = start_line + 5
  
  

# 
# while(not end):
#     threading.Timer(60.0, openURL(start_line)).start()

    

