# -*- coding: utf-8 -*-
"""
Created on Wed May  6 17:13:09 2020

@author: elo
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# fonction qui lit un fichier texte
def lectureTxt(name = 'listeFilm.txt'):
    '''fonction qui lit un fichier texte et renvoit une liste des éléments lus'''
    f = open(name, 'r', encoding = "utf8")
    listeFilm = []
    content = f.readlines()
    for x in content:
        listeFilm.append (x.strip())

    return(listeFilm)
    f.close() # nécessaire ?
    

# creation d'un dataframe test
df = pd.DataFrame({'idFilms' : ['1985','1520','12','547'], 
                   'titre' : ['Un bon film', 'un mauvais film', 'un film', 'un court métrage']}, 
                   index = [0,1,2,3])

#print(df.head())

#on appelle la fonction qui lit le fichier texte :
listeFilmLue = lectureTxt("listeFilm.txt")

#rechercher si correspondance entre listeFilmLue et base (df ici) et afficher le titre du film en commun.
result = df[df['idFilms'].isin(listeFilmLue)]
print(result['titre'])
