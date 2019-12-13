# -*- coding: utf-8 -*-
from transition import *
from state import *
import os
import copy
from sp import *
from parser import *
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
        """ Automate x str -> bool
        	
			rend True si auto accepte mot, False sinon
        """
        ## Déjà, premier test : chaque lettre du mot doit avoir au moins un état qui le succède pour que le mot soit accepté
        # listeAux : list[State]
        listeAux = auto.getListInitialStates() 
        ## listeAux représente 
        # listeFins : list[State]
        listeFins = []
        # c : char
        for c in mot: 
            # s : State
            for s in listeAux:
                listeFins += auto.succElem(s, c)
                print listeFins
                if (listeFins == []):
                   return False
                ListeAux  = listeFins 
                listeFins = []
                
        ## Si on est là, c'est que le premier test est validé, passons au suivant :)         
        ## ListeAux correspond au dernier listeFins, donc, à la liste complète des états finaux        
        ## Au moins un élement de la liste finale des états successeurs doit être un état final pour que le mot soit accepté
        for s in listeAux:
            if(s in auto.getListFinalStates()):
                return True 
                
        return False
        
    @staticmethod
    def estComplet(auto,alphabet) :
        """ Automate x str -> bool
         
			rend True si auto est complet pour alphabet, False sinon
        """
        return 


        
    @staticmethod
    def estDeterministe(auto) :
        """ Automate  -> bool
        
			rend True si auto est déterministe, False sinon
        """
        return
        

       
    @staticmethod
    def completeAutomate(auto,alphabet) :
        """ Automate x str -> Automate
        
			rend l'automate complété d'auto, par rapport à alphabet
        """
        return

       

    @staticmethod
    def determinisation(auto) :
        """ Automate  -> Automate
        
			rend l'automate déterminisé d'auto
        """
        return
        
    @staticmethod
    def complementaire(auto,alphabet):
        """ Automate -> Automate
        
			rend  l'automate acceptant pour langage le complémentaire du langage de a
        """
              
   
    @staticmethod
    def intersection (auto0, auto1):
        """ Automate x Automate -> Automate
        
			rend l'automate acceptant pour langage l'intersection des langages des deux automates
        """
        return

    @staticmethod
    def union (auto0, auto1):
        """ Automate x Automate -> Automate
        
			rend l'automate acceptant pour langage l'union des langages des deux automates
        """
        return
        

   
       

    @staticmethod
    def concatenation (auto1, auto2):
        """ Automate x Automate -> Automate
        	
			rend l'automate acceptant pour langage la concaténation des langages des deux automates
        """
        return
        
       
    @staticmethod
    def etoile (auto):
        """ Automate  -> Automate
        
			rend l'automate acceptant pour langage l'étoile du langage de a
        """
        return