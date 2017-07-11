

from sympy import Symbol
from sympy.abc import*
from sympy.logic.boolalg import to_cnf
from sympy.logic.boolalg import Not, And, Or
from sympy.logic.inference import satisfiable, valid
from mpmath import*
from itertools import product
import sys
import os
from copy import deepcopy
from shutil import copyfile
from itertools import*
import re

from z_classes import*





def get_file():
	while True:
		file_name = input("Please input the name of a text-file containing a set of rules \n")
		file_name = file_name + ".txt"
		if(os.path.exists(file_name)):
			_file = open(file_name, "r+")
			print("Name of file: %s \n" % (file_name))
			res = [_file, file_name]
			return res
		else:
			print("The file you selected does not exist, please try again\n")
            #filename = input("Select the first/second/third file:")

# Scans the rule file for atomic formulas (letters). This is needed to construct the worlds
def obtain_atomic_formulas(file):
	propositions = set()
	for line in file:
		_line = line.strip()
		_line = re.sub(r'\s+', '', _line)
		_line = _line.split("$")
		_line = _line[0]
		if _line.startswith("(") or _line.startswith("!"):
			_line = _line.replace("~", "")
			_line = _line.replace("&", ",")
			_line = _line.replace("|", ",")
			_line = _line.replace("(", "")
			_line = _line.replace(")", "")
			_line = _line.replace("->", ",")
			_line = _line.replace("!", "")
			new_props = _line.split(",")
			new_props = list(filter(None, new_props))
			for prop in new_props:
				if prop == "":
					continue 
				new = Symbol(prop)
				propositions.add(new)
			#propositions.add(_new)
	return propositions


def delete_file_content(pfile):
    pfile.seek(0)
    pfile.truncate()

# Parses each line of the rule file to create a dictionary of rules, distinguishing the item, body and head. The key is the name of the rule
# while the value is the Rule object itself
def construct_rules_dict(file):
	lines = []
	for line in file:
		line = line.strip()
		if line.startswith("("):
			line = re.sub(r'\s+', '', line)
			lines.append(line.strip())
	steps = []
	for line in lines:
		steps.append(re.split("->|\$", line))
	for step in steps:
		step[0] = step[0][1:]

		step[1] = step[1][:-1]
	rules = {}
	count = 0
	for line in steps:
		name = "r" + str(count)
		if len(line) == 2:
			item = line[0] + " -> " + line[1]
			new = Rule(name, item, line[0], line[1])
		if len(line) == 3:
			item = line[0] + " -> " + line[1] +  " $ " + line[2]
			new = Rule(name, item, line[0], line[1], float(line[2]))
		rules.update({name: new})
		count += 1
	return rules


def construct_worlds(propositions):
	_op = []
	for p in propositions:
		_op.append(str(p))
	_op.sort()
	op = []
	for o in _op:
		new = Symbol(o)
		op.append(new)
	num_worlds = list(range(2**len(propositions)))	#calculates number of rows in the table from which the worlds will be obtained
	world_names = ["w" + str(i) for i in num_worlds]	#creates a unique name for each world: "w" plus an integer
	n = len(propositions)								#number of propositions for table creation
	table = list(product([False, True], repeat=n))		#creation of a truth table
	worlds = {}											#initiates an empty list of worlds
	count = 0
	for row in table:
		state = dict(zip(op, row))
		name = world_names[count]			#each state is a dictionary associating a truth value with each propositional
		new = World(name, state)			#new world object is created with the name and state as attributes
		worlds[name] = new								#the new world is added to the list of worlds
		count +=1
	return worlds


def rule_conditional_formula(rule):
	formula = "~" + rule.body + "|" + rule.head
	return formula

def rule_to_conjuctive_formula(rule):
	formula = rule.body + "&" + rule.head
	return formula


def check_tolerance(rule, sub_rules):
	item = rule_to_conjuctive_formula(rule)
	for char in item:
		char = Symbol(char)
	item = to_cnf(item)
	expression = item
	for sub in sub_rules.values():
		other = rule_conditional_formula(sub)
		for char in other: 
			char = Symbol(char)
		sub.item = to_cnf(other)
		expression = And(expression, sub.item)
		print(expression) 
	if satisfiable(expression) == False:
		print("false")
		return False
	else:
		print("true")
		return True



