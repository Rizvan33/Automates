# -*- coding: utf-8 -*-
from transition import *
from state import *
import os
import copy
from sp import *
from parser import *
from itertools import product
from automateBase import AutomateBase

"""
2. Prise en main
"""

"""
2.1 Création d'automates 
"""

"""
1.
"""

## création des états s0, s1 et s2

# s0 : state
s0 = State(0, True, False, "s0")

# s1 : state
s1 = State(1, False, False, "s1")

# s2 : state 
s2 = State(2, False, True, "s2")
 

## création des transtions t1, t2, t3, t4, t5 et t6

# t1 : Transition
t1 = Transition(0, "a", 0)

# t2 : Transition
t2 = Transition(0, "b", 1)

# t3 : Transition
t3 = Transition(1, "a", 2)

# t4 : Transition
t4 = Transition(1, "b", 2)

# t5 : Transition
t5 = Transition(2, "a", 0)

# t6 : Transition
t6 = Transition(2, "b", 1)


## création de la liste listeA
# listeA : list[Transition]
listeA = [t1, t2, t3, t4, t5, t6]

## création de l'automate auto correspondant à A 
# auto : Automate
auto = Automate(listeA)

## Verification que l'automate auto correspond bel et bien à A 
print(auto)
auto.show("A_ListeTrans")




