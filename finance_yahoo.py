import requests
import csv
import time
import datetime

COMPANIES = ["PD", "ZUO", "PINS", "ZM", "PVTL", "DOCU", "CLDR", "RUN"]
YOUR_PATH = "  Specify the path to your folder here  "
URL = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-historical-data"
URL_NEWS = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-newsfeed"
HEADERS = {
    "x-rapidapi-host": "apidojo-yahoo-finance-v1.p.rapidapi.com",
    "x-rapidapi-key": "dea3efeedbmshd5e6f358d022195p12c033jsnc4b1bafc9602",
}
date_today = datetime.date.today()
unixtime = int(time.mktime(date_today.timetuple()))


def three_day_before(data):
    days_close = {}
    for i in data["prices"]:
        day = datetime.datetime.fromtimestamp(i["date"]).strftime("%b %d, %Y")
        days_close[day] = round(i["close"], 2)
    return days_close


def three_day_before_change(days_close_value, day):
    d_close = datetime.datetime.fromtimestamp(day).strftime("%b %d, %Y")
    d_three_close = datetime.datetime.fromtimestamp(day - 86400 * 3).strftime(
        "%b %d, %Y"
    )
    if d_three_close in days_close_value:
        changes = float(days_close_value[d_close]) / float(
            days_close_value[d_three_close]
        )
        return changes
    else:
        return "-"


def writer_historical_data(company):
    querystring = {
        "frequency": "1d",
        "filter": "history",
        "period1": "0",
        "period2": unixtime,
        "symbol": company,
    }
    try:
        response = requests.request("GET", URL, headers=HEADERS, params=querystring)
        data = response.json()
        path = "%s%s.csv" % (YOUR_PATH, company)
        days_close_value = three_day_before(data)
        with open(path, mode="w") as csv_file:
            fieldnames = [
                "Date",
                "Open",
                "High",
                "Low Close*",
                "Adj Close**",
                "Volume",
                "3day_before_change",
            ]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for i in data["prices"]:
                writer.writerow(
                    {
                        "Date": datetime.datetime.fromtimestamp(i["date"]).strftime(
                            "%b %d, %Y"
                        ),
                        "Open": round(i["open"], 2),
                        "High": round(i["high"], 2),
                        "Low Close*": round(i["low"], 2),
                        "Adj Close**": round(i["close"], 2),
                        "Volume": round(i["volume"], 3),
                        "3day_before_change": three_day_before_change(
                            days_close_value, i["date"]
                        ),
                    }
                )
        time.sleep(12)
    except:
        pass


def writer_company_news(company):
    querystring = {"region": "US", "category": company}
    try:
        response_news_company = requests.request(
            "GET", URL_NEWS, headers=HEADERS, params=querystring
        )
        data_news_company = response_news_company.json()
        path = "%s%s_news.csv" % (YOUR_PATH, company)
        if data_news_company["items"]["result"]:
            with open(path, mode="w") as csv_file:
                fieldnames = ["Link", "Title"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for i in data_news_company["items"]["result"]:
                    writer.writerow({"Link": i["link"], "Title": i["title"]})
        time.sleep(12)
    except:
        pass


if __name__ == "__main__":
    for company in COMPANIES:
        writer_historical_data(company)
        writer_company_news(company)
