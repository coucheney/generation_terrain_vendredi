###########################
# Auteur: Pierre Coucheney 
###########################

#######################
# import des librairies

import tkinter as tk
import random as rd


############################
# Définition des constantes

# hauteur du canevas
HAUTEUR = 600
# largeur du canevas
LARGEUR = 600
# taille de la grille
N = 50

# choix des couleurs
COUL_MUR = "grey"
COUL_VIDE = "white"

# paramètres de l'automate
# probabilité d'avoir un mur à l'initialisation
P = 0.5
# nombre d'itérations de l'automate
NB_ITER = 1
# seuil à partir duquel une case devient un mur
SEUIL = 4
# distance du voisinage
D = 1


######################
# variables globales

terrain = []
grille = []

#######################
# fonctions

def init_terrain():
    """ Initilise le terrain de la manière suivante:
    * met à 0 la liste à 2D appelée terrain qui contient pour chaque case la 
    valeur 1 si il y a un mur, et 0 sinon
    * initialise la liste à 2D grille qui contient l'identifiant
    de chaque carré dessiné sur le canevas 
    """
    global grille, terrain
    # on réinitialise les variables et le canvas
    grille = []
    terrain = []
    canvas.delete()
    for i in range(N):
        terrain.append([0]*N)
        grille.append([0]*N)

    for i in range(N):
        for j in range(N):
            if rd.uniform(0, 1) < P:
                terrain[i][j] = 1
                couleur = COUL_MUR
            else:
                couleur = COUL_VIDE
            largeur = LARGEUR // N
            hauteur = HAUTEUR // N
            x0, y0 = i * largeur, j * hauteur
            x1, y1 = (i + 1) * largeur, (j + 1) * hauteur
            rectangle = canvas.create_rectangle((x0, y0), (x1, y1), fill=couleur)
            grille[i][j] = rectangle


def affiche_terrain():
    """ Affiche le terrain sur le canvas"""
    for i in range(N):
        for j in range(N):
            if terrain[i][j] == 0:
                coul = COUL_VIDE
            else:
                coul = COUL_MUR
            canvas.itemconfigure(grille[i][j], fill=coul)


def sauvegarde():
    """ Ecrit la valeur N et la variable terrain
        dans le fichier sauvegarde.txt
    """
    fic = open("sauvegarde.txt", "w")
    fic.write(str(N) + "\n")
    for i in range(N):
        for j in range(N):
            fic.write(str(terrain[i][j]) + "\n")
    fic.close()    



def load():
    """Lit le fichier sauvegarde.txt et met à jour les variables
     N et terrain en conséquence, et modifie l'affichage
    """
    global N
    fic = open("sauvegarde.txt", "r")
    ligne = fic.readline()
    N = int(ligne)
    init_terrain()
    i = j = 0
    for ligne in fic:
        n = int(ligne)
        terrain[i][j] = n
        j += 1
        if j == N:
            j = 0
            i += 1
    fic.close()
    affiche_terrain()


def compte_mur(i, j, d):
    """Retourne le nombre de murs autour de la case de
     coordonnées (i, j) à distance inférieure à d"""
    cpt = 0
    delta_i = 0
    if i + d + 1 > N:
        delta_i = N
    for k in range(i-d-delta_i, i+d+1-delta_i):
        delta_j = 0
        if j + d + 1 > N:
            delta_j = N
        for l in range(j-d-delta_j, j+d+1-delta_j):
            if terrain[k][l] == 1:
                cpt += 1
    if terrain[i][j] == 1:
        cpt -= 1
    return cpt



def etape():
    """fait une étape de l'automate"""
    global terrain
    terrain_res = []
    for i in range(N):
        terrain_res.append([0]*N)
    for i in range(N):
        for j in range(N):
            mur = compte_mur(i, j, D)
            if mur > SEUIL:
                terrain_res[i][j] = 1
            else:
                terrain_res[i][j] = 0
    terrain = terrain_res
    affiche_terrain()



def genere():
    """générer un terrain"""
    init_terrain()
    for i in range(NB_ITER):
        etape()


def test_mur(event):
    """Fonction qui affiche le nombre de mur autour de la case cliquée"""
    x = event.x
    y = event.y
    largeur_case = LARGEUR // N
    hauteur_case = HAUTEUR // N
    i, j = x // largeur_case, y // hauteur_case
    print("i=", i, "j=", j, compte_mur(i, j, D))



#######################
# programme principal

# définition des widgets
racine = tk.Tk()
racine.title("Génération de terrain")
canvas = tk.Canvas(racine, width=LARGEUR, height=HAUTEUR, bg="blue")
bouton_sauv = tk.Button(racine, text="Sauvegarde", command=sauvegarde)
bouton_load = tk.Button(racine, text="Charger terrain", command=load)
bouton_genere = tk.Button(racine, text="génère terrain", command=genere)

# placement des widgets
canvas.grid(column=1, row=0, rowspan=10)
bouton_sauv.grid(row=0)
bouton_load.grid(row=1)
bouton_genere.grid(row=2)


canvas.bind("<Button-1>", test_mur)

# boucle principale
racine.mainloop()