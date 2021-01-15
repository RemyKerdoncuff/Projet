# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 15:34:09 2021

@author: Remy
"""
#Classe Author qui n'est actuellement pas utilisé
class Author():
    
    #Fonction d'initialisation d'une instance
    def __init__(self,name):
        self.name = name
        self.production = {}
        self.ndoc = 0
        
    #Fonction d'ajout
    def add(self, doc):     
        self.production[self.ndoc] = doc
        self.ndoc += 1
        
    #Fonction de renvoie du nom de l'auteur et de son nombre de documents écrit
    def __str__(self):
        return "Auteur: " + self.name + ", Number of docs: "+ str(self.ndoc)
    
    #Fonction de renvoie du nom de l'auteur
    def __repr__(self):
        return self.name