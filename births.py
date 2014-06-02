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

verbose=False

main_page_url = """http://www.ssa.gov/oact/NOTES/as120/LifeTables_Tbl_7.html"""
test_table = 'http://www.ssa.gov/oact/NOTES/as120/LifeTables_Tbl_7_2100.html'

def log(*args):
	if verbose:
		print args

def get_table_urls(main_page_url):
	url = main_page_url
	url_base = "/".join(url.split("/")[:-1]) + "/"
	log("looking up index", url)
	soup = bs(urlopen(url))
	year_options = soup.findAll('option')[1:12]
	table_urls = [ url_base + str(page_option["value"]) for page_option in year_options]
	table_years = [int(page_option.string) for page_option in year_options]
	log("fetched list of urls to use")
	return table_urls, table_years

def get_table_data(table_url):
	url = table_url
	log("looking up table", url)
	soup = bs(urlopen(url))
	log("found table")
	table = soup.find("table",border=1)
	rows = table.findAll("tr", valign=None)
	rows = [row for row,x in zip(rows,xrange(len(rows))) if x % 6 != 5 ]
	important = [operator.itemgetter(0,2,9)(row.findAll("div")) for row in rows]
	data = map(lambda x: map(lambda y:float(y.string.replace(",","")),x),important)
	log("found data")
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
	if len(sys.argv) > 0 and sys.argv[1] == "-v":
		print "Setting verbose to be true"
		verbose=True
	urls, years = get_table_urls(main_page_url)
	data = [get_table_data(url) for url in urls]
	alives = [getAliveIn2014(year, datum) for year, datum in zip(years, data)]
	log(alives)
	alive_birth_distribution = interpolate_alives(alives)
