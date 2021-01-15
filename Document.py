# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 15:22:47 2021

@author: Remy
"""
#Classe document
class Document:
    
    #Fonction d'initialisation
    def __init__(self, date, title, author, text, url):
        self.date = date
        self.title = title
        self.author = author
        self.text = text
        self.url = url
    
    #getters
    def get_author(self):
        return self.author

    def get_title(self):
        return self.title
    
    def get_date(self):
        return self.date
    
    def get_source(self):
        return self.source
        
    def get_text(self):
        return self.text
    
    #Renvoie du type du document et de son titre
    def __str__(self):
        return "Document " + self.getType() + " : " + self.title
    
    def __repr__(self):
        return self.title
    
#
# Classe fille permettant de modéliser un Document Reddit
#
  
class RedditDocument(Document):
    
    #Fonction d'initialisation
    def __init__(self, date, title,
                 author, text, url, num_comments):        
        Document.__init__(self, date, title, author, text, url)
        # ou : super(...)
        self.num_comments = num_comments
        self.source = "Reddit"
    
    #getters
    def get_num_comments(self):
        return self.num_comments

    def getType(self):
        return "reddit"
    
    def __str__(self):
        return Document.__str__(self) + " [" + str(self.num_comments) + " commentaires]"
    
#
# Classe fille permettant de modéliser un Document Arxiv
#

class ArxivDocument(Document):
    
    #Fonction d'initialisation
    def __init__(self, date, title, author, text, url, coauteurs):
        #datet = dt.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
        Document.__init__(self, date, title, author, text, url)
        self.coauteurs = coauteurs
        
    #getters
    def get_num_coauteurs(self):
        if self.coauteurs is None:
            return(0)
        return(len(self.coauteurs) - 1)

    def get_coauteurs(self):
        if self.coauteurs is None:
            return([])
        return(self.coauteurs)
        
    def getType(self):
        return "arxiv"
    
    def __str__(self):
        s = Document.__str__(self)
        if self.get_num_coauteurs() > 0:
            return s + " [" + str(self.get_num_coauteurs()) + " co-auteurs]"
        return s