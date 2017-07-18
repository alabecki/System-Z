

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


def base():
	do = ""
	res = []
	while len(res) == 0:
		print("\n")
		print("What would you like to do? \n")
		do = input("1: Open a file, 2: Exit program\n")
		if(do == "2"):
			sys.exit()
		if(do == "1"):
			print("Please input the name of a text-file containing a set of rules ")
			print("(or press 'r' to return) \n")
			name = input()
			if name != "r":
				res = get_file(name)
				if res == []:
					continue
				#print(type(res))
				return res

		else:
			print("I'm sorry, could you repeat your command? \n")
	return res


def get_file(name):
	while True:
		if name.endswith(".txt") == False:
			name = name + ".txt"
		if(os.path.exists(name)):
			_file = open(name, "r+")
			print("\n")
			print("Name of file: %s " % (name))
			res = [_file, name]
			return res
		else:
			print("The file you selected does not exist, please try again")
			print("(Or press 'r' to return) \n ")
			name = input()
			if name == 'r':
				res = []
				return res

# Scans the rule file for atomic formulas (letters). This is needed to construct the worlds
def obtain_atomic_formulas(file):
	propositions = set()
	for line in file:
		_line = line.strip()
		_line = re.sub(r'\s+', '', _line)
		_line = _line.split("$")
		_line = _line[0]
		if _line.startswith("(") or _line.startswith("!"):
			_line = _line.replace("FALSE", "")
			_line = _line.replace("TRUE", "")
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

def add_rule(rule, rules):
	rule = rule.strip()
	rule = re.sub(r'\s+', '', rule)
	step = (re.split("->|\$", rule))
	#print("Step 0 %s " % (step[0]))
	#print("Step 1 %s " % (step[1]))
	step[0] = step[0][1:]
	step[1] = step[1][:-1]
	count = len(rules)
	name = "r" + str(count)
	if len(step) == 1:
		item = " " + " -> " + step[0]
		new = Rule(name, item, " " , step[0])
	if len(step) == 2:
		item = step[0] + " -> " + step[1]
		new = Rule(name, item, step[0], step[1])
	if len(step) == 3:
		item = step[0] + " -> " + step[1] +  " $ " + step[2]
		new = Rule(name, item, step[0], step[1], float(step[2]))
	rules.update({name: new})


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

# Assigns each rule head and rule body a set of possible worlds, namely those in which it is true
#Since a given rule body/head will typically not include all atomic propositions found within the rule-set, directly applying  #a SAT solver on this formula will not give us the worlds we are looking for, since each world should assign truth values to  #all propositions found in the rule-set. So given a body/head x, if P is a proposition found in the set of rules but not in x, #then x will be augmented with &(P | ~P).
def assign_extensions(formula, worlds, propositions):
	extension = []
	if str(formula).isspace() or len(str(formula)) == 0 or str(formula) == "TRUE":			#if the formula is empty it will be treated as a toutology
		for w in worlds.values():
			extension.append(w.state)
		return extension
	if str(formula) == "FALSE":
		return extension
	else:
		props_in_formula = set()		#store propositions found in the formula
		for char in str(formula):
			add = Symbol(char)
			props_in_formula.add(add)
		props_not_in_form = propositions.difference(props_in_formula)	#Determine which propositions are missing from the rule's body
		supplement = Symbol('')
		#print("formula: %s " % (formula))
		form_cnf = to_cnf(formula)
		for p in props_not_in_form:
			supplement = Or(p, Not(p))							#Loop aguments (P | ~P) for each P not found in body
			form_cnf = And(form_cnf, supplement)
		#print("__form_cnf: %s \n" % (form_cnf))
		form_SAT = satisfiable(form_cnf, all_models = True)  #The sympy SAT solver is applied to the augmented formula
		form_SAT_list = list(form_SAT)				       #the ouput of satisfiable() is an itterator object so we turn it into a list
		if(len(form_SAT_list) == 1 and form_SAT_list[0] == False):		#check to handle inconsistencies
			extension = []
			return extension
		else:
			for state in form_SAT_list:		#We now turn each state in which the body is true into a dictionary so that
				new = {}						#they may be directly compared with each world state
				for key, value in state.items():
					new[key] = value
					if new not in extension:
						extension.append(new)
	return extension

def prepare_for_SAT(formula):
	for char in formula:
		char = Symbol(char)
	symb_form = to_cnf(formula)
	return symb_form


