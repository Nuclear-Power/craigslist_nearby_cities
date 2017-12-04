import ast
import json
import re

#set as needed to change line weight in the output file
line_weight = 3
#out.txt is the file created by get_data.py
infile = open("out.txt", "r", encoding="utf-8").read()
cities_dict = ast.literal_eval(infile)

"""
create a 'name': 'city name' dict
"""
city_name_list = list(cities_dict.keys())
names_strings = ['name' for _ in range(len(city_name_list))]
nodes = []
for i in range(len(city_name_list)):
	node_entry = {names_strings[i]: city_name_list[i]}
	nodes.append(node_entry)

#create the nodes section of the D3 json file
node_section = {"nodes": nodes}

"""
create the links section of the D3 json
"""
links = []
for i in range(len(nodes)):
	#gets city 
	y = city_name_list[i]
	z = cities_dict[city_name_list[i]] #[] to get value of this
	#get the nearby cities for city i 
	for j in range(0, len(z)):
		city_to_search = z[j]
		#nasty hack to break at 'more' in our list, not sure how to get it out
		if city_to_search == 'more ...':
			break
		target_index = city_name_list.index(city_to_search)
		link_entry = {"source": i, "target": target_index, "weight": line_weight}
		links.append(link_entry)

link_section = {"links": links}

"""
put node_section and link_section together
"""

node_section.update(link_section)

#write the final json in D3 form
outfile = open('final.json', 'w')
outfile.write(json.dumps(node_section))
outfile.close()