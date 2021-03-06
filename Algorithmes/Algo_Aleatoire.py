# -*- coding: utf-8 -*-

from Joueur import Joueur
from Joueur_Interne import JoueurInterne
from Serveur_Interne import ServeurInterne
from Map import Map

class AlgoAleatoire(JoueurInterne):
    """
    Joueur avec la fonction de décision aléatoire de Charles
    """
class AlgoAleatoireInterne(JoueurInterne):
    """
    Joueur avec la fonction de décision aléatoire de Charles
    """

    @classmethod
    def nb_vertices_created(cls):
        return 0

if __name__=="__main__":
    # Joueur Interne
    Joueur1=AlgoAleatoireInterne
    Joueur2 =AlgoAleatoireInterne
    Serveur=ServeurInterne(Map,Joueur1,Joueur2)
    Serveur.start()

    # Joueur Réel
    #Joueur_1=AlgoAleatoire()
    #Joueur_1.start()
    #Joueur_1.join()
