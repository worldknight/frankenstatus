# FRANKENSTATUS
# Adapted from the original program written by William Sims Bainbridge in
# Sociology Laboratory: Computer Simulations for Learning Sociology (1987)

# Import Packages
import sys #For exiting
import numpy as np ## For calculating correlations
import pandas as pd #For data storage
import plotly.express as px ##For plots
import random ## For calculating chances
from unique_names_generator import get_random_name ## For name generation
from unique_names_generator.data import ADJECTIVES, ANIMALS  ## To make name generation more fun.
import copy ## For swapping 
import tqdm
from tqdm import trange  ##For progress display

# Reset Identiity and Attempt Counter
ident = 0
attempt = 0
np.random.seed(123)

#Print synopsis
with open('synopsis.txt') as synopsis:
	while True:
		line = synopsis.readline()
		if not line:
			break
		print(line)

input('Press Enter or Return to continue... ')
print('\n' *4)

# Creating Individual Units
class Initial_Member:
	'''Individual members are assigned numbers, names, and a body and intelligence rating'''
	def __init__(self, ident, name, original_mind_stat, body_stat):
		self.ident= ident
		self.name = name
		self.original_mind_stat = original_mind_stat
		self.body_stat = body_stat

#Creating Names
names_list = [ ]
num = int(input('How many people are to be invited by Dr. Frankenstatus?  '))
for i in range(num):
	name = get_random_name(combo = [ADJECTIVES, ANIMALS], separator = " ")
	if name in names_list:
		print('Duplicate: ' + name)
		name = get_random_name(combo = [ADJECTIVES, ANIMALS], separator = " ")
		print('Substitute: ' + name)
		names_list.append(name)
	else:
		names_list.append(name)


random.shuffle(names_list)

#Creating Categories
def set_mind():
	'''Setting up intelligence rating'''
	original_mind_stat = random.randint(0, 100)
	#print(f'Mind Score: {mind_chance}')
	return original_mind_stat

def set_body():
	'''Setting up body rating'''
	body_stat = random.randint(0, 100)
	#print(f'Body Score: {body_chance}')
	#print('\n')
	return body_stat

# Generating People
person_attributes = [ ]
people = []
people_data = pd.DataFrame(columns = ['ID', 'Name', 'original_mind_stat', 'body_stat'])
for i in range(num):
	ident = ident + 1
	person_attributes.append((ident, names_list[i], set_mind(), set_body()))
for ident, name, original_mind_stat, body_stat in person_attributes:
	person = Initial_Member(ident, name, original_mind_stat, body_stat)
	person.current_body_name = name
	people.append(person)
	people_data.loc[(len(people_data))] = [ident, name, original_mind_stat, body_stat]

def mind_score_labels(row):
	if row['original_mind_stat'] <= 50:
		return 'dim'
	else: 
		return 'bright'

def body_score_labels(row):
	if row['body_stat'] <= 50:
		return 'ugly'
	else: 
		return 'beautiful'

people_data['mind'] = people_data.apply(mind_score_labels, axis = 1)
people_data['body'] = people_data.apply(body_score_labels, axis = 1)


#Generate Initial List of People
print('*' * 60)
people_data = people_data.reset_index(drop = True)
print(str(num) + ' people have arrived:')
for person in people:
	if person.original_mind_stat >= 50:
		mind = 'bright'
	else:
		mind = 'dim'
	if person.body_stat >= 50:
		body = 'beautiful'
	else:
		body = 'ugly'
	print(f'{person.name} is {mind} and {body}')
	print('*' * 60)


#Plot
#Basic Scatterplot and Quadranting
plot = px.scatter(people_data, x = "original_mind_stat", y = "body_stat", text = None, hover_data = "Name")
#Quadrant axes
body_axis = ['ugly', 'beautiful']
mind_axis = ['dim', 'bright']


#Averages and ticks
x_avg = people_data['original_mind_stat'].mean()
y_avg = people_data['body_stat'].mean()

