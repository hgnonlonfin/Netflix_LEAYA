#IMPORT des librairies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#DEFINITION DES FONCTIONS

#Définition genreDummies pour créer des variables binaires pour le genre de films
def genresDummies(DataFrame):
  '''création d'une colonne pour chaque genre de films et codage binaire'''
  tmp=DataFrame["genres"].str.split('|',expand=True)
  for element in tmp[0].unique():
    DataFrame[element]=0
    DataFrame.loc[DataFrame["genres"].str.contains(element), element] = 1

def askMeGenre(dataframe = df) :
    '''fonction qui demande un genre de film à l'utilisateur et retourne les statistiques principales de ce genre de film dans la bdd'''
    print("Hello ! Quel genre de film aimez-vous ?")
    genre = input("Action, Adventure, Animation, Children's, Comedy, Crime, \n Documentary, Drama, Fantasy, Film-Noir, Horror, Musical, Mystery, Romance, Sci-Fi, Thriller, War, Western ?")
    
    # calculs sur le df total :
    NbFilmsTotaux = len(np.unique(df.movieId))
    MOY = df.groupby('movieId').mean()['rating'].mean() 
    
    # subset de dataframe correspondant au genre :
    res = df[df[genre] == 1]
    # calculer les stats descriptives pour ce genre et les afficher
    # on regroupe les avis par film en utilisant movieId:
    df_grouped = res.groupby('movieId')

    # nombre de films de ce genre : 
    nbFilm = len(df_grouped)
    print(f'Il y a {nbFilm} films répértoriés pour le genre {genre}')
    if nbFilm > NbFilmsTotaux/ 5 :
        print('Il y a du choix dans cette catégorie !!')
    
    # nombre de films | % / films totaux 
    print(f'Cela représente {round(nbFilm / NbFilmsTotaux  * 100, 1)} % des films totaux')
    # moyenne des films de ce genre :
    df_grouped.mean()['rating'].sort_values(ascending = False)
    MoyParGenre = df_grouped.mean()['rating'].mean()
    print(f'En moyenne ces films sont notés {round(MoyParGenre,1)} / 5 étoiles (la moyenne pour tous les films est {round(MOY,1)})')
    
    # boxplot montrant la distribution des films de cette catégorie
    plt.figure()
    sns.boxplot(y = res['rating'], showmeans=True)
    plt.title(f'Répartition des notes pour le genre : {genre}')
    nomfig = genre + 'png'
    plt.show()
    
    # répartition des notes:
    sns.distplot(res['rating'], kde = False)
    plt.title(f'Voici la distribution des notes pour le genre {genre}')
    plt.show()

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
    

#IMPORTATION DES BASES DE DONNEES
links = pd.read_csv('https://raw.githubusercontent.com/hgnonlonfin/Netflix_LEAYA/master/links.csv')
movies = pd.read_csv('https://raw.githubusercontent.com/hgnonlonfin/Netflix_LEAYA/master/movies.csv')
ratings = pd.read_csv('https://raw.githubusercontent.com/hgnonlonfin/Netflix_LEAYA/master/ratings.csv')
tags = pd.read_csv('https://raw.githubusercontent.com/hgnonlonfin/Netflix_LEAYA/master/tags.csv')

#Fusion des bases movies et links
moviesLinks=movies.merge(links, on="movieId", how="inner")


#Fusion des informations sur les movies et les users
df=ratings.merge(moviesLinks, on="movieId", how="inner")

#Application de la fonction genresDummies pour transformer la colonne genre en n * genres remplis de 0 ou 1
genresDummies(df)

# drop des colonnes qui ne nous intéressent pas : timestamp_x  et y
df = df.drop(columns = ['timestamp'])



#on appelle la fonction qui lit le fichier texte :
listeFilmLue = lectureTxt("listeFilm.txt")

#rechercher si correspondance entre listeFilmLue et base (df ici) et afficher le titre du film en commun.
result = df[df['movieId'].isin(listeFilmLue)]
print(result['title'])
    
