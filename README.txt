_________________________________________________________________________
System Z Default Reasoning Solver 
_________________________________________________________________________ 
 

0. Installation

To run the program, a computer must have Python 3.x installed. The program 
was written on Python 3.6 but may run correctly on older versions. Version 
3.4 or higher, however, is recommended. The program can be opened in on the 
command-line in Windows or Linux machines. 

In the command line, go to the directory in which you have placed the 
folder containing the program and type:

	python z_main.py

(If you have Anaconda installed on your computer you need only type 
“z_main.py”)

The program makes use of the logic module from the sympy library. It is 
recommended that the user employ pip when installing Python libraries. To 
install sympy simply type:

       pip install sympy	(perhaps with a “sudo”)


If you have both Python 2.x and 3.x installed on your system, it might 
run Python 2.x by default, which will cause trouble both when trying to 
run the program and when installing modules. 

If this is the case, type the following into the command prompt: 
	
	alias python='/usr/bin/python3'   (Linex)
	
	alias python='python3'		  (Mac)

Then install sympy as follows:
	
	python3.x -m pip install sympy    (Mac)

If you have trouble installing through pip, please try using Easy Install:

	easy_install sympy		(perhaps with sudo prefixed)

This second way of installing sympy may be necessary even if you already
have python 3 active.

If none of these methods of installing sympy work see:

http://docs.sympy.org/latest/install.html

_________________________________________________________________________


1. Introduction

The program is designed to compute the z-rank of rules, worlds, and formulas 
determined by a ruleset, R, provided by the user. z-ranking is based on 
“system z” as presented in Judea Pearl (1990) and Moisés Goldszmidt and 
Judea Pearl (1996). 

A z-ranking is over something like a preference or normality relation. If item
alpha has a higher z-ranking than item beta, then alpha is more unexpected, 
exceptional, or unusual than beta. (Inconsistent formulas are the most 
“unexpected”and have an infinite z-ranking). The z-ranking of a set of rules R
induce a partitionof R (when R is consistent) and is used to determine the
z-entailment of any formulas
a, b supplied by the user.

The program can also check for the weaker p-entailment relation between two
given formulas. a p-entails b if adding the rule (a -> ~b) makes R inconsistent
(so it cannot be fully partitioned into a z-ranking).  
_________________________________________________________________________

2. Rulesets 

Rulesets are provided by the user in the form of ‘.txt’ files. Upon starting
the program, the user will be asked if he or she would like to open a file.

Rules must be written in the following format: (b -> h), where 'b' and 'h' are
formulas of propositional logic. "&" is used for "and", "|" is used for "or", 
and "~" is used for “not”. Material implication must be expressed in terms of 
these symbols.

Atomic propositions are composed of Latin letters. I, E, S, N, C, O, and Q, 
however, should not be used because sympy reserves them for imaginary numbers.
It is recommended that the user stick with lower-case letters.  

	Example 1:	((~par | (~qu | r)) -> (qu & par)) 

The program is flexible regarding the use of parentheses, with the following 
exceptions:

	(1) The outermost parentheses for rules must be included
	(2) Any parentheses required for removing ambiguity from the      
            meaning of a formula must be included 

Spacing within a line is ignored. The following rule is perfectly acceptable: 

	Example 2: (abs   & ~b &c -> p | q |re) 
 
IMPORTANT: Rules must appear on lines by themselves or the program will not 
be able to parse them correctly. Also, the first character of a rule line MUST 
be “(“.

Rules do not need to have bodies, but they do need to have heads.
	
	Example 3: (  -> p|q)

In this example, p or q ought to be the case by default, but this default might
be overturned by a rule with a body:
	
	Example 4: (r -> ~(p|q))

“TRUE” and “FALSE” can be used when defining rules: 
	
       Example 5: (pm & hs -> FALSE)
       
       Example 6: (TRUE -> p|q)
       
       Example 7: (~(p|q) -> FALSE)

Ex. 5 is the rule that, normally, pm and hs are not both true. Ex. 6 and 7 are
both notational variants of Ex.3.  
	

Some example ruleset text files are included with the program. 
  
_________________________________________________________________________

3. Commands

After the program reads and processes a ruleset file, the following options will
be presented:

	1: Print the z-rankings of R
	2: Print the z-ranking of each world w
	3: Find the z-ranking for a given formula f
	4: Check if 'a |- b' obtains by p-entailment
	5: Check if 'a |- b' obtains by z-entailment
	6: Return to previous...
 

The commands are generally self-explanatory. 

The first gives the z-rank of each rule in R and the second does the same for 
each possible world. The third command will prompt the user to enter a formula and 
will return its z-rank with respect to R. The fourth and fifth commands each prompt
the user to input two formulas in sequence and tell the user whether the first 
p-entails/z-entails the second.
Finally, the sixth option takes the use back to the start, where a new file may be 
opened or the user may exit the program.


_________________________________________________________________________

References

Judea Pearl. 1990. System Z: a natural ordering of defaults with tractable
applications to nonmonotonic reasoning. In Proceedings of the 3rd conference
on Theoretical aspects of reasoning about knowledge (TARK '90). Morgan Kaufmann
Publishers Inc., San Francisco, CA, USA, 121-135.


Moisés Goldszmidt, Judea Pearl. 1990. Qualitative probabilities for default reasoning,
belief revision, and causal modeling. Artificial Intelligence, Volume 84, Issue 1, 
1996, 57-112.

