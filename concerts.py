#!/home/zach/anaconda3/bin/python
# -*- coding: utf-8 -*-

""" Scrapes krcl's live music calendar and makes dict with k, v pairs {concert_datetime: concert name}
"""

from datetime import datetime
from bs4 import BeautifulSoup
import requests
import pprint

def make_show_list(url=None, page_num=1, show_titles=None, show_times=None):

	# Initialize URL
	if not url:
		url = 'https://krcl.org/events/?category=live-music'
	page_response = requests.get(url, timeout=5)
	page_content = BeautifulSoup(page_response.content, 'html.parser')

	# Initialize show_times
	if not show_times:
		show_times = [str(e.text) for e in page_content.find_all("span", attrs={'class:', 'post-date'})]
	else: # Concatenate show_times and new page
		show_times += [str(e.text) for e in page_content.find_all("span", attrs={'class:', 'post-date'})]
	# Initialize show_titles
	if not show_titles:
		show_titles = [str(e.text) for e in page_content.find_all("h1")]
	else: # Concatenate show_titles and new page.
		show_titles += [str(e.text) for e in page_content.find_all("h1")]

	# Checks for a next page. If there is, function calls itself with new page. Otherwise, proceeds to prepare final list.
	if bool((page_content.find_all('a', attrs={'class': 'next '}))): 
		page_num += 1
		url = f'https://krcl.org/events/?category=live-music&page={page_num}'
		return make_show_list(url, page_num, show_titles, show_times)

	# When no more pages, zip show titles and dates/times together and return list of tuples.
	else:
		filtered_show_times = [e for e in show_times if not (str(e).startswith("CATEGORY"))]
		zipped_dict = dict(zip(filtered_show_times, show_titles))
		return zipped_dict

upcoming_shows = make_show_list()
pprint.pprint(upcoming_shows)
