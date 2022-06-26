# Data Visualization of the America Film Institute's Top 100 movies of all time

The American Film Institute (AFI) has maintained a [list of the top 100 movies of all time](https://www.afi.com/afis-100-years-100-movies-10th-anniversary-edition/). As a film enthusiast, I have been watching movies off of this list for the past year and a half. This repository contains some code to
create several plots which highlight different elements, from genres to actors and awards. These tell us a lot about these movies, how they differ from
the thousands of movies created over the same period but also how they have changed over time.

There is a lot more to be done with this data. I have written a Medium article with my findings, but my hope is that this will encourage people to take up
where I left off, and unearth more insights from the wealth of data present. Anyone is welcome to re-use my code, with proper citation.

## Prerequisites

The core of the analysis is included in the R markdown file. While I have included a PDF version, should you want to run and modify the code yourself, you will need to take the following steps.

### Install the libraries

You need to have the most updated versions of the ggplot2, rvest, data.table and tidyverse libraries. A simple set of install.packages statements should
get you there.

### Download the data

While I did some web scraping to get the list of movies (included in the R code), I relied extensively on IMDb to get additional information. You should
download all the files available [here](https://datasets.imdbws.com/) and store them in your working directory. In addition, I used [this dataset](https://datahub.io/rufuspollock/oscars-nominees-and-winners) to track Academy Awards winners over time (thanks to rufuspollock for making this data easily available on Datahub). 

### Run the Python script

While R is great for statistical computing and data visualization, it proved to be annoyingly slow at some data wrangling tasks. Hence, I wrote a simple
Python script to do some of these, leaving as much as I could self-contained in the R markdown document. Once you have all the files, simply run `python3 aggregate_principals.py` to create crew_info.csv.

### Set working directory

My file structure assumes that all the files are stored in an Articles/ directory. Should you change this, you will need to edit the setwd statements in the code.

## Run the code

You now have everything you need to run the code! Use your favorite R GUI (R Studio for my part), run the code and enjoy seeing the charts appear on your screen. As stated above, you are welcome to re-use all or part of my code for your analysis, as long as you properly cite that I was the original writer. I look forward to seeing the great things you will create and knowledge you will unearth!
