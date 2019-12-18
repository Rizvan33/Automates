# -*- coding: utf-8 -*-

from automate import Automate
from state import State
from transition import Transition
from parser import *

print "\n|Testons les méthodes de la classe Automate|\n"

## On crée les deux atomates de tests 

## Préparations pour la création de l'automate a 
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
## Création de l'automate a 
a = Automate(listStates=[], label="a", listTransitions=liste) 
## Traitements sur l'automate a (modifications) 
a.prefixStates(0)
a.removeTransition(t5)
a.removeTransition(t5)
a.addTransition(t5)
a.addTransition(Transition(s2,"c", s1))
a.addTransition(Transition(s2,"c",s1))

## Préparations pour la création de l'automate b 
sr1 = State(0, True, False)
ss = State(1, False, True)
ts = Transition(sr1, "a", ss) 
tr = Transition(sr1, "b", sr1) 
listeb = [ts, tr] 
## Création de l'automate b 
b = Automate(listStates=[], label="b", listTransitions=listeb)

## Présentation des deux automates de test a et b 
print "******************************************************\n"
print "Présentation des deux automates de test a et b\n"

print "======================================================\n"
print "L'automate a sur lequel nous testons nos méthodes : \n"
print a
## pdf du a 
#a.show("essaiA")
print "======================================================\n"


print "======================================================\n"
print "L'automate b sur lequel nous testons nos méthodes : \n"
print b 
## pdf du b
#b.show("essaiB")
print "======================================================\n"

print "******************************************************\n"
## Fin de la présentation des deux automates a et b 

print "Testons les méthodes\n"

print "******************************************************\n"
list = [s1,s2]
print "Test de la méthode succ\n"
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

print "******************************************************\n"
print "Test de la méthode accepte\n"
print "Automate.accepte(a, \"abc\") : "
print Automate.accepte(a, "abc") ## résultat attendu : False
print "\n" 
print "Automate.accepte(a, \"aaabbcb\") : "
print Automate.accepte(a, "aaabbcb") ## résultat attendu : True
print "\n"
print "Automate.accepte(a, \"abs\") : "
print Automate.accepte(a, "abs") ## résultat attendu : False 
print "\n******************************************************\n"

print "******************************************************\n"
print "Test de la méthode estComplet\n"
print "Automate.estComplet(a, [\"a\", \"b\", \"c\"]) : "
print Automate.estComplet(a, ["a", "b", "c"])
print "\n Automate.estComplet(a, [\"0\", \"1\"]) : "
print Automate.estComplet(a, ["0", "1"]) 
print "\n Automate.estComplet(a, [\"a\", \"b\"]) : "
print Automate.estComplet(a, ["a", "b"]) 
print "\n******************************************************\n"

print "******************************************************\n"
print "Test de la méthode estDeterministe\n" 
print "Automate.estDeterministe(a) :\n"
print Automate.estDeterministe(a)
print "\nAutomate.estDeterministe(b) :\n"
print Automate.estDeterministe(b) 
print "\n******************************************************\n"

print "******************************************************\n"
print "Test de la méthode completeAutomate\n"
print "Automate.completeAutomate(a, [\"a\", \"b\", \"c\"]) : \n"
k = Automate.completeAutomate(a, ["a", "b", "c"])
print k 
## Création du pdf
#k.show("completA")
print "\n******************************************************\n"

print "********************************************************\n"
print "Test de la méthode determinisation\n"
print "Automate.determinisation(b) :\n"
c = Automate.determinisation(b)
print c
## Création du pdf 
#c.show("DeterminisationB")
print "\nAutomate.determinisation(a)\n"
c1 = Automate.determinisation(a)
print c1
## Création du pdf
#c1.show("DeterminisationA")
print "\n******************************************************\n"

print "********************************************************\n"
print "Test de la méthode complementaire\n"
print "Automate.complementaire(a,[\"a\", \"b\"]) :\n"
d = Automate.complementaire(a, ["a", "b"])
print d
## Création du pdf
#d.show("ComplementaireA")
print "\n******************************************************\n"

print "********************************************************\n"
print "Test de la méthode intersection\n"
print "Automate.intersection(a, b) : \n"
e = Automate.intersection(a, b)
print e
## Création du pdf 
#e.show("IntersectionAB")
print "\n******************************************************\n"

print "********************************************************\n"
print "Test de la méthode union\n"
print "Automate.union(a, b) : \n"
f = Automate.union(a, b)
print f
## Création du pdf
#f.show("UnionAB")
print "\n******************************************************\n"

print "********************************************************\n"
print "Test de la méthode concatenation\n"
print "Automate.concatenation(a, b): \n"
g = Automate.concatenation(a, b)
print g
## Création du pdf 
#g.show("ConcatenationAetB")
print "\n******************************************************\n"

print "********************************************************\n"
print "Test de la méthode etoile\n"
print "Automate.etoile(a)\n"
h = Automate.etoile(a)
print h
## Création du pdf
#h.show("EtoileA")
print "\n******************************************************\n"

print "\n\t|Toutes les méthodes ont été testées|\n"









