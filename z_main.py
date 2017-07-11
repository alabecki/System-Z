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

	#worlds = construct_worlds(propositions)  #creates a dictionary of worlds

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
			if check_tolerance(rule, comp) == True:
				temp.append(rule)
				print("Temp:")
				for t in temp:
					print( t.item)
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