def rule_conditional_formula(rule):
	if rule.head == "FALSE":
		formula = "~(" + rule.body + ")"
		return formula
	if rule.body == "TRUE":
		formula = rule.head
		return formula
	formula = "~(" + rule.body + ")|" + rule.head
	return formula

def rule_to_conjuctive_formula(rule):
	if rule.head == "FALSE":
		formula = "~(" + rule.body + ")"
		return formula
	if rule.body == "TRUE":
		formula = rule.head
		return formula
	formula = rule.body + "&" + rule.head
	return formula

def check_tolerance(item, sub_rules):
	expression = item
	for sub in sub_rules.values():
		other = rule_conditional_formula(sub)
		#print("other before: %s" % (other))
		other = prepare_for_SAT(other)
		#print ("Other after: %s" % (other))
		expression = And(expression, other)
	#print(expression) 
	if satisfiable(expression) == False:
		##print("false")
		return False
	else:
		return True

def z_partition(rules):
	decomposition = dict()
	count = 0
	remaining_rules = deepcopy(rules)
	remaining_shadow = deepcopy(rules)
	num_rules = len(rules.keys())
	trials = 0
	while len(remaining_rules.keys()) > 0 and count <= num_rules:
		##print("Len rules: %s" % (len(remaining_rules.keys())))
		#print("Remaining rules:")
		#for k, v in remaining_rules.items():
		#	print(k, v.item)
		temp = []
		#for r in remaining_rules.keys():
		#	print(r, end=" ")
		for r, rule in remaining_rules.items():
		#	print("Current rule: %s" % (rule.item))
			comp = deepcopy(remaining_rules)
			del comp[r]
			item = deepcopy(rule)
			item = rule_to_conjuctive_formula(item)
			item = prepare_for_SAT(item)
			if check_tolerance(item, comp) == True:
				temp.append(rule)
			#	print("Count: %s" % (count))
			#	print("rule: %s" % (rule.item))
				rules[r].Z = count 
			#	print("rule z: %s" % (rule.Z))
			#	for t in temp:
			#		print( t.item)
				del remaining_shadow[r]
		name = "d" + str(count)
		decomposition[name] = temp
		remaining_rules = deepcopy(remaining_shadow)
		if len(remaining_rules.keys()) == 0:
			break
		#print("Current len remaining rules: %s" % (len(remaining_rules.keys())))
		count += 1
	if len(remaining_rules.keys()) > 0 :
		decomposition = dict()
	return decomposition

def get_f_Z(formula, decomposition):
	Z = len(decomposition) -1
	if len(decomposition.keys()) == 0:
		return 10000
	#limit = Z 
	flag = False
	check = {}
	while Z >= 0:
		key = "d" + str(Z)
		#print("Key is %s" % (key))
		temp = decomposition[key]
		for d in temp:
			check[d.name] = d
		#for k, v in check.items():
		#	print(k, v.item)
		if check_tolerance(formula, check):
			Z -= 1
			flag = True
		else:
			if flag == False:
				return 10000
			else:
				return Z + 1
		#limit -= 1 
	if flag == False:
		return 10000
	return Z + 1

def entailment_0(a, b, rules):
	first = "~" + a + "|" + b 
	second = "~" + a + "|" + "~" + b 
	first = prepare_for_SAT(first)
	second = prepare_for_SAT(second)
	expression = And(first, second)
	for k, v in rules.items():
		frule = rule_conditional_formula(v)
		frule = prepare_for_SAT(frule)
		expression = And(expression, frule)
	expression = And(expression, Not(b))
	#print(expression)
	if satisfiable(expression) == False:
		return True
	else:
		return False

def entailment_0Z(a, b, rules):
	KB = deepcopy(rules)
	new = "(" + a + "->" + "~" + b + ")"
	#print("new: %s" % (new))
	add_rule(new, KB)
	#print("KB:")
	#for k, v in KB.items():
	#	print(k, v.item)
	decomp = z_partition(KB)
	if len(decomp.keys()) == 0:
		return True
	else:
		return False
	


def entailment_1(a, b, decomposition):
	a = prepare_for_SAT(a)
	b = prepare_for_SAT(b)
	affirm = And(a, b)
	deny = And(a, Not(b))
	affirmZ = get_f_Z(affirm, decomposition)
	denyZ = get_f_Z(deny, decomposition)
	#print("Affirm Z: %s" % (affirmZ))
	#print("Deny Z: %s" % (denyZ))
	if affirmZ < denyZ:
		return True
	else:
		return False





