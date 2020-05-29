#STATISTIQUES DESCRIPTIVES de la base df du projet NETFLIX LEAYA

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from outil import *

# lire les données
#Etape 0: Importation des bases
links = pd.read_csv('https://raw.githubusercontent.com/hgnonlonfin/Netflix_LEAYA/master/links.csv')
movies = pd.read_csv('https://raw.githubusercontent.com/hgnonlonfin/Netflix_LEAYA/master/movies.csv')
ratings = pd.read_csv('https://raw.githubusercontent.com/hgnonlonfin/Netflix_LEAYA/master/ratings.csv')
tags = pd.read_csv('https://raw.githubusercontent.com/hgnonlonfin/Netflix_LEAYA/master/tags.csv')

#Etape 1: Fusion des bases 
  #1a Fusion des bases movies et links
moviesLinks=movies.merge(links, on="movieId", how="inner")

  #1b Fusion des informations sur les movies et les users
df=ratings.merge(moviesLinks, on="movieId", how="inner")

  #1c Application de la fonction genresDummies pour transformer la colonne genre en n * genres remplis de 0 ou 1
genresDummies(df)   
df = df.drop(columns = ['timestamp']) # drop des colonnes qui ne nous int�ressent pas : timestamp_x  et y

# ajout d'une colonne Link_movies avec formattage des lien imbd (7 chiffres)
moviesLinks['Link_movies'] = ('https://www.imdb.com/title/tt') + moviesLinks['imdbId'].astype(str).apply(lambda x: x.zfill(7))

#REGLAGES FENETRE GRAPHIQUE
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 16}

plt.rc('font', **font)

df.head()
df.info()

# NOMBRE DE FILMS 
# par titre :
res = np.unique(df['title'], return_counts = True)
len(res[0]) #9719
NbNotesParFilm = pd.DataFrame({'titre' : res[0], 'nombre' : res[1]})
print(NbNotesParFilm)
NbNotesParFilm.mean(axis = 0) # En moyenne les films ont été noté 10,4 fois
NbNotesParFilm.median(axis = 0) # la médiane est de 3

# par movieId
res = np.unique(df['movieId'], return_counts = True)
len(res[0]) #9724
NbNotesParFilm = pd.DataFrame({'ID' : res[0], 'nombre' : res[1]})
print(NbNotesParFilm)
NbNotesParFilm.mean(axis = 0) # En moyenne les films ont été noté 10,4 fois
NbNotesParFilm.median(axis = 0) # la médiane est de 3

# retrouver le résultat différemment :
df.groupby('movieId').count().median()
df.groupby('movieId').count().mean()

#VISUALISATION
plt.figure(figsize = (10,8))
sns.distplot(NbNotesParFilm['nombre'], kde = False, bins = 200, color = '#006600')
plt.title('Distribution du nombre de notes par film')
plt.xlim(0,30,1)

plt.savefig('DistributionNotes.png')



np.unique(df['movieId']).shape #9724

# les lignes vides => colonne tmbdId
df1 = df[df.isna().any(axis=1)] 
print(df1)
# selon que l'on groupe par movieId ou par title, le nombre de films dans la base est différent 
# existe-t-il des duplicats ?
unique = df.groupby(['title', 'movieId']).count()
unique.head()
unique.reset_index(inplace = True)
unique[unique['title'].duplicated()] #5 films sont en double avec des movieId différents mais des titres identiques
unique[unique['movieId'].duplicated()]

listeFilmsEnDouble = list(unique[unique['title'].duplicated()]['title'].values[:])
print(df[df['title'].isin(listeFilmsEnDouble)][['title', 'movieId']])

# pour chaque film, le nombre de titre : 
pd.pivot_table(data = df, index = 'movieId', values = 'title', aggfunc = 'count')

#export de la liste des movieID et title films en csv
listeFilm = pd.pivot_table(data = df, index = ['movieId', 'title'], values = 'rating', aggfunc = 'count')
listeFilm.to_csv('liste_films.csv')

  
  
# NOMBRE DE NOTES PAR FILM :
nbNotesParFilm = pd.pivot_table(data = df, index = 'movieId', values = 'userId', aggfunc = 'count')
df[df['movieId'] == 193581] # certains films ne sont notés qu'une seule fois 

val = df.groupby('movieId').count().sort_values(by = 'userId', ascending = False)
df[df['movieId'] == 356] # le film le plus noté est le 356 : 329 fois : Forrest Gump (1994)
df[df['movieId'] == 318]# le film le 2ème plus noté est le 318 : 317 fois : Shawshank Redemption, The (1994) 
df[df['movieId'] == 296]# le film le 3ème plus noté est le 296 : 307 fois : Pulp Fiction (1994)
val.nlargest(5, 'userId')


# NOTE MOYENNE De TOUS LES FILMS
MOY = df.groupby('movieId').mean()['rating'].mean() # 3.3
MEDIAN = df.groupby('movieId').median()['rating'].median()  # 3.5


# NOTE MOYENNE PAR FILM
moyParFilm = df.groupby('movieId').mean()
moyParFilm.shape #9724

# nombre de film avec une moyenne de 5 ?
moyParFilm[moyParFilm['rating'] == 5].count() #296

#VISUALISATION
plt.hist(moyParFilm['rating'])
plt.title('Histogramme montrant la \n répartition du rating moyen des films')
plt.get_yticks()
plt.savefig('hist_repartition des notes.png')
