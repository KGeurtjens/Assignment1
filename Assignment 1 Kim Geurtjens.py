# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 13:03:57 2023

@author: 20181846
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def one_country(dataset, country):
    """Function that returns a dataset containing only the rows of one
    specified country of the original dataset
    """
    one_country = []
    one_country = dataset.loc[dataset["Location"] == country]
    one_country = one_country[["Period", "FactValueNumeric"]]
    return one_country


def one_year(dataset, year):
    """Function that returns a dataset containing the rows of one
    specified year
    """
    one_year = []
    one_year = dataset.loc[dataset["Period"] == year]
    one_year = one_year[["Location", "FactValueNumeric"]]
    return one_year


def delete(dataset, column, value):
    """Function that deletes rows from a dataset when a specified column
    has a specified value
    """
    deleted = []
    deleted = dataset.drop(dataset[dataset[column] == value].index)
    return deleted


life_expect = pd.read_csv("life_expectancy.csv")

# Remove rows with life expectancy at age 60
life_expect_birth = life_expect.loc[life_expect["Indicator"] ==
                                    "Life expectancy at birth (years)"]

# Make dataset that only keeps the relevant columns for the plots
life_expect_birth = life_expect_birth[["Location", "Period",
                                      "FactValueNumeric"]]

# See all unique countries and periods in dataset
for Location in life_expect_birth:
    print(life_expect_birth[Location].unique())

# Make datasets per country and sort the rows by period,
# replacing the life expectancy with its mean per period
expect_chi = one_country(life_expect_birth, "China")
expect_chi = expect_chi.groupby("Period", as_index=False)[
    "FactValueNumeric"].mean()

expect_rus = one_country(life_expect_birth, "Russian Federation")
expect_rus = expect_rus.groupby("Period", as_index=False)[
    "FactValueNumeric"].mean()

expect_can = one_country(life_expect_birth, "Canada")
expect_can = expect_can.groupby("Period", as_index=False)[
    "FactValueNumeric"].mean()

expect_us = one_country(life_expect_birth, "United States of America")
expect_us = expect_us.groupby("Period", as_index=False)[
    "FactValueNumeric"].mean()

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

# Make dataset that only contains the period 2019 and sort the rows
# by location, replacing the life expectancy with its mean per location
expect_2019 = one_year(life_expect_birth, 2019)
expect_2019 = expect_2019.groupby("Location", as_index=False)[
    "FactValueNumeric"].mean()

# Make datasets per country (for poorest countries)
expect_2019_bur = expect_2019.loc[expect_2019["Location"] == "Burundi"]
expect_2019_som = expect_2019.loc[expect_2019["Location"] == "Somalia"]
expect_2019_moz = expect_2019.loc[expect_2019["Location"] == "Mozambique"]
expect_2019_mad = expect_2019.loc[expect_2019["Location"] == "Madagascar"]
expect_2019_sie = expect_2019.loc[expect_2019["Location"] == "Sierra Leone"]

# Append the individual datasets into one
expect_2019_poor = pd.concat([expect_2019_bur, expect_2019_som,
                              expect_2019_moz, expect_2019_mad,
                              expect_2019_sie], axis=0)

# Make datasets per country (for richest countries)
expect_2019_den = expect_2019.loc[expect_2019["Location"] == "Denmark"]
expect_2019_nor = expect_2019.loc[expect_2019["Location"] == "Norway"]
expect_2019_lux = expect_2019.loc[expect_2019["Location"] == "Luxembourg"]
expect_2019_ire = expect_2019.loc[expect_2019["Location"] == "Ireland"]
expect_2019_swi = expect_2019.loc[expect_2019["Location"] == "Switzerland"]

# Append the individual datasets into one
expect_2019_rich = pd.concat([expect_2019_den, expect_2019_nor,
                              expect_2019_lux, expect_2019_ire,
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

# Make dataset that only contains the periods of 2000 and 2019
expect_not_2010 = delete(life_expect_birth, "Period", 2010)
expect_2000_2019 = delete(expect_not_2010, "Period", 2015)
expect_2000_2019 = expect_2000_2019.groupby(["Location", "Period"],
                                            as_index=False) \
                                            ["FactValueNumeric"].mean()

# Make sure that the datasets of 2000 and 2019 have the right column
# names for their life expectancy values, so they can be merged into
# one dataset
expect_all_2000 = expect_2000_2019.loc[(expect_2000_2019["Period"] == 2000)]
expect_all_2000 = expect_all_2000.reset_index(drop=True)
expect_all_2000.columns = ["Location", "Period", "2000"]
expect_all_2000 = expect_all_2000["2000"]

expect_all_2019 = expect_2000_2019.loc[(expect_2000_2019["Period"] == 2019)]
expect_all_2019 = expect_all_2019.reset_index(drop=True)
expect_all_2019.columns = ["Location", "Period", "2019"]
expect_all_2019 = expect_all_2019["2019"]

expect_scatter = pd.concat([expect_all_2000, expect_all_2019], axis=1)

# Scatter plot of life expectancy of countries in 2000 versus 2019
plt.figure()

plt.figure(figsize=(6, 6))

plt.scatter(expect_scatter["2000"], expect_scatter["2019"])

plt.title("Life expectancy of all countries in 2000 versus 2019")
plt.xlabel("Life expectancy of year 2000")
plt.ylabel("Life expectancy of year 2019")
plt.xlim(40, 85)
plt.ylim(40, 85)

plt.savefig("life_expectancy_scatter.png")

plt.show()