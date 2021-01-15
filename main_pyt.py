#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 15:59:48 2020

@author: loulou
"""
#Import
import praw
import urllib.request
import xmltodict
import datetime
from Corpus import *
from Document import *

################################## Création du Corpus ##################################
#Fonction de création d'un corpus pour Reddit
def recuperation_corpus_reddit(sujet):
    #Recupération données pour le corpus reddit
    reddit = praw.Reddit(client_id='kiAjLxNOm7OqhA', client_secret='34s8G410Lzz4ypFXVtzq52Otaa0', user_agent='test')
    documentreddit = reddit.subreddit(sujet).hot(limit=100)
    #Création de notre corpus
    corpusreddit = Corpus("Reddit")
    #Parcour des documents
    for doc in documentreddit:
        datet = datetime.datetime.fromtimestamp(doc.created)
        txt = doc.title + ". "+ doc.selftext
        txt = txt.replace('\n', ' ')
        txt = txt.replace('\r', ' ')   
        #Instanciation d'un objet Document
        doc2 = RedditDocument(datet,
                       doc.title,
                       doc.author,
                       txt,
                       doc.url,
                       doc.num_comments)
        #Ajout des documents
        corpusreddit.add_doc(doc2)
    return(corpusreddit)

#Fonction de création d'un corpus pour arxiv
def recuperation_corpus_arxiv(sujet):
    #Recupération donnée pour le corpus arxiv
    url = 'http://export.arxiv.org/api/query?search_query=all:{}&start=0&max_results=100'.format(sujet)
    data = urllib.request.urlopen(url).read().decode()
    # decode() transforme le 'bytes stream" en chaîne de caractères
    documentarxiv = xmltodict.parse(data)['feed']['entry']
    #Création de notre corpus
    corpusarxiv = Corpus("Arxiv")
     #Parcour des documents
    for i in documentarxiv:
        datet = datetime.datetime.strptime(i['published'], '%Y-%m-%dT%H:%M:%SZ')
        try:
            author = [aut['name'] for aut in i['author']][0]
        except:
            author = i['author']['name']
        try:
            coAuth = [aut['name'] for aut in i['author']][1:]
        except:
            coAuth = "Pas de co-auteur"
        txt = i['title']+ ". " + i['summary']
        txt = txt.replace('\n', ' ')
        txt = txt.replace('\r', ' ')
        #Instanciation d'un objet Document
        doc = ArxivDocument(datet,
                       i['title'],
                       author,
                       txt,
                       i['id'],
                       coAuth,
                       )
        #Ajout des documents
        corpusarxiv.add_doc(doc)
    return(corpusarxiv)