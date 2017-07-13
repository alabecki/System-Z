_________________________________________________________________________
System Z Default Reasoning Solver 
_________________________________________________________________________ 
 
0. Installation
To run the program, a computer must have Python 3.x installed.
The program was written on Python 3.6 but may run correctly on older 
versions. It is, however, recommended that the user should have 3.4 or higher
installed. The program can be opened in on the command-line in Windows or Linux
machines. 

In the command line, go to the directory in which you have placed the 
folder containing the program and type:

	python main.py

(If you have Anaconda installed on your computer you need only type 
“main.py”)

The program makes use of the logic module from the sympy library, which 
is itself dependent upon the pmath library. If these have not been 
installed, the user will be informed when trying to run the program. 
It is recommended that the user employ pip when installing Python libraries.
To install sympy and pmath using pip simply type:

pip install sympy
pip install pmath

(Linux users may need to preface these commands with the customary 
“sudo”)

If you have both Python 2.x and 3.x installed on your system, your system Python 2.x 
might be the default version, which will cause trouble both when trying to run the program 
and when installing modules with pip for Python 3. 

If this is the case, type the following into the command prompt: 
	alias python='/usr/bin/python3'

Then install sympy as follows:
	python3.x -m pip install sympy  # specifically Python 3.x

_________________________________________________________________________


1. Introduction

The program is designed to compute the z-rank of rules, worlds, and formulas determined
by a ruleset, R, provided by the user. A z-ranking is over something like a perference 
or norality relation. If item alpha has a higher z-ranking than item beta, then alpha is
more unexpected, exceptional, or unusual than beta. The z-rankings of rules, which induces a 
partition of R (when R is consistant) is used determine the z-entailment of any formulas 
a, b supplied by the user.

The program can also check for the weaker p-entailment relation between two given formulas.
a p-entails b if adding the rule (a -> ~b) makes R inconsistant.  
____________________________________________________________________________

2. Rulesets 

Rulesets are prvoded by the user in the form of ‘.txt’ files. Upon starting the
program the user will be asked if he or she would like to open a file.

Rules must be written in the following format: (b -> h), where 'b' and 'h' 
are formulas of propositional logic. "&" is used for "and", "|" is used for
"or", and "~" is used for negation. 

Atomic propositions are composed of one or more Latin letters. 
The sympy module reserves I, E, S, N, C, O, and Q for imarginary numbers, 
so they should not be used in propositions. For this reason it is recommended that the user stick with lower-case letters.  

		Example:	( (~par | (~qu | r)) -> (qu & par) ) 

  
The program is fairly flexible with the use of parentheses, with the 
following exceptions:

	(1) The outermost parentheses for rules must be included
	(2) Any parentheses required for understanding the meaning of the
	expression must be included 

Moreover, spacing within a line is ignored. The following rule is 
perfectly acceptable: 

		Example: (a   & ~b &c -> p | q |r) 
 
IMPORTANT: Rules must appear on lines by themselves or the program will not
be able to parse them correctly. Also, the first character of a rule line 
MUST be “(“.
 
Some example ruleset text files are included with the program. 
  
_________________________________________________________________________

3. Commands

After the program read and procsses a ruleset file, the following options
will be presented:

	1: Print the z-ranking of R
	2: Print the z-ranking of each world w
	3: Find the z-ranking for a given formula f
	4: Check if 'a |- b' obtains by p-entailment
	5: Check if 'a |- b' obtains by z-entailment
	6: Retuen to previous...
 

The commands are generally self-explanatory. 

The first gives the z-rank of each rule 
in R and the second does the same for each possible world relative to R.

The third command will propt the user to enter a formula and will return its z-rank
relative to R. 

The fouth and fifth commands each prompt the user to input two formulas in sequence and 
tell the user whether the first entails the second. In 4, the program tests for p-entailment,
while, in the second, it tests for z-entailment. 

Finally, the sixth option takes the use back to the start, where a new file may be opened or the user may exit the program.