plot.add_vline(x = x_avg, line_width = 1)
plot.add_hline(y= y_avg, line_width = 1)

adj_x = max((people_data['original_mind_stat'].max() - x_avg), (x_avg - people_data['original_mind_stat'].min())) * 1.1
adj_y = max((people_data['body_stat'].max() - y_avg), (y_avg - people_data['body_stat'].min())) * 1.1

lb_x, ub_x = (x_avg - adj_x, x_avg + adj_x)
lb_y, ub_y = (y_avg - adj_y, y_avg + adj_y)

#Correlation
matrix = np.corrcoef(people_data['original_mind_stat'], people_data['body_stat'])
coef = str(matrix[0,1])
coef_percentage = f"{float(coef):.0%}"

plot.update_xaxes(range = [lb_x, ub_x])
plot.update_yaxes(range = [lb_y, ub_y])

plot.update_layout(
	xaxis_title = 'Mind Score',
	xaxis = dict(tickmode = 'array', tickvals = ([(x_avg - adj_x /2), (x_avg + adj_x /2)]), ticktext = mind_axis, showgrid = False))

plot.update_layout(
	yaxis_title = 'Body Score',
	yaxis = dict(tickmode = 'array', tickvals = ([(y_avg - adj_y /2), (y_avg + adj_y /2)]), ticktext = body_axis, showgrid = False))

# Quadrant Group Labels
plot.update_layout(
    title=dict(text = ('<br>FRANKENSTATUS RELATIONS' + '<br><b><i>Correlation: </i></b>' + coef),
           automargin =  True,
           y = 1.0,
           x = 0.5,
           xanchor = 'center',
           yanchor = 'top',
           font = dict(
           	family = "Calibri, monospace",
           	variant = "small-caps",
           	)))

##Beautiful, Dim
plot.add_annotation(dict(
	font = dict(color = 'black', size = 18, family = 'Calibri, monospace', variant = "unicase"),
	x = people_data['original_mind_stat'].min(),
	y = people_data['body_stat'].max(),
	text = '<b><i>Beautiful & Dim</i></b>', xref = 'x', yref ='y',  showarrow = False))

##Beautiful, Bright
plot.add_annotation(dict(
	font = dict(color = 'black', size = 18, family = 'Calibri, monospace', variant = "unicase"),
	x = people_data['original_mind_stat'].max(),
	y = people_data['body_stat'].max(),
	text = '<b><i>Beautiful & Bright</i></b>', xref = 'x', yref= 'y', showarrow = False))

##Ugly, Dim
plot.add_annotation(dict(
	font = dict(color = 'black', size = 18, family = 'Calibri, monospace', variant = "unicase"),
	x = people_data['original_mind_stat'].min()-0.2,
	y = people_data['body_stat'].min() - 0.2,
	text = '<b><i>Ugly & Dim</i></b>', xref = 'x', yref= 'y', showarrow = False))

##Ugly, Bright
plot.add_annotation(dict(
	font = dict(color = 'black', size = 18, family = 'Calibri, monospace', variant = "unicase"),
	x = people_data['original_mind_stat'].max(),
	y = people_data['body_stat'].min(),
	text = '<b><i>Ugly & Bright</i></b>', xref = 'x', yref= 'y', showarrow = False))

plot.update_traces(textposition = 'top right')

#Update Plot
plot.update_layout(
    height = 500,
    showlegend = False,
    plot_bgcolor = 'white',
    font_family = 'Courier New, monospace'
)

#Write Initial Plot
plot.write_html('start.html')
people_data.to_csv('start.csv', index = False)
print('The current data is saved in a chart labeled start.html. A spreadsheet labeled start.csv is also saved.')
print('\n' * 5)
print('-' * 60)
print(f'The current correlation between mind and body is {coef}. This means that mind and body are roughly {coef_percentage} correlated')

