# ================================================== #
#   Importation Of Default Module
# ================================================== #
from datetime import datetime

# ================================================== #
#   Importation Of 3rd Party Module
# ================================================== #
import pandas as pd
import requests

# ================================================== #
#   Importation Of Self Development Module
# ================================================== #

# ================================================== #
#   Declaration AND Definition Of This Module Variable
# ================================================== #
URL_Listed = r"https://isin.twse.com.tw/isin/C_public.jsp?strMode=2";
URL_OTC = r"https://isin.twse.com.tw/isin/C_public.jsp?strMode=4";
URL_Emerging = r"https://isin.twse.com.tw/isin/C_public.jsp?strMode=5";

URLLocal_Listed = r"./../Listed_Normal_Symbol_{}.csv"
URLLocal_OTC = r"./../OTC_Normal_Symbol_{}.csv"
URLLocal_Emerging = r"./../Emerging_Normal_Symbol_{}.csv"
# ================================================== #
#   Declaration AND Definition Of This Module Function
# ================================================== #
def GetNormalSymbol (Market: int=0) -> pd.DataFrame:
    if ((type(Market) != int) or (Market < 0) or (Market >= 3)):
        print("\n0: Stock Exchange Market\n\
               \r1: OTC Market\n\
               \r2: Emerging Stock Market\n")
        return None
    
    today = datetime.today()
    ThisYear = today.year
    ThisMonth = today.month

    if (Market == 0):
        try:
            ListedNormalSymbol = pd.read_csv(URLLocal_Listed.format(str(ThisYear) + "Q" + str((ThisMonth-1)//3 + 1)))
        except:
            print("GET New Listed Normal Symbol From The Internet")
        else:
            return ListedNormalSymbol

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
    
    # -------------------------------------------------- #
    #   Post Processing
    # -------------------------------------------------- #
    if (Market == 0):
        DFSymbol = DFSymbol[0]
        DFSymbol.columns = DFSymbol.iloc[0, :]
        ListedNormalSymbol = DFSymbol[DFSymbol["CFICode"] == "ESVUFR"]
        ListedNormalSymbol["Symbol"] = ListedNormalSymbol["有價證券代號及名稱"].apply(lambda x: (x.split())[0])
        ListedNormalSymbol["Name"] = ListedNormalSymbol["有價證券代號及名稱"].apply(lambda x: (x.split())[1])
        ListedNormalSymbol = ListedNormalSymbol[["Symbol", "Name", "上市日", "產業別"]]
        ListedNormalSymbol.reset_index(drop=True, inplace=True)
    elif (Market == 1):
        pass
    elif (Market == 2):
        pass

    return ListedNormalSymbol

# ================================================== #
#   Testing Of This Module
# ================================================== #
if (__name__ == "__main__"):
    result = GetNormalSymbol(Market=3)
    result = GetNormalSymbol(Market=0)
    print(result.head(5))