# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 13:03:57 2023

@author: 20181846
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def one_country(data, country):
    """Function that returns dataset containing data of only one country"""
    one_country = []
    one_country = data.loc[data["Location"] == country]
    one_country = one_country[["Period", "FactValueNumeric"]]
    return one_country


def period_2019(data):
    """dd"""
    period_2019 = []
    period_2019 = data.loc[data["Period"] == 2019]
    period_2019 = period_2019[["Location", "FactValueNumeric"]]
    return period_2019


life_expect = pd.read_csv("life_expectancy.csv")

life_expect_birth = life_expect.loc[life_expect["Indicator"] == \
                                    "Life expectancy at birth (years)"]

# Only keep the relevant columns for the line plot:
life_expect_birth = life_expect_birth[["Location", "Period", \
                                      "FactValueNumeric"]]

# See all countries in dataset:
for Location in life_expect_birth:
    print(life_expect_birth[Location].unique())

# Make dataframes per country and sort by period:
expect_chi = one_country(life_expect_birth, "China")
expect_chi = expect_chi.groupby("Period", as_index=False)\
    ["FactValueNumeric"].mean()

expect_rus = one_country(life_expect_birth, "Russian Federation")
expect_rus = expect_rus.groupby("Period", as_index=False)\
    ["FactValueNumeric"].mean()

expect_can = one_country(life_expect_birth, "Canada")
expect_can = expect_can.groupby("Period", as_index=False)\
    ["FactValueNumeric"].mean()

expect_us = one_country(life_expect_birth, "United States of America")
expect_us = expect_us.groupby("Period", as_index=False)\
    ["FactValueNumeric"].mean()

# Line plot of life expectancy of biggest countries over time
plt.figure()

plt.plot(expect_chi["Period"], expect_chi["FactValueNumeric"], label="China")
plt.plot(expect_rus["Period"], expect_rus["FactValueNumeric"], label="Russia")
plt.plot(expect_can["Period"], expect_can["FactValueNumeric"], label="Canada")
plt.plot(expect_us["Period"], expect_us["FactValueNumeric"], label="US")

plt.title("Life expectancy of biggest countries in the world")
plt.xlabel("Year")
plt.ylabel("Life expectancy in years")
plt.xlim(2000, 2019)
plt.legend(loc="lower right")

plt.savefig("life_expectancy_lineplot.png")

plt.show()

expect_2019 = period_2019(life_expect_birth)
expect_2019 = expect_2019.groupby("Location", as_index=False)\
    ["FactValueNumeric"].mean()

expect_2019_bur = expect_2019.loc[expect_2019["Location"] == "Burundi"]
expect_2019_som = expect_2019.loc[expect_2019["Location"] == "Somalia"]
expect_2019_moz = expect_2019.loc[expect_2019["Location"] == "Mozambique"]
expect_2019_mad = expect_2019.loc[expect_2019["Location"] == "Madagascar"]
expect_2019_sie = expect_2019.loc[expect_2019["Location"] == "Sierra Leone"]

expect_2019_poor = pd.concat([expect_2019_bur, expect_2019_som, \
                              expect_2019_moz, expect_2019_mad, \
                              expect_2019_sie], axis=0)

expect_2019_den = expect_2019.loc[expect_2019["Location"] == "Denmark"]
expect_2019_nor = expect_2019.loc[expect_2019["Location"] == "Norway"]
expect_2019_lux = expect_2019.loc[expect_2019["Location"] == "Luxembourg"]
expect_2019_ire = expect_2019.loc[expect_2019["Location"] == "Ireland"]
expect_2019_swi = expect_2019.loc[expect_2019["Location"] == "Switzerland"]

expect_2019_rich = pd.concat([expect_2019_den, expect_2019_nor, \
                              expect_2019_lux, expect_2019_ire, \
                              expect_2019_swi], axis=0)

# Bar plot of life expectancy for the year 2019
plt.figure()

plt.figure(figsize=(14, 5))
plt.suptitle("Life expectancy of countries in 2019")

plt.subplot(1, 2, 1)
plt.bar(expect_2019_poor["Location"], expect_2019_poor["FactValueNumeric"])
plt.xlabel("Poorest countries")
plt.ylabel("Life expectancy in years")
plt.ylim(0, 85)

plt.subplot(1, 2, 2)
plt.bar(expect_2019_rich["Location"], expect_2019_rich["FactValueNumeric"])
plt.xlabel("Richest countries")
plt.ylabel("Life expectancy in years")
plt.ylim(0, 85)

plt.savefig("life_expectancy_barplot.png")

plt.show()