#Set up threshold
print('Dr. Frankenstatus is going to switch the member\'s bodies!')
print('A correlation of 1.0 would mean that the most \'beautiful\' people are also the \'smartest\' \nA correlation of -1.0 would mean that the most \'beautiful\' people are also the \'dimmest\'. \n')
threshold = float(input('What is the correlation  you want to aim for? \nHINT: Try for something lower than the current correlation. '))
tries = int(input('How many times do you want to run this? '))
exchange_frame= [ ]

def swapping_time(people, tries, threshold):
	''' Dr. Frankenstatus has unleashed the psychexchanger. God help us. In actuality, all this does is swap the scores between units.'''

	exchange_frame_setup = people[:]

	#Setup Swap Frame (SF):
	swapped = pd.DataFrame(columns = ['ID', 'Name', 'original_mind_stat', 'body_stat', 'current_body_name'])

	class Swap_Member:
		'''Dr. Frankenstatus has swapped two members' minds.'''
		def __init__(self, ident, name, original_mind_stat, body_stat, current_body_name):
			self.ident= ident
			self.name = name
			self.original_mind_stat = original_mind_stat
			self.body_stat = body_stat
			self.current_body_name= current_body_name

	for person in exchange_frame_setup:
		person.current_body_name = person.name
		new_class_person = Swap_Member(person.ident, person.name, person.original_mind_stat, person.body_stat, person.current_body_name)
		exchange_frame.append(new_class_person)
		swapped.loc[len(swapped)] = [person.ident, person.name, person.original_mind_stat, person.body_stat, person.current_body_name]

	#Search for best possible correlation
	with tqdm.tqdm(total = tries) as pbar:
		for i in range(tries):
			best_swap = None
			current_coef = float(coef)
			best_coef = current_coef

			for j in range(len(swapped)):
				for k in range(j+1, len(swapped)):
					temp_swap = swapped.copy()
					temp_swap.loc[j, 'body_stat'], temp_swap.loc[k, 'body_stat'] = temp_swap.loc[k, 'body_stat'], temp_swap.loc[j, 'body_stat']
					temp_swap.loc[j, 'current_body_name'], temp_swap.loc[k, 'current_body_name'] = temp_swap.loc[k, 'current_body_name'], temp_swap.loc[j, 'current_body_name']
					new_coef = np.corrcoef(temp_swap['original_mind_stat'], temp_swap['body_stat'])[0,1]
					#print(f" Current: {temp_swap.loc[j, 'Name']} and {temp_swap.loc[k, 'current_body_name']} * Current Correlation: {new_coef}")
	
				if threshold < 0: #For positive correlation
					if abs(threshold - new_coef) < abs(threshold - best_coef):
						best_swap =(j, k)
						best_coef = new_coef
				else: #For negative correlation
					if abs(threshold - new_coef) > abs(threshold - best_coef):
						best_swap =(j, k)
						best_coef = new_coef
			if best_swap:
				swapped.loc[best_swap[0], 'body_stat'], swapped.loc[best_swap[1], 'body_stat'] = swapped.loc[best_swap[1], 'body_stat'], swapped.loc[best_swap[0], 'body_stat']
				swapped.loc[best_swap[0], 'current_body_name'], swapped.loc[best_swap[1], 'current_body_name'] = swapped.loc[best_swap[1], 'current_body_name'], swapped.loc[best_swap[0], 'current_body_name']
				current_coef = best_coef
				pbar.set_description(f"Best:  {swapped.loc[best_swap[0], 'Name']} and {swapped.loc[best_swap[1], 'Name']} * Current Correlation: {current_coef}")
				if abs(current_coef - threshold) <= 0.01: #Arbitrary value
					pbar.set_description(f' Swap {i+1}: Target achieved!')
					print(f"Swap {i} successful.")
					pbar.close()
					return swapped
				
			pbar.update()

swapped = swapping_time(people, tries, threshold)
if swapped is None:
	print(f'{tries} attempts were insufficient to  improve this set. Dr. Frankenstatus has failed!')
	sys.exit()
