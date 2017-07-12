#/usr/bin/python3

# System Z Solver ___________________________________________________________________________________________________________

 #Libraries______________________________________________________________________________________________________________________
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

from z_functions import*
from z_classes import*



while(True):
	do = ""
	print("What would you like to do? \n")
	while(do != "1" and do !="2"):
		do = input("1: Open a file, 2: Exit program\n")
		if(do == "2"):
			sys.exit()
		if(do == "1"):
			res = get_file()
			file = res[0]
			file_name = res[1]
		else:
			print("I'm sorry, could you repeat your command? \n")

	file.seek(0)
	propositions = obtain_atomic_formulas(file)
	#for p in propositions:					#fetches all atomic formulas found in a rule or constraint
		#print (p)
	file.seek(0)
	#rules = {}
	rules = construct_rules_dict(file)		# parses input text, make a Rule object for each rule, saves objects in dictionary
	file.seek(0)

	worlds = construct_worlds(propositions)  #creates a dictionary of worlds


	# Get Z-partition of Rules
	decomposition = dict()
	count = 0
	remaining_rules = deepcopy(rules)
	remaining_shadow = deepcopy(rules)

	while len(remaining_rules.keys()) > 0:
		print("Len rules: %s" % (len(remaining_rules.keys())))
		print("Remaining rules:")
		temp = []
		for r in remaining_rules.keys():
			print(r, end=" ")
		for r, rule in remaining_rules.items():
			comp = deepcopy(remaining_rules)
			del comp[r]
			item = deepcopy(rule)
			item = rule_to_conjuctive_formula(item)
			item = prepare_for_SAT(item)
			if check_tolerance(item, comp) == True:
				temp.append(rule)
				print("Count: %s" % (count))
				print("rule: %s" % (rule.item))
				rules[r].Z = count 
				print("rule z: %s" % (rule.Z))
				#for t in temp:
				#	print( t.item)
				del remaining_shadow[r]
		name = "d" + str(count)
		decomposition[name] = temp
		remaining_rules = deepcopy(remaining_shadow)
		print("Current len remaining rules: %s" % (len(remaining_rules.keys())))
		count += 1

	for d, v in decomposition.items():
		print (d)
		for r in v:
			print (r.item)

	for k, rule in rules.items():
		rule.bodyExtension = assign_extensions(rule.body, worlds, propositions)		#obtains extension of bodies of rules
		rule.headExtension = assign_extensions(rule.head, worlds, propositions)		#obtains extensions of heads of rules

	for r, rule in rules.items():
		print(rule.item, rule.Z)
	

	for w, world in worlds.items():
		highest = 0
		for r, rule in rules.items():
			if(world.state in rule.bodyExtension and world.state not in rule.headExtension) and (rule.Z + 1) > highest:
				highest = rule.Z
		world.Z = highest +1 

	#for w, world in worlds.items():
	#	print(world.state, world.Z)

	#get Z value of a formula

	#print("Please enter a formula to check: \n")
	#form = input()
	#form_Z = get_f_Z(form, decomposition)
	#print(form_Z)
	print("You can now check if some 'a' 0- entails some 'b'\n")
	a = input("Please type in the 'a' formula ")
	b = input("Please type in the 'b' formula ")
	res = entailment_0(a, b, rules)
	if res == True:
		print("%s entails %s " % (a, b))
	else:
		print("%s does not entail %s" % (a, b))

	print("You can now check if some 'a' 1-entails some 'b' \n")
	a = input("Please type in the 'a' formula ")
	b = input("Please type in the 'b' formula ")
	res = entailment_1(a, b, decomposition)
	if res == True:
		print("%s entails %s " % (a, b))
	else:
		print("%s does not entail %s" % (a, b))

