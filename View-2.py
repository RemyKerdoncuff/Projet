#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 00:16:59 2021

@author: loulou
"""
import tkinter 
import sys
#Import
from main_pyt import *

#Police et taille
LARGE_FONT= ("Arial", 15)
title_font = ("Arial", 35, 'bold')

#Fenêtre affichant le chargement de l'analyse
class SplashAnalyse(tkinter.Toplevel):
    def __init__(self, parent):
        tkinter.Toplevel.__init__(self, parent)
        
        #Label du titre dans la fenêtre
        txt = tkinter.Label(self, text="Nous etudions les mot-clés ...", font=LARGE_FONT)
        txt.pack(pady=10,padx=10)

        self.update()

#Fenêtre affichant une erreur de keyword
class SplashError(tkinter.Toplevel):
    def __init__(self, parent):
        tkinter.Toplevel.__init__(self, parent)
        #Label du titre dans la fenêtre
        txt = tkinter.Label(self, text="Ce mot clé n'est pas dans le corpus", font=LARGE_FONT)
        txt.pack(pady=10,padx=10)
        
        #Boutons
        button = tkinter.Button(self, text="OK", relief = tkinter.GROOVE, command=self.destroy)
        button.pack(pady = 5)
        
        self.update()

#Fonction d'analyse
def CORPUS_creation(self, entryKeyword, txt):        
    try:
        #variable global afin de pouvoir garder en memoire la valeur et de pouvoir les utiliser dans les auutres pages
        global corpusreddit
        global corpusarxiv
        corpusreddit = 0
        corpusarxiv = 0
        
        splash = SplashAnalyse(self)
        #on recupere le mot cle passé en parametre
        motcle = entryKeyword.get().upper()
        
        #creation de nos 2 corpus a partir du mot cle 
        try:
            corpusreddit=recuperation_corpus_reddit(motcle)
            corpusarxiv=recuperation_corpus_arxiv(motcle)
        except IndexError as error:
            splash.destroy()
            splash = SplashError(self)
        print(motcle)
        
        txt.delete(1.0,tkinter.END)
        
        #on affiche le nombre de docment ainsi que le nombre d'auteur présent dans chaque corpus dans un widget texte
        #Config mot coupés
        txt.config(wrap=tkinter.WORD)
        print("Création du corpus reddit, %d documents et %d auteurs\n" % (corpusreddit.ndoc,corpusreddit.naut))
        txt.insert(tkinter.END, "Création du corpus reddit, %d documents et %d auteurs\n" % (corpusreddit.ndoc,corpusreddit.naut) , 'normal')
        txt.insert(tkinter.END, "Création du corpus arxiv, %d documents et %d auteurs\n" % (corpusarxiv.ndoc,corpusarxiv.naut) , 'normal')
        
        #for i in range(corpusreddit.ndoc):
        #    txt.insert(tkinter.END, corpusreddit.get_doc(i).get_text() + '\n', 'normal')

        txt.pack()
        #Destruction à la fin de l'analyse
        splash.destroy()
        #Exception si le keyword est introuvable   
    except IndexError as error:
        splash.destroy()
        splash = SplashError(self)
 
    
def RechercheMotCle(self, entryKeyword, txt):
    try:
        
        splash = SplashAnalyse(self)
        motcle = entryKeyword.get().upper()
        #Config mot coupés
        txt.config(wrap=tkinter.WORD)
        
        #on recupere grace à search differentes informations :  un tableau du titre de chaque document, un tableau avec les phrases et un tableau avec le nom des corpus
        a,b,c = corpusreddit.search(motcle)
        d,e,f = corpusarxiv.search(motcle)
        
        ad = a + d
        be = b + e
        cf = c + f
        
        
        #on affiche les informations récupérés avec search dans un widget texte
        txt.delete(1.0,tkinter.END)
        for i in range(0,len(ad)):
            txt.insert(tkinter.END, "TITRE : " + ad[i], 'normal')
            txt.insert(tkinter.END, "--- PHRASE  : " + be[i], 'normal')
            txt.insert(tkinter.END, "--- CORPUS  : " + cf[i] + "\n", 'normal')


        txt.pack()
        #Destruction à la fin de l'analyse
        splash.destroy()
        
        #Exception si le keyword est introuvable   
    except IndexError as error:
        splash.destroy()
        splash = SplashError(self)
 
    
def ComparaisonCorpus(self, entryKeyword1, entryKeyword2,  entryKeyword3, entryKeyword4,txt):
    try:

        splash = SplashAnalyse(self)

        txt.config(wrap=tkinter.WORD)

        txt.delete(1.0,tkinter.END)
        
        #on crée nos 3 tableaux, tab qui va permettre de naviguer entre les mots passés en paramètre, tab_mot_cle et tab_mot_cle2 qui permettent de récupéré le mot en fonction du corpus
        tab = []
        tab_mot_cle = []
        tab_mot_cle2 = []

        tab.append(entryKeyword1)
        tab.append(entryKeyword2)
        tab.append(entryKeyword3)
        tab.append(entryKeyword4)

        #on test si nos mots sont présents dans un des deux corpus
        for element in tab:
            if (corpusreddit.nb_doc_apparition_mot_cle(element.get())) != 0:
                tab_mot_cle.append(element.get())
            if (corpusarxiv.nb_doc_apparition_mot_cle(element.get())) != 0:
                tab_mot_cle2.append(element.get())

        #on calcul le TF_IDF de chaque mot clé pour les 2 corpus
        cal = corpusreddit.calculTF_IDF(tab_mot_cle)
        cal2 = corpusarxiv.calculTF_IDF(tab_mot_cle2)
        maxx = max(len(cal),len(cal2))
        #on affiche les fréquences issues du calcul avec les mots afin de pouvoir comparer visiuellement
        for i in range(maxx):
            txt.insert(tkinter.END, "MOT : " + tab[i].get() + "\n", 'normal')
            if tab[i].get() in cal :
                txt.insert(tkinter.END, "TF_IDF corpus Reddit : " + str(cal[tab_mot_cle[i]]) + "\n", 'normal')
            else:
                txt.insert(tkinter.END, "TF_IDF corpus Reddit : 0\n", 'normal')
            if tab[i].get() in cal2 :
                txt.insert(tkinter.END, "TF_IDF corpus Arxiv : " + str(cal2[tab_mot_cle2[i]]) + "\n" , 'normal')
            else:
                txt.insert(tkinter.END, "TF_IDF corpus Arxiv : 0\n", 'normal')
                
            txt.insert(tkinter.END, "\n")
        
        
        
        txt.pack()
        #Destruction à la fin de l'analyse
        splash.destroy()

        #Exception si le keyword est introuvable
    except IndexError as error:
        splash.destroy()
        splash = SplashError(self)

#Classe principale
class InterfaceGraphique(tkinter.Tk):

    def __init__(self, *args, **kwargs):
        
        tkinter.Tk.__init__(self, *args, **kwargs)
        container = tkinter.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.title("Projet Python Master, Louis & Remy")
        self.geometry("800x800")

        self.frames = {}

        for F in (PageChoixDuSujet, PageMenu, PageRechercheMotCle, PageEvolutionTemporelle, PageComparaisonDesCorpus):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PageMenu)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()



        
#Page menu
class PageMenu(tkinter.Frame):

    def __init__(self, parent, controller):
        #Init
        tkinter.Frame.__init__(self, parent)
        
        #Label du titre dans la fenêtre
        titreMenu = tkinter.Label(self, text="MENU", font=title_font)
        titreMenu.pack(pady=10,padx=10)

        #Boutons
        buttonM1 = tkinter.Button(self, text="Choix du sujet", relief = tkinter.GROOVE, command=lambda: controller.show_frame(PageChoixDuSujet))
        buttonM1.pack(pady = 5)

        buttonM2 = tkinter.Button(self, text="Recherche du mot Cle", relief = tkinter.GROOVE, command=lambda: controller.show_frame(PageRechercheMotCle))
        buttonM2.pack(pady = 5)

        buttonM3 = tkinter.Button(self, text="Comparaison des corpus", relief = tkinter.GROOVE, command=lambda: controller.show_frame(PageComparaisonDesCorpus))
        buttonM3.pack(pady = 5)
        
        buttonM4 = tkinter.Button(self, text="Evolution Temporelle du mot cle", relief = tkinter.GROOVE, command=lambda: controller.show_frame(PageEvolutionTemporelle))
        buttonM4.pack(pady = 5)
        
        buttonM5 = tkinter.Button(self,text ="Quitter l'application", relief = tkinter.GROOVE, command=sys.exit)
        buttonM5.pack(pady = 5)
        
        
        
class PageChoixDuSujet(tkinter.Frame):

    def __init__(self, parent, controller):
        #Init
        tkinter.Frame.__init__(self,parent)
        
        #Label du titre dans la fenêtre
        titreMenu = tkinter.Label(self, text="Choix du sujet", font=title_font)
        titreMenu.pack(pady=10,padx=10)
        
        #Label du titre dans la fenêtre
        txtexpli = tkinter.Label(self, text = "Entrez un nom de sujet pour lancer la génération des corpus\n", font = LARGE_FONT)
        txtexpli.pack(pady = 5)
        
        #Zone de texte
        txt = tkinter.Text(self, height=50, width=100)
        #Config polices, etc.
        txt.tag_configure('normal', font=('Arial', 16), justify='left')
        
        
        #Champ de saisie
        champKeyword = tkinter.StringVar()
        entryKeyword = tkinter.Entry(self, textvariable = champKeyword, width = 10)
        entryKeyword.pack(pady = 5)
    
        #Boutons
        boutonValidation = tkinter.Button(self, text = "Analyser", relief = tkinter.GROOVE, command = lambda: CORPUS_creation(self, entryKeyword, txt))
        boutonValidation.pack(pady = 5)
        
        buttonMenu = tkinter.Button(self, text="MENU", relief = tkinter.GROOVE, command=lambda: controller.show_frame(PageMenu))
        buttonMenu.pack(pady = 5)


class PageRechercheMotCle(tkinter.Frame):

    def __init__(self, parent, controller):
        #Init
        tkinter.Frame.__init__(self,parent)
        
        #Label du titre dans la fenêtre
        titreMenu = tkinter.Label(self, text="Recherche du mot cle", font=title_font)
        titreMenu.pack(pady=10,padx=10)
        
        #Label du titre dans la fenêtre
        txtexpli = tkinter.Label(self, text = "Entrez un mot cle\n", font = LARGE_FONT)
        txtexpli.pack(pady = 5)
        
        #Zone de texte
        txt = tkinter.Text(self, height=50, width=100)
        #Config polices, etc.
        txt.tag_configure('normal', font=('Arial', 16), justify='left')
        
        #Champ de saisie
        champKeyword = tkinter.StringVar()
        entryKeyword = tkinter.Entry(self, textvariable = champKeyword, width = 10)
        entryKeyword.pack(pady = 5)
    
        #Boutons
        boutonValidation = tkinter.Button(self, text = "Lancer la recherche", relief = tkinter.GROOVE, command = lambda: RechercheMotCle(self, entryKeyword, txt))
        boutonValidation.pack(pady = 5)
        
        buttonMenu = tkinter.Button(self, text="MENU", relief = tkinter.GROOVE, command=lambda: controller.show_frame(PageMenu))
        buttonMenu.pack(pady = 5)
  
    
#Page autre métohde de prédiction
class PageEvolutionTemporelle(tkinter.Frame):

    def __init__(self, parent, controller):
        #Init
        tkinter.Frame.__init__(self, parent)
        
        #Label du titre dans la fenêtre
        titreMethode = tkinter.Label(self, text="Evolution temporelle d'un mot cle", font=title_font)
        titreMethode.pack(pady=10,padx=10)
        
        #Champ de saisie
        champKeyword = tkinter.StringVar()
        entryKeyword = tkinter.Entry(self, textvariable = champKeyword, width = 10)
        entryKeyword.pack(pady = 5)
        
        #Boutons
        boutonValidation = tkinter.Button(self, text = "Analyser", relief = tkinter.GROOVE)
        boutonValidation.pack(pady = 5)

        buttonMenu = tkinter.Button(self, text="MENU", relief = tkinter.GROOVE, command=lambda: controller.show_frame(PageMenu))
        buttonMenu.pack(pady = 5)

        
          
class PageComparaisonDesCorpus(tkinter.Frame):

    def __init__(self, parent, controller):
        #Init
        tkinter.Frame.__init__(self,parent)
        
        #Label du titre dans la fenêtre
        titreMenu = tkinter.Label(self, text="Comparaison des fréquences\n", font=title_font) #(Par défaut du nom du sujet du corpus, sinon en fonction d'un mot cle)
        titreMenu.pack(pady=10,padx=10)
        
        #input mot cle optionnel 1
        txtMco1 = tkinter.Label(self, text = "Ajout mot cle optionnel 1\n", font = LARGE_FONT)
        txtMco1.pack(pady = 5)
        #Champ de saisie
        champKeyword1 = tkinter.StringVar()
        entryKeyword1 = tkinter.Entry(self, textvariable = champKeyword1, width = 10)
        entryKeyword1.pack(pady = 5)
        
        #input mot cle optionnel 2
        txtMco2 = tkinter.Label(self, text = "Ajout mot cle optionnel 2\n", font = LARGE_FONT)
        txtMco2.pack(pady = 5)
        #Champ de saisie
        champKeyword2 = tkinter.StringVar()
        entryKeyword2 = tkinter.Entry(self, textvariable = champKeyword2, width = 10)
        entryKeyword2.pack(pady = 5)
        
        #input mot cle optionnel 3
        txtMco3 = tkinter.Label(self, text = "Ajout mot cle optionnel 3\n", font = LARGE_FONT)
        txtMco3.pack(pady = 5)
        #Champ de saisie
        champKeyword3 = tkinter.StringVar()
        entryKeyword3 = tkinter.Entry(self, textvariable = champKeyword3, width = 10)
        entryKeyword3.pack(pady = 5)
        
        #input mot cle optionnel 4
        txtMco4 = tkinter.Label(self, text = "Ajout mot cle optionnel 4\n", font = LARGE_FONT)
        txtMco4.pack(pady = 5)
        #Champ de saisie
        champKeyword4 = tkinter.StringVar()
        entryKeyword4 = tkinter.Entry(self, textvariable = champKeyword4, width = 10)
        entryKeyword4.pack(pady = 5)
        
        #Zone de texte
        txt = tkinter.Text(self, height=50, width=100)
        #Config polices, etc.
        txt.tag_configure('normal', font=('Arial', 16), justify='left')
        
        #Boutons
        boutonValidation = tkinter.Button(self, text = "Lancer la comparaison", relief = tkinter.GROOVE, command=lambda: ComparaisonCorpus(self,entryKeyword1,entryKeyword2,entryKeyword3,entryKeyword4,txt))
        boutonValidation.pack(pady = 5)
        
        buttonMenu = tkinter.Button(self, text="MENU", relief = tkinter.GROOVE, command=lambda: controller.show_frame(PageMenu))
        buttonMenu.pack(pady = 5) 
        
#Main
app = InterfaceGraphique()
app.mainloop()