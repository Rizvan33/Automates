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
            successeurs = [] ## Initalisée à vide pour la constuire par la suite, sera retournée à la fin. Si pas de successeurs, alors vide direcement (trivial)
            # t : Transitions ## Variable courante
            for t in self.getListTransitionsFrom(state): ## On parcourt toutes les listes des transitions
                if ((t.etiquette == lettre) and (t.stateDest not in successeurs)): ## Pas dans les successeurs (unicité) et etiquette c est la lettre
                    successeurs.append(t.stateDest) ## on rajoute 
            return successeurs ## On retourne la liste
        ##Testée - fonctionne bien (fonction donnée de base)
        
        def succ (self, listStates, lettre):
            """list[State] * str -> list[State]
        
        	rend la liste des états accessibles à partir de la liste d'états
        	listStates par l'étiquette lettre
            """
            # listEtatsAccessibles : list[State] 
            listEtatsAccessibles = [] ## Initalisée à vide pour la constuire par la suite, sera retournée à la fin. Si pas d'états accessibles, alors vide direcement (trivial)
            # s : State ## Variable courante
            for s in listStates: ## On parcourt toute la liste des états 
                # successeurs : list[State]
                successeurs = self.succElem(s, lettre)  ## Liste des états accesibles à partir de l'état s par l'étiquette lettre 
                # sp : State ## Variable courante
                for sp in successeurs: ## On parcourt tous les états de cette liste
                    if (sp not in listEtatsAccessibles): ## Si elle n'y ait pas déjà, alors on la rajoute (pour l'unicité)
                        listEtatsAccessibles.append(sp) 
            return listEtatsAccessibles ## On retourne la liste :)
        ##Testée - fonctionne bien 
        
        
        """ Définition d'une fonction déterminant si un mot est accepté par un automate.
        Exemple :
                a=Automate.creationAutomate("monAutomate.txt")
                if Automate.accepte(a,"abc"):
                    print "L'automate accepte le mot abc"
                elisteDeStatese:
                    print "L'automate n'accepte pas le mot abc"
        """
        
        @staticmethod
        def accepte(auto, mot) :
            """ Automate * str -> bool
            
            rend True si auto accepte mot, False sinon
            """
            ## Déjà, premier test : chaque lettre du mot doit avoir au moins un état qui le succède pour que le mot soit accepté
            # listeAux : list[State]
            listeAux = auto.getListInitialStates() ## On a la liste de tous les états Initiales de l'automate, d'ou on peut commencer, donc
            # listeFins : list[State]
            listeFins = [] ## liste initialisée à vide, pour la "construire" par la suite
            # c : char ## variable courante
            for c in mot: ## on parcourt tout le mot
                # s : state
                for s in listeAux: ## La première fois, parcourt tous les états Initiales de l'automate, puis lors de l'itération les états qui succèdent à la fin
                    listeFins += auto.succElem(s, c)  ## On prend les états qui succèdent pour constuire listeFins à chaque fois, comme expliqué plus bas
                    if(listeFins == []): ## On n'a pas du tout de successeurs, donc, le mot n'est pas accepté (puisqu'elle est restée vide la liste)
                        return False
                    listeAux = listeFins ## Pour parcourir les états qui succèdent, on dirait qu'on prend un nouvel automate qui accepte ce qui reste du mot à chaque fois
                    listeFins = [] ## On remet à vide pour refaire le test à chaque nouvelle fois 
            ## Si on est là, c'est que le premier test est validé, passons au suivant :) car cela n'est pas suffisant 
            ## ListeAux correspond, maintenant au dernier listeFins, donc, à la liste complète des derniers états finaux trouvés
            ## Tous les éléments de la liste finale des états successeurs doivent être des états finaux pour que le mot soit accepté (en général, il n'y en aura qu'un d'ailleurs)
            for s in listeAux:  ## On parcourt la liste des derniers états finaux
                if(s not in auto.getListFinalStates()): ## Si ce n'est pas un état final, alors le mot n'est pas accepté
                    return False
            return True ## mot accepté puisque le permier et deuxième test (si on est là) sont validés
            ## Testée - Fonctionne bien      
                 
        @staticmethod
        def estComplet(auto, alphabet) :
            """ Automate * str -> bool
                
            rend True si auto est complet pour alphabet, False sinon
            """   
            ## Dire qu'un automate est complet revient à dire que chaque état a au moins une transition (par l'étiquette)          
            ## Si alphabet est une chaîne vide, autant directement renvoyer True puisqu'il n'y a pas de transition 
            if(len(alphabet) == 0):
                return True 
            # s : state ## variable courante
            for s in auto.listStates:  ## On parcout toute la liste des états de l'automate
                # c : char ## variable courante
                for c in alphabet: ## On parcourt alphabet
                    if(auto.succElem(s, c) == []): ## Si on trouve ne serait ce qu'une lettre qui n'a pas de successeur alors, forcément, l'automate n'est pas complet
                         return False
            ## Si on est là, c'est que tous les lettres de l'alphabet ont des successeurs. Du coup, l'automate est complet              
            return True ## IlisteDeStates ont tous des successeurs, donc complet 
            ## Testée - fonctionne bien 
        
        @staticmethod
        def estDeterministe(auto) :
            """ Automate  -> bool
                
            rend True si auto est déterministe, False sinon
            """
            ## Dire qu'un automate est déterministe revient à dire que chaque état a une et une seule transition de la meme étiquette
            ## Traitons le cas si alphabet est vide PAS DU TOUT DE TRNASITIONS, en fait c'est l'alphabet de estComplet :p
            if(len(auto.getAlphabetFromTransitions()) == 0):
                return False
            ## Si on est ici, alors alphabet est non vide 
            # s : state ## Variable courante
            for s in auto.listStates: ## Parcourons tous les états de l'automate
                # c : str ## Variable courante
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
                ## Dire qu'un automate est complet revient à dire que chaque état a au moins une transition (par l'étiquette) 
                ## On doit, donc, rajouter les transitions manquante pour compléter l'automate :)
                
                ## On va renvoyer un automate, donc, clonons le pour ne pas toucher à l'original :) 
                #autonew : Automate ## nouvel automate à renvoyer après qu'il soit complet
                autonew = copy.deepcopy(auto) ## On clone auto ## copy seul ne marche pas, ce n'est pas une méthode
                
                ## L'automate peut déjà être complet, alors on le renvoie directement 
                if(Automate.estComplet(auto,alphabet)):
                    return autonew ## on aurait pu pour une meilleure optimisation (complexité) ne pas faire d'autonew ni rien dans ce cas, mais ceci a été fait pour respecter l'énoncé
                
                #Letats : list[State]
                Letats = auto.listStates # on récupère la liste de tous les états de l'automate
                
                ## Opla, on rajoute un état
                #rs : State ## rs pour Rizvan et Sami, pas de siginification particulière, juste un easter egg :p 
                rs = State(len(auto.listStates)+1,False,False,"RS") ## on rajoute un state en plus d'ou le +1 dans le len, "RS" car l'idenitfiant doit etre unique, False/False car ni initial ni final (trivial)
                if(autonew.addState(rs)):  ## On rajoute ce fameux rs
                    # s : State ## Variable courante
                    for s in Letats: ## On parcourt les listes des états de l'automate
                        # c : str ## Varibale courante 
                        for c in alphabet: ## On parcourt les lettres de l'alphabet
                            if(len(auto.succElem(s,c))==0): ## si pas de successeurs alors pas de transition alors ajout d'une transition pour qu'il soit complet
                                autonew.addTransition(Transition(s,c,rs)) # création d'une transition vers le rs
                    # c : str ## Juste rappel :p 
                    for c in alphabet:
                        autonew.addTransition(Transition(rs,c,rs)) # rajout des "loops"/"boucles" pour chaque lettre/etiquette sur le rs (le nouveau state)
                
                return autonew ## ouf ! retournons cet automate :)
                ## Testée - fonctionne bien

        ## Passons à la fonction la plus longue et la plus "dure", rien ne nous arretera, on aura tous les boules de cristal, on attrapera tous les pokémons <3 ## Meilleurs dresseurs
        @staticmethod
        def determinisation(auto) :
                """ Automate  -> Automate
                rend l'automate déterminisé d'auto
                """
                ## Dire qu'un automate est déterministe revient à dire que chaque état a une et une seule transition de la meme étiquette
                ## Donc supprimer les transitions en plus :) Rajouter les transitions manquantes :=) ALORS AUTANT EN CREER UN NOUVEAU
                ## La meilleure facon d'expliquer le raisonnement de cette fonction est de voir le s0 et de dire on a généralisé :) 
                ## Comme d'hab, peut etre qu'il est déterministe, déjà, alors juste retournons le 
                if(Automate.estDeterministe(auto)): # Ah pas de boulot, il est déjà déterministe 
                    return auto
                ## Ok, pas deterministe, on y va :)
                
                ## Commençons par déclarer et initialiser les variables dont on aura besoin :) 
                #listeEtatsInitiales = list[State]
                listeEtatsInitiales = auto.getListInitialStates() ## On prend tous les états Initiales 
                
                #alphabet : list[String]
                alphabet = auto.getAlphabetFromTransitions() ## On prend l'alphabet (celui de estcomplet comme d'hab ;) )
                
                #listeDeTransitions = list[Transition]
                listeDeTransitions = [] ## vide de base
                
                #listeDeStates = list[State]
                listeDeStates = [] ## vide de base 
                
                #listeDeCouplesDeStatesCrees : list[tuple(set[State],Bool,Bool,String] ## Merci la doc :p 
                listeDeCouplesDeStatesCrees = [] ## vide de base 
                
                #ensembleDEtatsInitiales : set[State]
                ensembleDEtatsInitiales = {s for s in listeEtatsInitiales} ## Compréhention d'états pour récupérer fissa les listes d'états initiales # s : State du coup variable courante
                
                ## On s'occupe du premier état 
                #s0isFinal : boolean
                s0isFinal = False ## Initialisation à false, après on verra si c est true :) 
                # s : State ## Variable Courante
                for s in ensembleDEtatsInitiales: ## On parcourt les états initales
                    if(s.fin): ## renvoie True si final et False sinon
                        s0isFinal = True
                
                ## On s'occupe des labels :)
                #labelisteDeStates0 : String ## Avec un grand S parceque c'est un objet :) Merci cours de Java ^^
                labelisteDeStates0 = "{"## On commence par { toujours alors autant le faire :) 
                
                for s in listeEtatsInitiales: ## On parcourt tous les états initiales 
                    if(len(labelisteDeStates0) == len(listeEtatsInitiales)):## On a fini
                        labelisteDeStates0+= s.label + "}" ## On est arrivé à la fin donc on ferme } 
                    else: 
                        labelisteDeStates0 += s.label +"," ## pas encore la fin mais nouveau label, donc virgule pour les séparer, c'est comme ça ^^
                ## Le cptbis nous sert ici pour vérifier (avec un assert) puis on taech à la poubelle :) 
                #on a notre premier état, on l'ajoute à listeDeStates :
                listeDeStates.append(State(0,True,s0isFinal,labelisteDeStates0)) ## s0 donc initial pour sur d ou le True :) 
                listeDeCouplesDeStatesCrees.append(ensembleDEtatsInitiales) ##oppla on les rajoute à la liste c est en fait le s0 en tant qu ensemble qu on rajoute :) 
                
                ## Maintenant ce qu'on a fait pour s0, on va le généraliser pour tout le reste $.$ 
                
                # i : int ## compteur (indique à chaque fois l'indice d'ou on pointe dans la liste des states)
                i = 0
                # E : set 
                for E in listeDeCouplesDeStatesCrees: ## on a notre set dans les couples pour accéder aux couples 
                    i += 1 ## on est au 1er indice la premiere fois et ainsi de suiste
                    # c : char 
                    for c in alphabet:## On parcourt l'alphabet 
                        #listeDeStatesucc = liste des successeurs
                        listeDeStatesucc = [e for e in E] ## liste des successeurs de chacun des states dans E / compréhension de liste pour écrire en une seule ligne 
                        listeDeStatesucc += auto.succ(listeDeStatesucc,c) ## On rajoute le successeur de la lettre
                        if(len(listeDeStatesucc)!= 0 ): ## Liste non vide, cool, on rajoute :)
                            labelisteDeTransitionsemp = "{"  ## On commence par {
                            # final : bool ## etat final ? true apres si c est le cas 
                            final = False ## On initialise à false 
                            # intial : bool ##etat initial ? ture apres si c est le cas 
                            initial = False ## On initialise à false 
                            Pstemp = () ## pseudo état temporaire vu que c est un tuple 
                            Etemp = set() ## ensemble d'états temporaitres 
                            ## On  fait la meme chose faire pour s0 pas besoin de commenter :)
                            for s in listeDeStatesucc:  ## on parcourt tous les états successeurs 
                                if(len(listeDeStatesucc) == len(listeDeStatesucc)):## si on finit le parcours on rajoute }
                                    labelisteDeTransitionsemp += s.label + "}"
                                else:
                                    labelisteDeTransitionsemp += s.label +"," ## sinon comme tout a l heure , pour rajouter en plus 
                                Etemp.add(s) ## on rajoute l etat a la liste temporaire 
                                if(s.fin):## si final alors final 
                                    final = True
                                if(listeDeStatesucc == listeEtatsInitiales): ## si liste des successeur la meme que celle etats initials alors ouais state initial
                                    initial = True
                                Pstemp = Etemp ## Juste pour mieux voir après :) 
                            if(Pstemp not in listeDeCouplesDeStatesCrees): ##unicité 
                                listeDeCouplesDeStatesCrees.append(Pstemp) ## unique donc rajoute 
                                #on crée l'état enfin :) 
                                ## enfin notre state on le rajoute 
                                listeDeStates.append(State(0,initial,final,labelisteDeTransitionsemp)) ##On met 0 à id à chaque fois bon aurait pu mettre un compteur ou utiliser i mais ca sert à rien ^^
                            listeDeTransitions.append(Transition(listeDeStates[i-1],c,listeDeStates[i-1])) ## i-1 car on commence de 0 pour éviter débordement 
                            
                return Automate(listeDeTransitions) ## Constructeur Automate par la liste des transitions uniquement  (listeDeTransition finale)
                ## testée - fonction bien

      	@staticmethod
    	def complementaire (auto,alphabet) :
                """ Automate -> Automate
                rend  l'automate acceptant pour langage le complémentaire du langage de a
                """
                #tempAuto : Automate
                tempAuto = Automate(auto.listTransitions) ##copie de l'automate 
                tempAuto = Automate.completeAutomate(tempAuto,alphabet) ##complétion de l'automate
                tempAuto = Automate.determinisation(tempAuto) ## déterminisation de l'automate
                #s : State 
                for s in tempAuto.listStates:
                    s.fin = not (s.fin) ## ajout des états opposés 
                return tempAuto ## retour de l'automate 
        ## testée - fonctionne bien 

    	@staticmethod
    	def intersection (auto0, auto1):
                """ Automate x Automate -> Automate
                rend l'automate acceptant pour langage l'intersection des langages des deux automates
                """
                if(auto0.listTransitions == auto1.listTransitions):
                    return Automate(auto0.listTransitions)
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

                #alphabet0 : str
                alphabet0 = auto0.getAlphabetFromTransitions()
                #alphabet1 : str
                alphabet1 = auto1.getAlphabetFromTransitions()
                #alphabet : str
                alphabet= alphabet0
                for c in alphabet1:
                    if c not in alphabet0:
                        alphabet+=c
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
                #Liste0_f : list[States]
                Liste0_f=auto0.getListFinalStates()
                #Liste1_f : list[States]
                Liste1_f=auto1.getListFinalStates()
                #Liste_f : list[States]
                Liste_f = Liste0_f
                for l1 in Liste1_f:
                    if l1 not in Liste0_f:
                        Liste_f.append(l1)
                new_States = set()
                for l in Liste:
                    if l[0] in Liste_f and l[1] in Liste_f:
                        test = True
                    new_States.add(State(id ,True ,test ,"("+ str (l[0])+ " ; "+ str (l[1])+ ")") )
                    test = False
                    id += 1
                while(Liste!=[]):
                    s="("+ str (Liste[0][0]) + " ; "+str (Liste[0][1])+")"
                    for l in new_States:
                        if s==l.label:
                            State_temp1=l
                            break
                    for lettre in alphabet:
                        Liste_temp0=auto0.succElem(Liste[0][0],lettre)
                        Liste_temp1=auto1.succElem(Liste[0][1],lettre)
                        for l0 in Liste_temp0: 
                            for l1 in Liste_temp1:
                                if (l0,l1) in Liste_parcourue:
                                    s = "("+str (l0) +" ; "+ str (l1)+")"
                                    for l in new_States:
                                        if s==l.label:
                                            State_temp2=l
                                            Liste_Transition.append(Transition(State_temp1,lettre,State_temp2))
                                            break
                                        else:
                                            if l0 in Liste_f and l1 in Liste_f:   
                                                test=True
                                            Liste_parcourue.append((l0,l1))
                                            s = "("+str (l0) + " ; "+str (l1)+")"
                                            State_temp2=State(id,False,test,s)
                                            id += 1
                                            test = False
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
                ## On prépare la liste des transitions (union de auto0 et auto1) 
                tempAuto = auto0.listTransitions
                tempAuto.extend(auto1.listTransitions)
                ## On crée le nouvel automate 
                tempAuto2 = Automate(tempAuto)
                ## On déterminise ce dernier 
                tempAuto2 = Automate.determinisation(tempAuto2)
                return tempAuto2 

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
                test = False
                for i in Auto1.listStates:
                    i.insertPrefix(1)
                    if i in Liste_F:
                        i.fin = False
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
                    if (t.stateDest).fin: #Si état final
                        Trans.append(t) #On ajoute la transition

                for t in Trans:
                    for i in Auto2.getListInitialStates() :
                        Auto2.addTransition(Transition(t.stateSrc, t.etiquette, i))

                return Auto2 
