#IMPORT des librairies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier

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
    genre = input("Action, Adventure, Animation, Children's, Comedy, Crime, \n Documentary, Drama, Fantasy, Film-Noir, Horror, Musical, Mystery, Romance, Sci-Fi, Thriller, War, Western ? ")
    
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
    # réglagle des sorties graphiques
    font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 16}

    plt.rc('font', **font)
    
    plt.figure(figsize = (20, 8))
    plt.subplot(1,2,1)
    sns.boxplot(y = res['rating'], showmeans=True)
    plt.title(f'Répartition des notes pour le genre : {genre}')

    # répartition des notes:
    plt.subplot(1,2,2)
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
        listeFilm.append(x.strip())

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
print("Les films que vous aimez sont :\n", np.unique(result['title']))
print()

# TODO les stats sur ces films


#on appelle la fonction des stats par genre
askMeGenre()

#MODELE de RECOMMANDATION "Item-Item Collaborative Filtering"
#On implémente un modèle kNN

"""Définition de la base de données des films aimés"""
dfAime=df[df["rating"]>4].groupby(["movieId","title", "genres", "imdbId", "tmdbId"]).mean()
dfAime.reset_index(inplace=True)


"""Définition des variables"""
X2=dfAime.loc[:,np.append(df["genres"].str.split('|',expand=True)[0].unique(),["rating"])]
y2=dfAime.loc[:, "movieId"]

"""Défition des bases d'entrainement et de test. Toutefois, vu le type de modèle, on n'as pas vraiment besoin de faire un test.
Du coup, on implémente le modèle sur toute la base de données"""
#X_train2, X_test2, y_train2, y_test2 =train_test_split(X2, y2, random_state=42, train_size = 0.80)


"""Initialisation du modèle"""
modelClassification2 = KNeighborsClassifier(n_neighbors=1)
modelClassification2.fit(X2, y2)

"""On test le modèle avec une liste de films tirés au hasard"""

films=listeFilmLue

# TODO : à partir de la liste des films, faire les recommandations
for idFilm in films:
  print(idFilm)
  recommandation2=modelClassification2.kneighbors(df.loc[df["movieId"]==idFilm, np.append(df["genres"].str.split('|',expand=True)[0].unique(),["rating"])], n_neighbors=1, return_distance=False)
  print("Si vous avez aimé le film ", df[df["movieId"]==idFilm]["title"].values[0], ", les 5 films suivants pourraient vous intéresser: \n")
  for item in np.nditer(recommandation2):
    print(dfAime[dfAime.index==item][["title", "genres"]].values[0])
  print()
