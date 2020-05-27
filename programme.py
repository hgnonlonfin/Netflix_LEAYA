#IMPORT des librairies
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from outil import *
   

if __name__ == '__main__':
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
    #TODO passer en int ?
    #rechercher si correspondance entre listeFilmLue et base (df ici) et afficher le titre du film en commun.
    result = df[df['movieId'].isin(listeFilmLue)]
    print("Les films que vous aimez sont :\n", np.unique(result['title']))
    print()
    
    # TODO les stats sur ces films
    
    
    #on appelle la fonction des stats par genre
    askMeGenre(df)
    
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
    
    """On test le modèle avec la liste de film de Cindy"""
    # TODO : à partir de la liste des films, faire les recommandations
    # on crée un df avec un movieId unique par ligne:
    df_unique = df.groupby(['title', 'movieId']).mean()
    df_unique.reset_index(inplace=True)
    df_unique.info()
    
    for idFilm in listeFilmLue:
      idFilm = int(idFilm)
      listeCol = np.append(movies["genres"].str.split('|', expand=True)[0].unique(), ['rating'])
      res = df_unique.loc[df_unique["movieId"] == idFilm]
      res = res[listeCol]
      
      recommandation2 = modelClassification2.kneighbors(res, n_neighbors=1, return_distance=False)
      print("Si vous avez aimé le film ", movies[movies["movieId"] == idFilm]["title"].values[0], ", le film suivant pourrait vous intéresser: \n")
      for item in np.nditer(recommandation2):
        print(dfAime[dfAime.index == item][["title", "genres"]].values[0])
      print()


   
