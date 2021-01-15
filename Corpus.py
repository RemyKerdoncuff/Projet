# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 15:33:42 2021

@author: Remy
"""
import pickle
import re
from Author import Author
import math

#Classe Corpus
class Corpus():
    
    #Fonction d'initialisation
    def __init__(self,name):
        self.name = name
        self.collection = {}
        self.authors = {}
        self.id2doc = {}
        self.id2aut = {}
        self.ndoc = 0
        self.naut = 0
        #String contenant la chaine avec tous les documents du corpus pour éviter que la fonction de création du string soit re-appellé
        self.string = ""
        
    #Fonction d'ajout de document au corpus
    def add_doc(self, doc):
        #On ajoute le document au corpus à la seule condition qu'il soit vérifié par la fonction verification
        if(self.verification(doc)==True):
            self.collection[self.ndoc] = doc
            self.id2doc[self.ndoc] = doc.get_title()
            self.ndoc += 1
            aut_name = doc.get_author()
            aut = self.get_aut2id(aut_name)
            if aut is not None:
                self.authors[aut].add(doc)
            else:
                self.add_aut(aut_name,doc)
                
    #Fonction d'ajout des auteurs : non utilisé, mais qui explique la création d'une classe Author
    def add_aut(self, aut_name,doc):
        aut_temp = Author(aut_name)
        aut_temp.add(doc)
        self.authors[self.naut] = aut_temp
        self.id2aut[self.naut] = aut_name
        self.naut += 1

    #Fonction d'ajout des coauteurs
    def get_aut2id(self, author_name):
        aut2id = {v: k for k, v in self.id2aut.items()}
        heidi = aut2id.get(author_name)
        return heidi
    
    #getters
    def get_doc(self, i):
        return self.collection[i]
    
    def get_coll(self):
        return self.collection


    #Création de l'attribut string
    def get_string(self):
        tablestring=[]
        for i in range(self.ndoc):
            txt = self.get_doc(i).get_title() + ". "+ self.get_doc(i).get_text()
            txt = txt.replace('\n', ' ')
            tablestring.append(txt)
        str=""
        #On ajoute tous ces elements en minuscule à notre variable string
        self.string=str.join(tablestring).lower()
        #print(self.string)
    
    
    #Vérification de la taille de l'article
    def verification(self, doc):
        if len(doc.get_text())>100:
            return True
        return False
    
    #Vérification de la présence d'un mot et renvoie des phrases dans lesquelles il est contenu ainsi que son titre et son corpus
    def search(self, mot_cle):
        #
        table_title=[]
        table_sentence=[]
        table_corpus=[]
        #Parcours des documents
        for i in range(self.ndoc):
            titre = self.get_doc(i).get_title()
            #Parcours des phrase du document i
            for sentence in self.get_doc(i).get_text().split('. ' or ', '):
                if mot_cle.lower() in sentence:
                    table_title.append(titre)
                    table_sentence.append(sentence)
                    #Voila donc pourquoi on utile l'héritage dans document
                    table_corpus.append(self.get_doc(i).getType())
        return table_title,table_sentence,table_corpus
        
        
    #Compte le nombre de fois ou le mot_clé est utilisé dans notre string
    def get_number_motcle(self, mot_cle):
        if(self.string==""):
            self.get_string()
        resultat = re.findall(mot_cle, self.string)
        return len(resultat)
    
    #Compte le nombre de mots de chaque textes et titres
    def compte_mots(self):
        if(self.string==""):
            self.get_string()
        return len(self.string.split())
    
    #Compte le nombre de documents contenant le mot-clé
    def nb_doc_apparition_mot_cle(self,mot_cle):
        index=0
        for i in range(self.ndoc):
            txt = self.get_doc(i).get_title() + ". "+ self.get_doc(i).get_text()
            if len(re.findall(mot_cle,txt))!=0:
                index+=1
        return index
    
    #Cette fonction aurait pu avoir un interêt dans la partie evolution temporelle
    #Compte le nombre de mots clé pour chaque documents et renvoie ce nombre et la date
    def nb_mot_par_doc(self,mot_cle):
        date=[]
        number=[]
        for i in range(self.ndoc):
            txt = self.get_doc(i).get_title() + ". "+ self.get_doc(i).get_text()
            if len(re.findall(mot_cle,txt))!=0:
                number.append(len(re.findall(mot_cle,txt)))
                date.append(self.get_doc(i).get_date())
        return(number,date)
    
    #On prend un paramètre un tableau de mot clé et on revoie un dictionnaire contenant ces éléments en index et leur fréquence
    def calculTF_IDF(self,tab_mot_cle):
        values={}
        #Vérification que le tableau n'est pas vide
        if(not tab_mot_cle):
            result_tf = self.get_number_motcle(self.name) / self.compte_mots()
            result_IDF = math.log(self.ndoc/(self.nb_doc_apparition_mot_cle(self.name)))
            values[tab_mot_cle] = result_tf*result_IDF
        else:
            for element in tab_mot_cle:
                result_tf = self.get_number_motcle(element) / self.compte_mots()
                result_IDF = math.log(self.ndoc/(self.nb_doc_apparition_mot_cle(element)))
                values[element] = result_tf*result_IDF
        return (values)
