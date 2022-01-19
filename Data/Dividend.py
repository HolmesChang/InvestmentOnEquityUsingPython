# ================================================== #
#   Importation Of Default Module
# ================================================== #
from typing import List
from datetime import datetime

# ================================================== #
#   Importation of 3rd Party Module
# ================================================== #
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

# ================================================== #
#   Importation of Self Development Module
# ================================================== #

# ================================================== #
#   Declaration AND Definition Of This Module Variable
# ================================================== #

URLDividend_Network = r"https://mops.twse.com.tw/mops/web/ajax_t05st09_2"
URLDividend_Local = r"Dividend_{}.csv"
headers = {'Connection': 'keep-alive',
           'Content-Length': '172',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
           'sec-ch-ua-platform': 'Windows',
           'Content-Type': 'application/x-www-form-urlencoded',
           'Accept': '*/*',
           "Host": "mops.twse.com.tw",
           'Origin': 'https://mops.twse.com.tw',
           'Sec-Fetch-Site': 'same-origin',
           'Sec-Fetch-Mode': 'cors',
           'Sec-Fetch-Dest': 'empty',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh-TW,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5'}
# co_id: Symbol
# qryType=1: Dividend Determination Year
# qryType=2: Dividend Source Year
payloads = {'encodeURIComponent': 1,
            'step': 1,
            'firstin': 1,
            'off': 1,
            'keyword4': '',
            'code1': '',
            'TYPEK2': '',
            'checkbtn': '',
            'queryName': 'co_id',
            'inpuType': 'co_id',
            'TYPEK': 'all',
            'isnew': 'false',
            'co_id': '',
            'date1': '',
            'date2': '',
            'qryType': 2}

# ================================================== #
#   Declaration AND Definition Of This Module Function
# ================================================== #
def GetDividend (Symbol: str="", Latest: bool=False, StartYear: int=None, EndYear: int=None) -> List[List[float]]:
    today = datetime.today()
    ThisYear = today.year
    ThisMonth = today.month
    if (ThisMonth >= 10):
        LatestYear = ThisYear - 1
    else:
        LatestYear = ThisYear - 2
    
    dividend = None
    try:
        dividend = np.loadtxt(URLDividend_Local.format(Symbol), delimiter=",", encoding="utf_8_sig")
    except Exception as Ex:
        print("No Record. Start Fetching Data From The Internet")
        payloads["co_id"] = Symbol
        payloads["isnew"] = "false"
        payloads["date1"] = str(LatestYear - 1921)
        payloads["date2"] = str(LatestYear - 1911)
        
        try:
            response = requests.post(URLDividend_Network, headers=headers, data=payloads)
        except:
            print("Access Fail. Please Check The Internet Connection")
            return None
        else:
            text = response.text

            df = pd.read_html(text)
            df = df[3]
            df = df[[df.columns[1], df.columns[-11]]]
            df[df.columns[0]] = df[df.columns[0]].apply(lambda x: int(x.replace("年年度", "")) + 1911)
            df.iloc[::-1].to_csv(URLDividend_Local.format(Symbol), header=False, index=False, encoding="utf_8_sig")

            if (Latest):
                return [df.iloc[0].to_list()]
            else:
                dividend = []
                for (index, row) in df.iterrows():
                    if ((row[0] >= StartYear) and (row[0] <= EndYear)):
                        dividend.append(row)
                
                return dividend
    else:
        if (Latest):
            if (dividend[-1, 0] == LatestYear):
                return [dividend[-1]]
            else:
                try:
                    payloads["co_id"] = Symbol
                    if (LatestYear == (dividend[-1, 0] + 1)):
                        payloads["isnew"] = "true"
                    else:
                        payloads["isnew"] = "false"
                        payloads["date1"] = str(dividend[-1, 0] - 1910)
                        payloads["date2"] = str(LatestYear - 1911)
                    
                    response = requests.post(URLDividend_Network, headers=headers, data=payloads)
                except:
                    print("Access Fail. Please Check The Internet Connection")
                    return None
                else:
                    text = response.text

                    df = pd.read_html(text)
                    df = df[3]
                    df = df[[df.columns[1], df.columns[-11]]]
                    df[df.columns[0]] = df[df.columns[0]].apply(lambda x: int(x.replace("年年度", "")) + 1911)

                    tmp = pd.DataFrame(dividend, columns=df.columns)
                    df = tmp.append(df.iloc[::-1], ignore_index=True)
                    df.to_csv(URLDividend_Local.format(Symbol), header=False, index=False, encoding="utf_8_sig")

                    return [df.iloc[-1].to_list()]
        else:
            if (EndYear > LatestYear):
                EndYear = LatestYear
            
            if ((StartYear >= dividend[0, 0]) and (EndYear <= dividend[-1, 0])):
                tmp = []
                for row in dividend:
                    if ((row[0] >= StartYear) and (row[0] <= EndYear)):
                        tmp.append(row)
                
                return tmp
            else:
                try:
                    payloads["co_id"] = Symbol
                    payloads["isnew"] = "false"
                    if (StartYear >= dividend[0, 0]):
                        payloads["date1"] = str(dividend[0, 0] - 1910)
                    else:
                        payloads["date1"] = str(StartYear - 1911)
                    if (EndYear <= dividend[-1, 0]):
                        payloads["date2"] = str(dividend[-1, 0] - 1912)
                    else:
                        payloads["date2"] = str(EndYear - 1911)
                    
                    response = requests.post(URLDividend_Network, headers=headers, data=payloads)
                except:
                    print("Access Fail. Please Check The Internet Connection")
                    return None
                else:
                    text = response.text

                    df = pd.read_html(text)
                    if (StartYear <= (LatestYear-19)):
                        df = df[2]
                    elif (EndYear == LatestYear):
                        df = df[3]
                    else:
                        df = df[2]
                    df = df[[df.columns[1], df.columns[-11]]]
                    df[df.columns[0]] = df[df.columns[0]].apply(lambda x: int(x.replace("年年度", "")) + 1911)

                    if (StartYear >= dividend[0, 0]):
                        tmp = pd.DataFrame(dividend, columns=df.columns)
                        df = tmp.append(df[::-1], ignore_index=True)
                        df.to_csv(URLDividend_Local.format(Symbol), header=False, index=False, encoding="utf_8_sig")
                    elif (EndYear <= dividend[-1, 0]):
                        tmp = pd.DataFrame(dividend, columns=df.columns)
                        df = df[::-1].append(tmp, ignore_index=True)
                        df.to_csv(URLDividend_Local.format(Symbol), header=False, index=False, encoding="utf_8_sig")
                    else:
                        df = df.iloc[::-1]
                        df.to_csv(URLDividend_Local.format(Symbol), header=False, index=False, encoding="utf_8_sig")

                    tmp2 = []
                    for (index, row) in df.iterrows():
                        if ((row[0] >= StartYear) and (row[0] <= EndYear)):
                            tmp2.append(row.to_list())
                    
                    return tmp2
                

# ================================================== #
#   Declaration AND Definition Of This Module Class
# ================================================== #

# ================================================== #
#   Testing Of This Module
# ================================================== #
if (__name__ == "__main__"):
    Dividends = GetDividend(Symbol="8016", Latest=False, StartYear=2001, EndYear=2022)
    for Dividend in Dividends:
        print(Dividend)