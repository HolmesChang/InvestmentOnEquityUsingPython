from typing import List
from datetime import datetime
import requests
import io
import pandas as pd

class TradingDay ():
    def __init__ (self,
                  URLTemplate: str=r"https://www.twse.com.tw/holidaySchedule/holidaySchedule?response=csv&queryYear={}",
                  URLLocal: str=r"Trading_Schedule_{}"):
        self.URLTemplate = URLTemplate
        self.URLLocal = URLLocal
        self.ThisYear = datetime.today().strftime("%Y")

    def GetLocalTradingHolidayFile (self) -> List[str]:
        try:
            df = pd.read_csv(self.URLLocal.format(self.ThisYear))
        except:
            print("No Local Data")
            return None
        
        df = df[df[df.columns[-1]] != "o"]

        dates = df[df.columns[2]].to_list()
        for (index, date) in enumerate(dates):
            dates[index] = "{}{:02}{:02}".format(self.ThisYear, *(list(map(lambda x: int(x), date.replace("月", " ").replace("日", " ").split()))))
        
        return dates
    
    def GetInternetTradingHolidayFile (self) -> List[str]:
        ThisYearTW = str(int(self.ThisYear) - 1911)
        
        try:
            response = requests.get(self.URLTemplate.format(ThisYearTW))
        except:
            print("Error Accessing Server")
            return None
        
        if (response.status_code == 200):
            df = pd.read_csv(io.StringIO(response.content.decode("big5")), skiprows=1, encoding="utf-8")
            df.to_csv(self.URLLocal.format(self.ThisYear), encoding="utf_8_sig")
        else:
            print("Error Response From Server")
            return None
        
        df = df[df[df.columns[-1]] != "o"]

        dates = df[df.columns[1]].to_list()
        for (index, date) in enumerate(dates):
            dates[index] = "{}{:02}{:02}".format(self.ThisYear, *(list(map(lambda x: int(x), date.replace("月", " ").replace("日", " ").split()))))
        
        return dates
    
    def GetTradingHoliday (self):
        dates = self.GetLocalTradingHolidayFile()
        if (type(dates) != type(None)):
            return dates
        
        dates = self.GetInternetTradingHolidayFile()

        return dates
    
    def IsTradingDay (self) -> bool:
        dates = self.GetTradingHoliday()

        today = datetime.today()
        today_date = today.strftime("%Y%m%d")
        today_weekday = today.weekday()

        if (today_weekday >= 5):
            return False
        
        for date in dates:
            if (today_date == date):
                return False
        
        return True

if (__name__ == "__main__"):
    ObjTradingDay = TradingDay()
    TradingHoliday = ObjTradingDay.GetTradingHoliday()
    print(TradingHoliday)

    if (ObjTradingDay.IsTradingDay()):
        print("Today Is Trading Day")
    else:
        print("Today Is Not Trading Day")