#Basic Scatterplot and Quadranting
print(swapped)
new_matrix = np.corrcoef(swapped['original_mind_stat'], swapped['body_stat'])
new_coef = str(new_matrix[0,1])
new_coef_percentage = f"{float(new_coef):.0%}"

new_plot = px.scatter(swapped, x = "original_mind_stat", y = "body_stat", text = None, hover_data = ["Name", "current_body_name"])

#Averages and ticks
x_avg = swapped['original_mind_stat'].mean()
y_avg = swapped['body_stat'].mean()

new_plot.add_vline(x = x_avg, line_width = 1)
new_plot.add_hline(y= y_avg, line_width = 1)

adj_x = max((swapped['original_mind_stat'].max() - x_avg), (x_avg - swapped['original_mind_stat'].min())) * 1.1
adj_y = max((swapped['body_stat'].max() - y_avg), (y_avg - swapped['body_stat'].min())) * 1.1

lb_x, ub_x = (x_avg - adj_x, x_avg + adj_x)
lb_y, ub_y = (y_avg - adj_y, y_avg + adj_y)

new_plot.update_xaxes(range = [lb_x, ub_x])
new_plot.update_yaxes(range = [lb_y, ub_y])

new_plot.update_layout(
	xaxis_title = 'Mind Score',
	xaxis = dict(tickmode = 'array', tickvals = ([(x_avg - adj_x /2), (x_avg + adj_x /2)]), ticktext = mind_axis, showgrid = False))

new_plot.update_layout(
	yaxis_title = 'Body Score',
	yaxis = dict(tickmode = 'array', tickvals = ([(y_avg - adj_y /2), (y_avg + adj_y /2)]), ticktext = body_axis, showgrid = False))

# Quadrant Group Labels
new_plot.update_layout(
    title=dict(text = ('<br>FRANKENSTATUS RELATIONS' + '<br><b><i>Correlation: </i></b>' + new_coef),
           automargin =  True,
           y = 1.0,
           x = 0.5,
           xanchor = 'center',
           yanchor = 'top',
           font = dict(
           	family = "Calibri, monospace",
           	variant = "small-caps",
           	)))

##Beautiful, Dim
new_plot.add_annotation(dict(
	font = dict(color = 'black', size = 18, family = 'Calibri, monospace', variant = "unicase"),
	x = swapped['original_mind_stat'].min(),
	y = swapped['body_stat'].max(),
	text = '<b><i>Beautiful & Dim</i></b>', xref = 'x', yref ='y',  showarrow = False))

##Beautiful, Bright
new_plot.add_annotation(dict(
	font = dict(color = 'black', size = 18, family = 'Calibri, monospace', variant = "unicase"),
	x = swapped['original_mind_stat'].max(),
	y = swapped['body_stat'].max(),
	text = '<b><i>Beautiful & Bright</i></b>', xref = 'x', yref= 'y', showarrow = False))

##Ugly, Dim
new_plot.add_annotation(dict(
	font = dict(color = 'black', size = 18, family = 'Calibri, monospace', variant = "unicase"),
	x = swapped['original_mind_stat'].min()-0.2,
	y = swapped['body_stat'].min() - 0.2,
	text = '<b><i>Ugly & Dim</i></b>', xref = 'x', yref= 'y', showarrow = False))

##Ugly, Bright
new_plot.add_annotation(dict(
	font = dict(color = 'black', size = 18, family = 'Calibri, monospace', variant = "unicase"),
	x = swapped['original_mind_stat'].max(),
	y = swapped['body_stat'].min(),
	text = '<b><i>Ugly & Bright</i></b>', xref = 'x', yref= 'y', showarrow = False))

new_plot.update_traces(textposition = 'top right')

#Update new_plot
new_plot.update_layout(
    height = 500,
    showlegend = False,
    plot_bgcolor = 'white',
    font_family = 'Courier New, monospace'
)

#Write New Data
new_plot.write_html('compare.html')
swapped.to_csv('compare.csv', index = False)












