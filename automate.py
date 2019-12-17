# -*- coding: utf-8 -*-
from transition import Transition
from state import State
import os
import copy
import sp
from sp import *
from itertools import product
from automateBase import AutomateBase


class Automate(AutomateBase):
        
        def succElem(self, state, lettre):
            """State * str -> list[State]

        	rend la liste des états accessibles à partir d'un état
        	state par l'étiquette lettre.
            """
            # successeurs : list[State] 
            successeurs = []
            # t : Transitions
            for t in self.getListTransitionsFrom(state):
                if ((t.etiquette == lettre) and (t.stateDest not in successeurs)):
                    successeurs.append(t.stateDest)
            return successeurs
        ##Testée - fonctionne bien
        
        def succ (self, listStates, lettre):
            """list[State] * str -> list[State]
        
        	rend la liste des états accessibles à partir de la liste d'états
        	listStates par l'étiquette lettre
            """
            # listEtatsAccessibles : list[State] 
            listEtatsAccessibles = [] 
            # s : State
            for s in listStates:
                # successeurs : list[State]
                successeurs = self.succElem(s, lettre) 
                # sp : State 
                for sp in successeurs:
                    if (sp not in listEtatsAccessibles):
                        listEtatsAccessibles.append(sp)
            return listEtatsAccessibles
        ##Testée - fonctionne bien 
        
        
        """ Définition d'une fonction déterminant si un mot est accepté par un automate.
        Exemple :
                a=Automate.creationAutomate("monAutomate.txt")
                if Automate.accepte(a,"abc"):
                    print "L'automate accepte le mot abc"
                else:
                    print "L'automate n'accepte pas le mot abc"
        """
        
        @staticmethod
        def accepte(auto, mot) :
            """ Automate * str -> bool
            
            rend True si auto accepte mot, False sinon
            """
            ## Déjà, premier test : chaque lettre du mot doit avoir au moins un état qui le succède pour que le mot soit accepté
            # listeAux : list[State]
            listeAux = auto.getListInitialStates()
            # listeFins : list[State]
            listeFins = [] 
            # c : char
            for c in mot:
                # s : state
                for s in listeAux:
                    listeFins += auto.succElem(s, c)
                    if(listeFins == []):
                        return False
                    listeAux = listeFins
                    listeFins = []
            ## Si on est là, c'est que le premier test est validé, passons au suivant :) 
            ## ListeAux correspond au dernier listeFins, donc, à la liste complète des états finaux  
            ## Tous les éléments de la liste finale des états successeurs doivent être des états finaux pour que le mot soit accepté
            for s in listeAux: 
                if(s not in auto.getListFinalStates()):
                    return False
            return True
            ## Testée - Fonctionne bien      
                 
        @staticmethod
        def estComplet(auto, alphabet) :
            """ Automate * str -> bool
                
            rend True si auto est complet pour alphabet, False sinon
            """   
            ## Dire qu'un automate est complet revient à dire que chaque état a au moins une transition            
            ## Si alphabet est une chaîne vide, autant directement renvoyer True puisqu'il n'y a pas de transition
            if(len(alphabet) == 0):
                return True 
            # s : state 
            for s in auto.listStates:  ## Je parcours toute la liste des états de l'automate
                # c : char 
                for c in alphabet: ## Je parcours alphabet
                    if(auto.succElem(s, c) == []): ## Si je trouve qu'il y a une lettre qui n'a pas de successeur alors forcément, il n'est pas complet
                         return False
            ## Du coup, l'automate est complet              
            return True # Ils ont tous des successeurs, donc complet 
            ## Testée - fonctionne bien 
        
        @staticmethod
        def estDeterministe(auto) :
            """ Automate  -> bool
                
            rend True si auto est déterministe, False sinon
            """
            ## Dire qu'un automate est déterministe revient à dire que chaque état a une et une seule transition de la meme étiquette
            ## Traitons le cas si alphabet est vide 
            if(len(auto.getAlphabetFromTransitions()) == 0):
                return False
            ## Si on est ici, alors alphabet est non vide 
            # s : state
            for s in auto.listStates: ## Parcourons tous les états de l'automate
                # c : str
                for c in auto.getAlphabetFromTransitions():  ## Parcourons l'alphabet 
                    if(len(auto.succElem(s,c)) > 1): ## si on a plus d'une transition, alors c'est que l'automate n'est pas déterministe
                        return False
            ## Du coup, l'automate est déterministe 
            return True
            ## Testée - fonctionne bien

       
        @staticmethod
        def completeAutomate(auto,alphabet) :
                """ Automate x str -> Automate
                rend l'automate complété d'auto, par rapport à alphabet
                """
                
                #autonew : Automate
                autonew = copy.deepcopy(auto) #on clone auto
                
                if(Automate.estComplet(auto,alphabet)):
                    return autonew #si l'automate est déjà complet, pas besoin de puit
                
                #Letats = list[State]
                Letats = auto.listStates #on récupère la liste de tout les états de l'automate
                #Lid = list[int]
                Lid = [s.id for s in Letats] #récupération de tout les id
                
                #puit = State
                
                puit = State(max(Lid)+1,False,False,"P") #on attribue bien un identifiant unique
                if(autonew.addState(puit)):
                    for s in Letats: 
                        for c in alphabet:
                            if(len(auto.succElem(s,c))==0):
                                autonew.addTransition(Transition(s,c,puit)) #création d'une transition vers le puit
                
                    for c in alphabet:
                        autonew.addTransition(Transition(puit,c,puit)) #rajout des boucles pour chaque lettre sur le puit
                
                return autonew


       
        @staticmethod
        def determinisation(auto) :
                """ Automate  -> Automate
                rend l'automate déterminisé d'auto
                """
                if(Automate.estDeterministe(auto)):
                    return auto
                
                #Lini = list[State]
                Lini = auto.getListInitialStates()
                
                #alphabet : list[String]
                alphabet = auto.getAlphabetFromTransitions()
                
                #cpt : int
                # servira d'id à nos nouveaux états, à incrémenter à chaque création d'état
                cpt = 0
                
                #Lt = list[Transition]
                Lt=[]
                
                #LS = list[State]
                LS = []
                
                #LSp : list[tuple(set[State],Bool,Bool,String]
                LSp = []
                
                #Eini : set[State]
                Eini = {s for s in Lini}
                
                #s0isFinal : boolean
                s0isFinal = False
                
                for s in Eini:
                    if(s.fin):
                        s0isFinal = True
                
                #labels0 : String
                labels0 = "{"
                cptbis = 0
                for s in Lini:
                    cptbis+=1
                    if(cptbis == len(Lini)):
                        labels0+= s.label + "}"
                    else:
                        labels0 += s.label +","
                #on a notre premier état, on l'ajoute à LS :
                LS.append(State(cpt,True,s0isFinal,labels0))
                cpt += 1
                
                #pseudo_s0 : tuple[set[State],Boolean,Boolean]
                pseudo_s0 = Eini
                
                LSp.append(pseudo_s0)
                
                # i : int, indice de l'état de départ courant
                i = 0
                
                # j'ai enlevé la partie "label" des pseudos états qui faisait foirer tout
                for E in LSp:
                    i += 1
                    d = 0
                    for c in alphabet:
                        #Lsucc = liste des successeurs
                        Ltemp = [e for e in E]
                        Lsucc = auto.succ(Ltemp,c) 
                        if(len(Lsucc)!= 0 ):
                            # label temporaire initialisé vide
                            labeltemp = "{"
                            # boolean temporaire à mettre à true si les successeurs contiennent un etat final
                            final = False
                            #boolean temp pour état initial
                            initial = False
                            #Pstemp : pseudo etat initialisé vide
                            Pstemp = ()
                            #Etemp = ensemble d'état temporaire
                            Etemp = set()
                            
                            #on créé les éléments de notre pseudo état
                            cptter = 0
                            for s in Lsucc:
                                cptter+= 1
                                if(cptter == len(Lsucc)):
                                    labeltemp += s.label + "}"
                                else:
                                    labeltemp += s.label +","
                                
                                Etemp.add(s)
                                if(s.fin):
                                    final = True
                                    
                                if(Lsucc == Lini):
                                    initial = True
                                    
                                Pstemp = Etemp
                            
                            if(Pstemp not in LSp):
                                LSp.append(Pstemp)
                                d += 1 
                                #on créé l'état correspondant
                                Stemp = State(cpt,initial,final,labeltemp)
                                cpt += cpt + 1
                                
                                LS.append(Stemp)
                                
                            Ttemp = Transition(LS[i-1],c,LS[i-1+d])
                            Lt.append(Ttemp)
                            
                return Automate(Lt)

    	@staticmethod
    	def complementaire (auto,alphabet) :
        	""" Automate -> Automate
        	rend  l'automate acceptant pour langage le complémentaire du langage de a
        	"""
		#tempAuto : Automate
        	tempAuto = Automate(auto.listTransitions)
        	tempAuto = Automate.completeAutomate(tempAuto,alphabet)
        	tempAuto = Automate.determinisation(tempAuto)
        	for i in tempAuto.listStates:
             		i.fin= not (i.fin)
		return tempAuto


    	@staticmethod
    	def intersection (auto0, auto1):
        	""" Automate x Automate -> Automate
        	rend l'automate acceptant pour langage l'intersection des langages des deux automates
       		 """
		if(auto0.listTransitions==auto1.listTransitions):
        		return Automate(auto0.listTransitions)
        	################### Creation des Variables utiles au programme ########
        	#id : int
        	id=0
        	#test : boolean
        	test=False
        	#Liste_Transition: list[Transition]
        	Liste_Transition=[]
        	#Liste_parcourue ; list[tuple(States)]
        	Liste_parcourue=[]
        	#Liste_temp : list[States]
        	Liste_temp=[]
        	#Liste_temp0 : list[States]
        	Liste_temp0=[]
        	#Liste_temp1 : list[States]
        	Liste_temp1=[]
        	#State_temp1 : States
        	State_temp1=State(0,True,True,"trash")
        	#State_temp2 : States
        	State_temp2=State(0,True,True,"trash1")

       		################# Création de l'alphabet #############################
        	#alphabet0 : str
        	alphabet0 = auto0.getAlphabetFromTransitions()
        	#alphabet1 : str
        	alphabet1 = auto1.getAlphabetFromTransitions()
        	#alphabet : str
        	alphabet= alphabet0
        	for c in alphabet1:
            		if c not in alphabet0:
                		alphabet+=c
        	################# Création de la liste des States initiaux ###############
        	#Liste : list[tuple(States)]
        	Liste=[] ##Notre liste d'attente
        	#Liste0 : list[States]
        	Liste0=auto0.getListInitialStates()
       		#Liste1 : list[States]
       		Liste1=auto1.getListInitialStates()
        	for l0 in Liste0:
            		for l1 in Liste1:
                 		Liste.append((l0,l1))
                 		Liste_parcourue.append((l0,l1))
       	 	################ Création de la liste des States des états finaux #########
        	#Liste0_f : list[States]
        	Liste0_f=auto0.getListFinalStates()
        	#Liste1_f : list[States]
        	Liste1_f=auto1.getListFinalStates()
        	#Liste_f : list[States]
        	Liste_f =Liste0_f
        	for l1 in Liste1_f:
            		if l1 not in Liste0_f:
                		Liste_f.append(l1)
        	################ Création de l'ensemble des States du nouvel automate #########
        	#new_States ; set(State)
        	new_States=set()
        	for l in Liste:
            		if l[0] in Liste_f and l[1] in Liste_f:
                		test=True
            		new_States.add(State(id ,True ,test ,"("+ str (l[0])+ " ; "+ str (l[1])+ ")") )
            		test=False
            		id+=1
        	################ Parcours de la Liste d'attente #############################
        	while(Liste!=[]):
            		s="("+ str (Liste[0][0]) + " ; "+str (Liste[0][1])+")"
            		for l in new_States:
            		    if s==l.label:
            		        State_temp1=l
            		        break

            		for lettre in alphabet:
                		Liste_temp0=auto0.succElem(Liste[0][0],lettre)
                		Liste_temp1=auto1.succElem(Liste[0][1],lettre)
               			for l0 in Liste_temp0: ##automate construit ne doit pas avoir d’ ́etat non accessible depuis l’ ́etat initial
                    			for l1 in Liste_temp1:
                       				if (l0,l1) in Liste_parcourue:
                            				s = "("+str (l0) +" ; "+ str (l1)+")"
                            				for l in new_States:
                                				if s==l.label:
                                    					State_temp2=l
                                    					Liste_Transition.append(Transition(State_temp1,lettre,State_temp2))
                                    					break

                        			else:
                           				if l0 in Liste_f and l1 in Liste_f:   #Test pour voir si l'état sera final
                                				test=True
                            				Liste_parcourue.append((l0,l1))
                            				s= "("+str (l0) + " ; "+str (l1)+")"
                            				State_temp2=State(id,False,test,s)
                            				id+=1
                            				test=False
                            				Liste_Transition.append(Transition(State_temp1,lettre,State_temp2))
                            				new_States.add(State_temp2)
                            				Liste.append((l0,l1))

            		del Liste[0] 

		return Automate(Liste_Transition)


    	@staticmethod
    	def union (auto0, auto1):
        	""" Automate x Automate -> Automate
        	rend l'automate acceptant pour langage l'union des langages des deux automates
       		 """
		 LT = auto0.listTransitions
		 LT.extend(auto1.listTransitions)
        	 Auto2 = Automate(LT)
        	 Auto2 = Automate.determinisation(Auto2)
        	 return Automate2
    

   	@staticmethod
    	def concatenation (auto1, auto2):
        	""" Automate x Automate -> Automate
        	rend l'automate acceptant pour langage la concaténation des langages des deux automates
        	"""
		#Auto1 : Automate
        	Auto1 = copy.deepcopy(auto1)
        	#Auto2 : Automate
        	Auto2 = copy.deepcopy(auto2)
        	#ListeF : list[States]
        	Liste_F = Auto1.getListFinalStates()
        	#ListeIn : list[States]
        	Liste_In = Auto2.getListInitialStates()
        	#Liste1T: list[Transition]
        	Liste1T=Auto1.listTransitions
        	#Liste2T: list[Transition]
        	Liste2T=Auto2.listTransitions
        	#ListeT : List[Transition]
        	ListeT=Liste1T

        	#test : boolean
        	test=False
        	for i in Auto1.listStates:
            		i.insertPrefix(1)
            		if i in Liste_F:
                		i.fin=False
        	Auto2.prefixStates(2)

        	for f in Liste_F:
            		for L in Liste2T:
                		if L.stateSrc in Liste_In:
                    			L.stateSrc = f
                		if L.stateDest in Liste_In:
                    			L.stateDest = f
                		if L in ListeT:
                    			continue
                		ListeT.append(L)

        	return Automate(ListeT)
	
    	@staticmethod
    	def etoile (auto):
        	""" Automate  -> Automate
        	rend l'automate acceptant pour langage l'étoile du langage de a
        	"""
		Auto2 = copy.deepcopy(auto)
       		Trans = []
		
		#On cherche les transitions qui ont pour stateDest un état final
       		for t in Auto2.listTransitions :
            		if (t.stateDest).fin: #Si stateDest est un état final
                		Trans.append(t) #On ajoute la transition à newLT

        	#Pour chaque transition de newLT, on crée une nouvelle transition qui relie stateSrc aux états initiaux et on l'ajoute à l'automate
        	for t in Trans:
            		for i in Auto2.getListInitialStates() :
                		Auto2.addTransition(Transition(t.stateSrc, t.etiquette, i))

       	 	return Auto2
		
                


  
