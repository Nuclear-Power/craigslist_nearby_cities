import urllib
from bs4 import BeautifulSoup as bs
import re
import json
import time

LINKS = []
url = "https://newyork.craigslist.org/" #the center of the world
RESULTS = {}


city_page = urllib.request.urlopen(url)
soup = bs(city_page, "html.parser")

current_city = soup.find('h2', attrs={"class": "area"}).get_text()

right_bar = soup.find('ul', attrs={"class": "acitem"})

#get all the cities from the current page into a list
cities = []
for a in right_bar.find_all(href=True):
	cities += a

#get all the links for each of the cities into a list
for link in right_bar.find_all('a', attrs={'href': re.compile("^//")}):
	LINKS.append("https:" + link.get('href'))

city_links = dict(zip(cities, LINKS))

RESULTS[current_city] = cities

def funct(city, city_list, city_links):
	""" 
	assembles a dictionary to write to a file
	
	input city->str and city_list
	output: {city->str, city_list-list}
	"""

	if city_list == []:
		return RESULTS
	print("cities left to analyze = {}".format(len(city_list)))
	print('collecting data for {}'.format(city))
	print("Waits 2s, then runs")
	time.sleep(5)
	print()

	try:
		city_page = urllib.request.urlopen(city_links[city])
		
	except:
		print("connection error - waiting then retrying")
		#sleep for 300s if there is a connection error then try again
		time.sleep(120)
		try:
			print("retrying")
			city_page = urllib.request.urlopen(city_links[city])
		except:
			print("connection error - return and writing data")
			return RESULTS

	#parse the html data
	soup = bs(city_page, "html.parser")
	current_city = soup.find('h2', attrs={"class": "area"}).get_text()
	#print(current_city)
	right_bar = soup.find('ul', attrs={"class": "acitem"})

	#get the nearby cities for the current city and add them to our
	cities_to_add = []
	for a in right_bar.find_all(href=True):
		cities_to_add += a
	#create a new list of cities

	#so maybe here when we make a set of it it removes duplicates, but we still need some of them
	city_list = list(set(cities_to_add + city_list))
	city_list.remove(city)

	links_for_new_cities = []
	for link in right_bar.find_all('a', attrs={'href': re.compile("^//")}):
		links_for_new_cities.append("https:" + link.get('href'))

	#this is a new dict of cities and links to merge with city_links
	city_links_to_add = dict(zip(cities_to_add, links_for_new_cities))
	city_links.update(city_links_to_add)

	del city_links[city]
	#need to do something like if city: city_links_to_add not in results then add it
	#or if it is different maybe

	#remove city_link entries for cities that already have results
	city_links = {key: city_links[key] for key in city_links if key not in RESULTS}
	try:
		del city_links[city]
	except:
		pass
	#remake city_list to remove cities that have results
	city_list = [key for key in city_links]
	city_list.sort()

	RESULTS.update({city: cities_to_add})

	try:
		return RESULTS + funct(city_list[0], city_list, city_links)
	except TypeError:
		return RESULTS	

x = funct(cities[0], cities, city_links)

#open file and print our RESULTS to it
f = open('out.txt', 'w')
f.write(json.dumps(x))
f.close()