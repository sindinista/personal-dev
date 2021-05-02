# libraries
import pandas as pd
import requests
import json
import prettytable
import numpy as np
import calendar as cal
from datetime import date, timedelt

# get Bureau of Labor Statistics Job Openings and Employment reports for 'Accomodation and Food Services' sector

headers = {"Content-type": "application/json"}
data = json.dumps(
    {
        "seriesid": ["JTU720000000000000TSL", "CEU7072000001"],
        "startyear": "2018",
        "endyear": "2021",
    }
)
p = requests.post(
    "https://api.bls.gov/publicAPI/v2/timeseries/data/", data=data, headers=headers
)
json_data = json.loads(p.text)
for series in json_data["Results"]["series"]:
    x = prettytable.PrettyTable(["series id", "year", "period", "value", "footnotes"])
    seriesId = series["seriesID"]
    for item in series["data"]:
        year = item["year"]
        period = item["period"].strip(" ")
        value = item["value"]
        footnotes = ""
        for footnote in item["footnotes"]:
            if footnote:
                footnotes = footnotes + footnote["text"] + ","
            if "M01" <= period <= "M12":
                x.add_row([seriesId, year, period, value, footnotes[0:-1]])
    output = open(seriesId + ".txt", "w")
    output.write(x.get_string())
    output.close()


def jolts(csv):
    f = lambda x: ((x.rstrip(".0")).lstrip("M"))
    jolts = pd.read_csv(
        csv,
        converters={2: f},
        sep="|",
        header=1,
        usecols=[2, 3, 4, 5],
        names=["year", "period", "totalSep", "footnotes"],
    ).dropna()
    return jolts


def sum12(df):
    for i in range(0, df.shape[0] - 11):
        df.loc[df.index[i], "SUM_12"] = (
            df.iloc[i, 2]
            + df.iloc[i + 1, 2]
            + df.iloc[i + 2, 2]
            + df.iloc[i + 3, 2]
            + df.iloc[i + 4, 2]
            + df.iloc[i + 5, 2]
            + df.iloc[i + 6, 2]
            + df.iloc[i + 7, 2]
            + df.iloc[i + 8, 2]
            + df.iloc[i + 9, 2]
            + df.iloc[i + 10, 2]
            + df.iloc[i + 11, 2]
        )
    return df


def emp(csv):
    f = lambda x: ((x.rstrip(".0")).lstrip("M"))
    emp = pd.read_csv(
        csv,
        converters={2: f},
        sep="|",
        header=1,
        usecols=[2, 3, 4, 5],
        names=["year", "period", "headcount", "footnotes"],
    ).dropna()
    return emp


def avg12(df):
    for i in range(0, df.shape[0] - 11):
        df.loc[df.index[i], "AVG_12"] = np.round(
            (
                (
                    df.iloc[i, 2]
                    + df.iloc[i + 1, 2]
                    + df.iloc[i + 2, 2]
                    + df.iloc[i + 3, 2]
                    + df.iloc[i + 4, 2]
                    + df.iloc[i + 5, 2]
                    + df.iloc[i + 6, 2]
                    + df.iloc[i + 7, 2]
                    + df.iloc[i + 8, 2]
                    + df.iloc[i + 9, 2]
                    + df.iloc[i + 10, 2]
                    + df.iloc[i + 11, 2]
                )
                / 12
            ),
            1,
        )
    return df


# load dataframes from txt
foodTS = jolts("JTU720000000000000TSL.txt")
foodEmp = emp("CEU7072000001.txt")

# sum12 and avg12
foodTS = sum12(foodTS)
foodEmp = avg12(foodEmp)

# merge industry data and calculate turnover
foodTurnover = pd.merge(
    foodEmp,
    foodTS,
    how="left",
    left_on=["year", "period"],
    right_on=["year", "period"],
    suffixes=("_HC", "_Sep"),
)
foodTurnover["Turnover"] = foodTurnover.apply(
    lambda x: x["SUM_12"] / x["AVG_12"], axis=1
)
