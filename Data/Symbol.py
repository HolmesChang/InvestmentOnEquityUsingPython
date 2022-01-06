import pandas as pd
import requests

URL_Listed = r"https://isin.twse.com.tw/isin/C_public.jsp?strMode=2";
URL_OTC = r"https://isin.twse.com.tw/isin/C_public.jsp?strMode=4";
URL_Emerging = r"https://isin.twse.com.tw/isin/C_public.jsp?strMode=5";

def GetNormalSymbol (Market: int=0) -> pd.DataFrame:
    if ((type(Market) != int) or (Market < 0) or (Market >= 3)):
        print("0: Stock Exchange Market\n\
               1: OTC Market\n\
               2: Emerging Stock Market")
        return None
    
    if (Market == 0):
        try:
            response = requests.get(URL_Listed)
        except Exception as Ex:
            print(Ex)
    elif (Market == 1):
        try:
            response = requests.get(URL_OTC)
        except Exception as Ex:
            print(Ex)
    elif (Market == 2):
        try:
            response = requests.get(URL_Emerging)
        except Exception as Ex:
            print(Ex)
    
    if (response.status_code == 200):
        DFSymbol = pd.read_html(response.text)
    elif (response.status_code == 404):
        print("404")
        return None
    
    # Post Processing
    DFSymbol = DFSymbol[0]
    DFSymbol.columns = DFSymbol.iloc[0, :]
    ListedNormalSymbol = DFSymbol[DFSymbol["CFICode"] == "ESVUFR"]
    ListedNormalSymbol["Symbol"] = ListedNormalSymbol["有價證券代號及名稱"].apply(lambda x: (x.split())[0])
    ListedNormalSymbol["Name"] = ListedNormalSymbol["有價證券代號及名稱"].apply(lambda x: (x.split())[1])
    ListedNormalSymbol = ListedNormalSymbol[["Symbol", "Name", "上市日", "產業別"]]
    ListedNormalSymbol.reset_index(drop=True, inplace=True)

    return ListedNormalSymbol
