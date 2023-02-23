# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 13:03:57 2023

@author: 20181846
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#def country_column(row, country):
#    """Function that returns row only if the location is equal to \
#        one country"""
#    if row["Location"] == country:
#        return row


def one_country(data, country):
    """Function that returns dataset containing data of only one country"""
    return data.loc[data["Location"] == country]


life_expect = pd.read_csv("life_expectancy.csv")

life_expect_birth = life_expect.loc[life_expect["Indicator"] == \
                                    "Life expectancy at birth (years)"]

#life_expect.drop(["IndicatorCode"], axis=1, inplace=True) DELETE

# Only keep the relevant columns for the line plot:
life_expect_line = life_expect_birth[["Location", "Period", \
                                      "FactValueNumeric"]]

# See all countries in dataset:
for Location in life_expect_line:
    print(life_expect_line[Location].unique())

# Make dataframes per country:
expect_chi = one_country(life_expect_line, "China")
expect_chi = expect_chi.groupby(["Period", "Location"], as_index=False)\
    ["FactValueNumeric"].mean()

expect_rus = one_country(life_expect_line, "Russian Federation")
expect_rus = expect_rus.groupby(["Period", "Location"], as_index=False)\
    ["FactValueNumeric"].mean()

expect_can = one_country(life_expect_line, "Canada")
expect_can = expect_can.groupby(["Period", "Location"], as_index=False)\
    ["FactValueNumeric"].mean()
print(expect_can)

expect_us = one_country(life_expect_line, "United States of America")
expect_us = expect_us.groupby(["Period", "Location"], as_index=False)\
    ["FactValueNumeric"].mean()
print(expect_us)

#expect_leso = []
#expect_leso = life_expect_line.apply(country_column, country="Lesotho", axis=1)
# Only keep the rows without NaNs:
#expect_leso = expect_leso[expect_leso["FactValueNumeric"].notna()]
#expect_leso = expect_leso.groupby("Period", as_index=False)\
#    ["FactValueNumeric"].mean()

#life_expect3 = life_expect2.groupby(["Location", "Period"]).mean()
#print(life_expect3)

plt.figure()

#plt.hist(expect_leso["FactValueNumeric"])
plt.plot(expect_chi["Period"], expect_chi["FactValueNumeric"], label="China")
plt.plot(expect_rus["Period"], expect_rus["FactValueNumeric"], label="Russia")
plt.plot(expect_can["Period"], expect_can["FactValueNumeric"], label="Canada")
plt.plot(expect_us["Period"], expect_us["FactValueNumeric"], label="US")

plt.title("Life expectancy of biggest countries in the world")
plt.xlabel("Year")
plt.ylabel("Life expectancy in years")
plt.xlim(2000, 2019)
plt.legend(loc="lower right")

plt.savefig("life_expectancy.png")

plt.show()