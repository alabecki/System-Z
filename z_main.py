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


options = {
	"1": "Print the z-ranking of R",
	"2": "Print the z-ranking of each world w",
	"3": "Find the z-ranking for a given formula f",
	"4": "Check if 'a |- b' obtains by p-entailment",
	"5": "Check if 'a |- b' obtains by z-entailment",
	"6": "Retuen to previous..."
}


while(True):
	do = ""
	print("____________________________________________________________________")
	print("What would you like to do? ")
	print("____________________________________________________________________")

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

	decomposition = z_partition(rules)

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
		highest = -1
		for r, rule in rules.items():
			if(world.state in rule.bodyExtension and world.state not in rule.headExtension) and (rule.Z) > highest:
				highest = rule.Z
		world.Z = highest +1 

	for w, world in worlds.items():
		print(world.state, world.Z)


	while True:
		opt = " "
		print("\n")
		print("____________________________________________________________________")
		while opt not in options.keys():
			print("What would you like to do?\n")
			for k, v in options.items():
				print("%s: %s" % (k, v))
			print("____________________________________________________________________")
			print("\n")
			opt = input()

		if opt == "1": 
			print("Rules accoding to Z-rank:")
			print("____________________________________________________________________")
			sorted_rules = sorted(rules.values(), key = lambda x: x.Z)
			for rule in sorted_rules:
				print("%s: %s, %s " % (rule.name, rule.item, rule.Z))
			print("____________________________________________________________________")

		if opt == "2":
			print("Worlds sorted by Z-rank:")
			print("____________________________________________________________________")
			sorted_worlds = sorted(worlds.values(), key =lambda x: x.Z)
			for world in sorted_worlds:
				print("%s: %s, %s " % (world.name, world.state, world.Z))
			print("____________________________________________________________________")

		if opt == "3":
			z_rank = -1
			while True:
				try:
					form = input("Please input a well-formed fomula using '&', '|' and '~' as oprators: \n")
					_form = prepare_for_SAT(form)
					z_rank = get_f_Z(_form, decomposition)
					break
				except ValueError:
					print ("That was not a well-formed formula, please try again...")
			z_rank = get_f_Z(_form, decomposition)
			print("____________________________________________________________________")
			print("The Z-rank of %s is %s" % (form, z_rank))
			print("____________________________________________________________________")


		if opt == "4":
			a = input("Please type in the 'a' formula \n")
			b = input("Please type in the 'b' formula \n")
			#res = entailment_0(a, b, rules)
			res = entailment_0Z(a, b, rules)
			print("\n")
			if res == True:
				print("____________________________________________________________________")
				print("%s entails %s " % (a, b))
				print("____________________________________________________________________")

			else:
				print("____________________________________________________________________")
				print("%s does not p-entail %s" % (a, b))
				print("____________________________________________________________________")


		if opt == "5":
			a = input("Please type in the 'a' formula \n")
			b = input("Please type in the 'b' formula \n")
			res = entailment_1(a, b, decomposition)
			print("\n")
			if res == True:
				print("____________________________________________________________________")
				print("%s entails %s " % (a, b))
				print("____________________________________________________________________")

			else:
				print("____________________________________________________________________")
				print("%s does not z-entail %s" % (a, b))
				print("____________________________________________________________________")


		if opt == "6":
			print("....\n")
			break
