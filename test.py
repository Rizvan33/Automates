# -*- coding: utf-8 -*-

from automate import Automate
from state import State
from transition import Transition
from parser import *

print "\n\t|Testons les méthodes de la classe Automate|\n"

s = State(1, False, False)
s2=State(1, True, False)
t = Transition(s,"a",s)
t2=Transition(s,"a",s2)
s.insertPrefix(2)
a= Automate([t,t2])
a.prefixStates(3)
s1=State(1, True, False)
s2=State(2, False, True)
t1= Transition(s1,"a",s1)
t2=Transition(s1,"a",s2)
t3=Transition(s1,"b",s2)
t4=Transition(s2,"a", s2)
t5=Transition(s2,"b",s2)
liste = [t1,t2,t3,t4,t5]
a=Automate(listStates=[], label="a", listTransitions=liste) 
a.prefixStates(0)
a.removeTransition(t5)
a.removeTransition(t5)
a.addTransition(t5)
a.addTransition(Transition(s2,"c", s1))
a.addTransition(Transition(s2,"c",s1))
sr1 = State(0, True, False)
ss = State(1, False, True)
ts = Transition(sr1, "a", ss) 
tr = Transition(sr1, "b", sr1) 
listeb = [ts, tr] 
b=Automate(listStates=[], label="b", listTransitions=listeb)
print "b : \n"
print b 
a.show("essaiA")
b.show("essaiB")
print "======================================================\n"
print "L'automate a sur lequel nous testons nos fonctions : \n"
print a
print "======================================================\n"

print "******************************************************\n"
list = [s1,s2]
print "Test de la fonction succ\n"
print "Pour list = [s1, s2]\n"
print "a.succ(list, \"c\")"
print a.succ(list,"c")
print "\n"
print "a.succ(list, \"b\")"
print a.succ(list,"b")
print "\n"
print "a.succ(list, \"a\")"
print a.succ(list,"a")
print "\n******************************************************\n"

print "Automate.accepte(a, \"abc\")\n"
print Automate.accepte(a, "abc") ## False 
print "Automate.accepte(a, \"aaabbcb\")\n"
print Automate.accepte(a, "aaabbcb") ##True
print "Automate.accepte(a, \"abs\")\n"
print Automate.accepte(a, "abs") ## False 

print "\n******************************************************\n"
print "Automate.estComplet(a, [\"a\", \"b\", \"c\"])"
print Automate.estComplet(a, ["a", "b", "c"])
print Automate.estComplet(a, ["0", "1"]) 
print Automate.estComplet(a, ["a", "b"]) 
print "\n******************************************************\n"
print Automate.estDeterministe(a)
print Automate.estDeterministe(b) 
print "\n******************************************************\n"
print "a.completeAutomate\n"
print Automate.completeAutomate(a, ["a", "b", "c"])
(Automate.completeAutomate(a, ["a", "b", "c"])).show("completA") 

print "\n******************************************************\n"
print "Automate.determinisation(b)\n"
c = Automate.determinisation(b)
print c
c.show("DeterminisationB")
print "\n"
print "Automate.determinisation(a)\n"
c1 = Automate.determinisation(a)
print c1
c1.show("DeterminisationA")
print "\n******************************************************\n"

print "Automate.complementaire(a,[\"a\", \"b\"])\n"
d = Automate.complementaire(a, ["a", "b"])
print d
d.show("ComplementaireA")

print "\n******************************************************\n"
print "Automate.intersection(a, b)\n"
e = Automate.intersection(a, b)
print e
e.show("IntersectionAB")

print "\n******************************************************\n"
print "Automate.union(a, b)\n"
f = Automate.union(a, b)
print f
f.show("UnionAB")
print "\n******************************************************\n"

print "Automate.concatenation(a, b)\n"
g = Automate.concatenation(a, b)
print g
g.show("ConcatenationAetB")
print "\n******************************************************\n"
print "Automate.etoile(a)\n"
h = Automate.etoile(a)
print h
h.show("EtoileA")
print "\n******************************************************\n"


print "\n\t|Toutes les méthodes ont été testées|\n"









