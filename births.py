#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup as bs
import urlparse
from urllib2 import urlopen
from urllib import urlretrieve
import operator
import os
import sys

import numpy as np
from scipy.interpolate import interp1d


main_page_url = """http://www.ssa.gov/oact/NOTES/as120/LifeTables_Tbl_7.html"""
test_table = 'http://www.ssa.gov/oact/NOTES/as120/LifeTables_Tbl_7_2100.html'

def get_table_urls(main_page_url):
	url = main_page_url
	url_base = "/".join(url.split("/")[:-1]) + "/"
	soup = bs(urlopen(url))
	year_options = soup.findAll('option')[1:]
	table_urls = [ url_base + str(page_option["value"]) for page_option in year_options]
	table_years = [int(page_option.string) for page_option in year_options]
	return table_urls, table_years

def get_table_data(table_url):
	url = table_url
	soup = bs(urlopen(url))
	table = soup.find("table",border=1)
	rows = table.findAll("tr", valign=None)
	rows = [row for row,x in zip(rows,xrange(len(rows))) if x % 6 != 5 ]
	important = [operator.itemgetter(0,5,12)(row.findAll("div")) for row in rows]
	data = map(lambda x: map(lambda y:float(y.string.replace(",","")),x),important)
	return data

def getAliveIn2014(year, table_data):
	target = 2014 - year;
	for row_data in table_data:
		if (row_data[0] == target):
			return year,row_data[1], row_data[2]
	return year, 0, 0
	
def interpolate_alives(data):
	data_lists = list(zip(*data))
	years = data_lists[0]
	men = data_lists[1]
	women = data_lists[2]
	points = np.linspace(data[0][0], data[-1][0], data[-1][0] - data[0][0] +1)
	# a list of people alive by birth year - first point is from 1900
	return interp1d(years,men)(points)	

if __name__ == "__main__":
	urls, years = get_table_urls(main_page_url)
	data = [get_table_data(url) for url in urls]
	alives = [getAliveIn2014(year, datum) for year, datum in zip(years, data)]
	#print alives
	#data = [(1900, 0.0, 0.0), (1910, 38.0, 328.0), (1920, 8656.0, 30188.0), (1930, 152047.0, 293086.0), (1940, 635974.0, 918450.0), (1950, 1413720.0, 1800863.0), (1960, 2334716.0, 2775347.0), (1970, 3363298.0, 3812498.0), (1980, 4441973.0, 4884318.0), (1990, 5525378.0, 5956736.0), (2000, 6613985.0, 7029283.0), (2010, 7698786.0, 8097976.0), (2020, 0, 0), (2030, 0, 0), (2040, 0, 0), (2050, 0, 0), (2060, 0, 0), (2070, 0, 0), (2080, 0, 0), (2090, 0, 0), (2100, 0, 0)]
	alive_birth_distribution = interpolate_alives(data)
