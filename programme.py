#IMPORT des librairies
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from outil import *

if __name__ == '__main__':
      
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
            
    #Etape 2: Lecture d'un fichier txt et affichage des titres de films
    listeFilmLue = lectureTxt("listeFilm.txt") #Lecture du fichier "listeFilm.txt"
    result = df[df['movieId'].isin(listeFilmLue)] #création d'un df ids contenus dans listeFilm.txt
    print("Les films que vous aimez sont :\n", np.unique(result['title']))
    print()
    
    #Etape 3: Modèle de recommandation:"Item-Item Collaborative Filtering"
      #3a: Modèle kNN
    
    """Définition de la base de données des films aimés"""
    dfAime=df[df["rating"]>=4].groupby(["movieId","title", "genres", "imdbId", "tmdbId"]).mean()
    dfAime.reset_index(inplace=True)
    
    """Définition des variables"""
    X2=dfAime.loc[:,np.append(df["genres"].str.split('|',expand=True)[0].unique(),["rating"])]
    y2=dfAime.loc[:, "movieId"]
            
    """Initialisation du modèle"""
    modelClassification2 = KNeighborsClassifier(n_neighbors=1)
    modelClassification2.fit(X2, y2)
    
      #3a: Test du modèle KNN
    """On test le modèle avec la liste de film de Cindy"""
    df_unique = df.groupby(['title', 'movieId']).mean() #Calcul de la moyenne du rating par film
    df_unique.reset_index(inplace=True) 
        
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
