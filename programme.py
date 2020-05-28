#IMPORT des librairies
from sklearn.neighbors import KNeighborsClassifier
from outil import *
import random


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
    
    # ajout d'une colonne Link_movies avec formattage des lien imbd (7 chiffres)
    moviesLinks['Link_movies'] = ('https://www.imdb.com/title/tt') + moviesLinks['imdbId'].astype(str).apply(lambda x: x.zfill(7))

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
    
      #3b: Test du modèle KNN avec la liste de Cindy

    """On test le modèle avec la liste de film de Cindy"""
    df_unique = df.groupby(['title', 'movieId']).mean() #Calcul de la moyenne du rating par film
    df_unique.reset_index(inplace=True) 
    liste = []   
    for idFilm in listeFilmLue:
      idFilm = int(idFilm)
      listeCol = np.append(movies["genres"].str.split('|', expand=True)[0].unique(), ['rating'])
      res = df_unique.loc[df_unique["movieId"] == idFilm]
      res = res[listeCol]
      
      recommandation2 = modelClassification2.kneighbors(res, n_neighbors=2, return_distance=False)
     
      for item in np.nditer(recommandation2):
            proposition = df_unique[df_unique.index==item]["movieId"].values[0]
            if proposition not in (listeFilmLue and liste):
                  liste.append(proposition)
      
    # print(liste, "\n")
    recom = random.sample(liste,5)
    # print(recom, "\n")
    for ID in recom:
          print("titre du film: ", movies[movies["movieId"]==ID]["title"].values[0], "/catégorie du film: ", movies[movies["movieId"]==ID]["genres"].values[0], "\n")
   
# recherche le link movies       
res = []
for i in recom:
    lien = moviesLinks.loc[moviesLinks.movieId == i, 'Link_movies'].values[0]
    res.append(lien)

# recherche le link movies       
resTitre = []
for i in recom:
    lien = moviesLinks.loc[moviesLinks.movieId == i, 'title'].values[0]
    resTitre.append(lien)


# INTERFACE GRAPHIQUE
from tkinter import *

import webbrowser

i = res[0]

def open_imdb1():
    webbrowser.open(i, new=1, autoraise=True)

j = res[1]
    
def open_imdb2():
    webbrowser.open(j, new=1, autoraise=True)
    
k = res[2]
    
def open_imdb3():
    webbrowser.open(k, new=1, autoraise=True)
  
l = res[3]
   
def open_imdb4():
    webbrowser.open(l, new=1, autoraise=True)

m = res[4]

def open_imdb5():
    webbrowser.open(m, new=1, autoraise=True)

window = Tk()

window.title("Notre système de recommandation")

window.geometry("1080x720")

window.minsize(1080, 720)

window.config(background='black')

frame = Frame(window, bg='black')

label_title = Label(window, text="Voici la liste de nos 5 suggestions de films.", font=("Tahoma", 20),bg='black', fg='white')

label_title.pack()
#rouge : #f30a0e
label_subtitle = Label(window, text="Pour voir la fiche IMDb d'une de nos recommandations de films, cliquez dessus !", font=("Tahoma", 18),bg='black', fg='#f30a0e')

label_subtitle.pack()

m = resTitre[0]

yt_button1 = Button(frame, text = m, font=("Tahoma", 15),fg='black', bg='white', command=open_imdb1, relief='ridge', cursor='heart')

yt_button1.pack(pady=15, fill=X)

m = resTitre[1]

yt_button2 = Button(frame, text= m, font=("Tahoma", 15),fg='black', bg='white', command=open_imdb2, relief='ridge', cursor='gumby')

yt_button2.pack(pady=15, fill=X)

m = resTitre[2]

yt_button3 = Button(frame, text= m, font=("Tahoma", 15),fg='black', bg='white', command=open_imdb3, relief='ridge', cursor='umbrella')

yt_button3.pack(pady=15, fill=X)

m = resTitre[3]

yt_button4 = Button(frame, text= m, font=("Tahoma", 15),fg='black', bg='white', command=open_imdb4, relief='ridge', cursor='box_spiral')

yt_button4.pack(pady=15, fill=X)

m = resTitre[4]

yt_button5 = Button(frame, text= m, font=("Tahoma", 15),fg='black', bg='white', command=open_imdb5, relief='ridge', cursor='star')

yt_button5.pack(pady=15, fill=X)


frame.pack(expand=YES)

frame = Frame(window, bg='#B9DCDB')

label_subtitle = Label(window, text="Nous espérons que notre suggestion de films vous a plu, à bientôt !", font=("Tahoma", 15),bg='black', fg='#f30a0e')

label_subtitle.pack()

frame.pack(expand=YES)

window.mainloop()
