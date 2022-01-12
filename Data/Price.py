import pandas as pd
import requests
from bs4 import BeautifulSoup
import yfinance as yf

URL_YTWF_Main = r"https://tw.stock.yahoo.com"
Token_YTWF_Quote = r"quote"
URL_YTWF_Quote = URL_YTWF_Main + r"/" + Token_YTWF_Quote + r"/{}"
symbol = ""
stock = None

def GetRealTimePrice (Symbol: str) -> float:
    try:
        response = requests.get(URL_YTWF_Quote.format(Symbol))
    except Exception as Ex:
        print(Ex)
        return None
    
    if (response.status_code == 200):
        soup = BeautifulSoup(response.text, "html.parser")
    elif (response.status_code == 404):
        print("404")
        return None
    
    price = soup.find("span", {"class":"Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)"}).text

    if (type(price) == float):
        price = float(price)
    
    return price

def GetHistoryPriceANDVolume (Symbol: str, Interval: str="1d", Start: str=None, End: str=None, Period: str="1mo"):
    global symbol
    global stock

    if (Symbol != symbol):
        symbol = Symbol
        stock = yf.Ticker(Symbol)

    data = stock.history(period=Period, interval=Interval, start=Start, end=End)

    price = data.iloc[:, 0:4]
    volume = data.iloc[:, 4]

    return (price, volume)

def GetHistoryNAV ():
    pass

def GetHistoryEPS ():
    pass

def GetHistoryROE ():
    pass

def GetHistoryCDR ():
    pass

def GetHistorySDR ():
    pass

