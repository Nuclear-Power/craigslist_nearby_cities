import urllib
from bs4 import BeautifulSoup as bs
import re
import json
import time

city_list = []
cities_and_links = {}
RESULTS = []
t = ()

'''
This script works and colects the data, but it is slightly different than the one I used to 
build the site. Craiglist may have updated their pages to include the state of the city,
which throws off the edges in the graph that is built. 

The current version of this script outputs a tuple with tupler_maker() but can output a 
dictionary with output_builder()
'''

class City(object):
	"""
	a city that has a page on craigslist

	Attributes:
		name: a string representing the city's name
		link: a string representing the craiglist url of the city
		nearby cities: a list containing the cities that are listed as "nearby" the 
		city_page: the city's page html
		right_bar: the right bar on the page that contains the nearby city links
	"""
	def __init__(self, url):
  		self.url = url; 
  		self.city_page = urllib.request.urlopen(self.url)
  		self.soup = bs(self.city_page, "html.parser")
  		self.right_bar = self.soup.find('ul', attrs={"class": "acitem"})
  		self.name = self.soup.find('h2', attrs={"class": "area"}).get_text()

	def get_nearby_cities(self):
	    nearby_cities = []
	    for a in self.right_bar.find_all(href=True):
	      nearby_cities += a
	    #print(self.nearby_cities)
	    return nearby_cities

	def get_nearby_city_links(self):
		links = []
		for link in self.right_bar.find_all('a', attrs={'href': re.compile("^//")}):
			links.append("https:" + link.get('href'))
		return links

	def cities_and_links_updater(self):
		return dict(zip(self.get_nearby_cities(), self.get_nearby_city_links()))

	def output_builder(self):
		return {self.name: self.get_nearby_cities()}

	'''
	create a tuple with the following data (name, city url, list of nearby cities, city's modified name)
	this deals with the issue where when a city is listed as a nearby city, its name will be slightly 
	different than the one listed on its own page
	'''

	def tuple_maker(self):
		return (self.name, self.url, self.get_nearby_cities(), self.get_modified_name())

	def get_modified_name(self): 
		'''
		find the first  city on the sidebar, follow its link, find the target city in 
		that city's nearby city list, and return that name, which is the modified name 
		for the city
		'''
		links = self.get_nearby_city_links()
		first_city_link = links[0]
		first_city_page = urllib.request.urlopen(first_city_link)
		first_city_soup = bs(first_city_page, "html.parser")
		nearby_list_html = first_city_soup.find('ul', attrs={"class": "acitem"})
		nearby_list_cities = []
		for city in nearby_list_html.findAll('a'):
			nearby_list_cities.append(city.string)
		for city in nearby_list_cities:
			if city == self.name:
				#if the name is the same as the modified name
				return self.name
			if ',' in self.name: 
				arr = self.name.split(',')
				new_name = arr[0]
				if city == new_name:
					return new_name
		return self.name

city_list = ['new york']
cities_and_links = {'new york': "https://newyork.craigslist.org/"}
completed_cities = []

while len(city_list) >0:
	current_city = city_list[0]
	print("Current City: " + str(current_city) + "\n")
	#exception for 'more ...'  which shows up in nearby cities
	#sometime, if more delete and continue on
	if city_list[0] == 'more ...':
		city_list.pop(0)
		current_city = city_list[0]

	x = City(cities_and_links[city_list[0]])
	#add entries from the current city to the city list
	city_list = list(set(city_list + x.get_nearby_cities()))
	#updated completed cities with the current city
	completed_cities.append(current_city)
	#now we remove completed cites from city list so they aren't processed again
	city_list = [x for x in city_list if x not in completed_cities]
	city_list.sort()

	cities_and_links.update(x.cities_and_links_updater())
	#RESULTS.update(x.output_builder(x.url))
	RESULTS.append(x.tuple_maker())
	print("--> cities left: {} \n".format(len(city_list)))
	#time.sleep(5)

f = open('out.txt', 'w')
f.write(json.dumps(RESULTS))
f.close()
print("results writting to out.txt")
print('end of script')