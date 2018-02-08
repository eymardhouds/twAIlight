from copy import deepcopy
from queue import Queue


class Morpion:
    """
    Equivalent de la classe Map sur le jeu des Vampires vs Loups-garous.

    Les joueurs sont soit True soit False.

    Par défaut, True commence"""

    def __init__(self):
        self.etats = list() # contenu du plateau, dans l'ordre dans lequel les pions sont joués

    def whos_turn(self):
        """ Renvoie le joueur qui a la main.

        :return: boolean: nom du joueur
        """
        if len(self.etats) % 2:
            return False
        else:
            return True

    def add_moves(self, moves):
        """ Rajoute une liste de mouvements au jeu Morpion

        :param moves: liste de mouvements
        :return: None
        """
        for move in moves:
            self.add_move(move)

    def add_move(self, move):
        """ Rajoute un mouvement à la carte.
        :param move: (i,j,player) avec i,j coordonnées et player le nom du joueur
        :return : None
        """

        if len(move) == 3:
            i, j, player = move
        else:
            i, j = move
            player = self.whos_turn()

        self.etats.append((i, j, player))

    def __copy__(self, objet):
        t = deepcopy(objet)
        return t

    def state_evaluation(self, curr_player):
        """ Renvoie l'évaluation d'une carte Morpion pour le joueur actuel

        :param curr_player: race du joueur actuel (boolean)
        :return: score de l'évaluation
        """
        other_player = not curr_player

        # Cas victoire
        if self.winner() == curr_player:
            return 10000

        # Cas défaite
        elif self.winner() == other_player:
            return -10000

        # Cas Partie en cours
        else:
            op_c = self.open_positions(curr_player)
            op_o = self.open_positions(other_player)
<<<<<<< HEAD:minimax.py
        return op_o - op_c

    def open_positions(self,player):
        count=0
        row_line_blanks=[]
        other_player = not player

        for i in range(3):
            # Quoiqu'il arrive on ajoute toutes les lignes blanches ou colonnes blanche
            if i not in [k[0] for k in self.etat]:
                count=count+1
            if i not in [k[1] for k in self.etat]:
                count=count+1
            # On parcourt ensuite les état qui pourraient donner lieu à une victoire

        #print("Je ne garde que mes états")
        #print([state for state in self.etat if state[2]!=other_player])
        for i in [state for state in self.etat if state[2]!=other_player]:
            # si une ligne n'est occupée que par nos pions, c'est une victoire potentielle
            #print([k[0] for k in self.etat if k!=i and k[2]==other_player])
            if i[0] not in [k[0] for k in self.etat if k!=i and k[2]==other_player]:
                count=count+1
            # Si une colonne n'est occupée que par nos pions c'est aussi une victoire potentielle
            if i[1] not in [k[1] for k in self.etat if k!=i and k[2]==other_player]:
                count=count+1
        # Cas particulier des diagonales
        if (1,1,other_player) in self.etat:
            # Si l'autre n'occupe pas le centre (donc soit nous l'occupons, soit il est vide), on regarde qui occupe les coins
            if other_player not in [k[2] for k in self.etat if k[0:2]==(0,1) or k[0:2]==(0,2) or k[0:2]==(2,0) or k[0:2]==(2,2)]:
                count=count+1
=======
        return op_c - op_o # Nombre de positions ouvertes pour nous - Nombre de positions ouevrtes pour notre adversaire

    def open_positions(self, curr_player):
        """ Renvoie le nombre de ligne/Colonne/Diagonale ouverte pour le joueur actuel

        :param curr_player: race du joueur actuel (boolean)
        :return: Nombre d'ouvertures
        """
        count = 0 # Compte d'ouverture

        other_player = not curr_player

        # Quoiqu'il arrive on ajoute toutes les lignes vides ou colonnes vides
        for i in range(3):
            if i not in [k[0] for k in self.etats]:
                count = count + 1
            if i not in [k[1] for k in self.etats]:
                count = count + 1

        # On parcourt ensuite les état qui pourraient donner lieu à une victoire
        for i,j,race_joueur in self.etats:
            # si une ligne n'est occupée que par nos pions, c'est une victoire potentielle
            if i not in [x for x,y,race in self.etats if (i,j,race_joueur) != (x,y,race) and race == other_player]:
                count = count + 1
            # Si une colonne n'est occupée que par nos pions c'est aussi une victoire potentielle
            if j not in [y for x,y,race in self.etats if (i,j,race_joueur) != (x,y,race) and race == other_player]:
                count = count + 1

        # Cas particulier des diagonales
        #  Si l'adversaire n'occupe pas le centre
        if (1, 1, other_player) not in self.etats:
            # soit nous l'occupons, soit il est vide --> on regarde qui occupe les coins
            if other_player not in [race for x,y,race in self.etats if (x,y) in [(0, 2),(2, 0)]]:
                count = count + 1
            if other_player not in [race for x,y,race in self.etats if (x,y) in [(0, 0),(2, 2)]]:
                count = count + 1

>>>>>>> c1a606a8044b24ea5ecbd5ec310ae62094ae815f:alpha_beta.py
        return count

    def winner(self):
        """ Renvoie la race du joueur gagnant

        :return: True, False ou None si Partie encore en cours
        """

        # Parcours de la première ligne pour observer les colonnes
        for i in range(3):

            # Pour la ligne i, on cherche le joueur qui l'occupe
            if (i, 0, True) in self.etats:
                current_player = True
            elif (i, 0, False) in self.etats:
                current_player = False
            else:
                break

            # On regarde les deux autres éléments de la colonne pour vérifier si elle est occupée par le même joueur
            if (i, 1, current_player) in self.etats and (i, 2, current_player) in self.etats:
                return current_player

        # Parcours de la première colonne pour observer les lignes
        for j in range(3):

            # Pour la colonne j, on cherche le joueur qui l'occupe
            if (0, j, True) in self.etats:
                current_player = True
            elif (0, j, False) in self.etats:
                current_player = False
            else:
                break

            # On regarde les deux autres éléments de la ligne pour vérifier si elle est occupée par le même joueur
            if (1, j, current_player) in self.etats and (2, j, current_player) in self.etats:
                return current_player

        # Cas des diagonales

        # Joueur pouvant avoir une diagonale
        if (1, 1, True) in self.etats:
            current_player = True
        elif (1, 1, False) in self.etats:
            current_player = False
        else:
            return None

        # Parcours des deux diagonales avec l'information du joueur qui a le centre
        if (0, 0, current_player) in self.etats and (2, 2, current_player) in self.etats:
            return current_player
        if (2, 0, current_player) in self.etats and (0, 2, current_player) in self.etats:
            return current_player

        return None

    def next_possible_moves(self):
        possible_moves = set((i, j) for i in range(3) for j in range(3))
        possible_moves -= set((i, j) for i, j, _ in self.etats)
        next_player = self.whos_turn()
        return set((i, j, next_player) for (i, j) in possible_moves)

    def game_over(self):
        for i in range(3):
            if (i, 0, True) in self.etats:
                current_player = True
            elif (i, 0, False) in self.etats:
                current_player = False
            else:
                break
            if (i, 1, current_player) in self.etats and (i, 2, current_player) in self.etats:
                return True

        for j in range(3):
            if (0, j, True) in self.etats:
                current_player = True
            elif (0, j, False) in self.etats:
                current_player = False
            else:
                break
            if (1, j, current_player) in self.etats and (2, j, current_player) in self.etats:
                return True

        if (1, 1, True) in self.etats:
            current_player = True
        elif (1, 1, False) in self.etats:
            current_player = False
        else:
            return False
        if (0, 0, current_player) in self.etats and (2, 2, current_player) in self.etats:
            return True
        if (2, 0, current_player) in self.etats and (0, 2, current_player) in self.etats:
            return True

        return False

    def __repr__(self):
        res = "-------\n"
        for j in range(3):
            for i in range(3):
                res += '|'
                if (i, j, True) in self.etats:
                    res += "X"
                elif (i, j, False) in self.etats:
                    res += "O"
                else:
                    res += " "
            res += '|\n-------\n'
        return res


class GrapheDeJeu:
    def __init__(self):
        self.noeuds = []

    def add_vertice(self, vertice):
        if isinstance(vertice, SommetDuJeu):
            self.noeuds.append(vertice)

    def add_vertices(self, vertices):
        for vert in vertices:
            self.add_vertice(vert)


class SommetDuJeu:
    def __init__(self, is_ami):
        self.children = list()
        self.alpha = None
        self.beta = None
        self.etat = Morpion()
        self.is_ami = is_ami

    def __copy__(self, objet):
        t = deepcopy(objet)
        return t

    # MaxValue et MinValue vont devoir utiliser un parcours de graph type DFS
    def MinValue(self):
        pass

    def MaxValue(self):
        val = self.etat.state_evaluation(self.is_ami)
        return val


def select_move_to_study(self, data):
    return data


def get_graph(morpion_state, is_ami, level, total_level, child_vertice, graph_du_jeu, i):
    """
    Fonction de generation recursive de graph
    A un level
    """
    # On genere un graph dont la racine est morpion_state
    cur_vertice = SommetDuJeu(is_ami)
    cur_vertice.etat = cur_vertice.etat.__copy__(morpion_state)
    graph_du_jeu.add_vertice(cur_vertice)
    is_ami = not is_ami
    child_vertice[level] = {}
    # on commence par le base case: l'etat que l'on nous envoie est il un etat final ?
    if morpion_state.game_over() or level >= total_level:
        # dans ce cas la on s'arrete et on sort de la boucle
        pass;

    else:
        # Dans ce cas on peut rajouter des vertices avec des etats
        # On ajoute chacun des états possibles qui peut succéder à l'état actuel
        for move in cur_vertice.etat.next_possible_moves():
            # On copie l'état actuel du jeu:
            child_vertice[level][i] = SommetDuJeu(is_ami)
            child_vertice[level][i] = child_vertice[level][i].__copy__(cur_vertice)
            # On ajoute au nouvel état le nouveau move possible
            child_vertice[level][i].etat.add_move(move)

            # On lie au noeud père le noeuf enfant
            cur_vertice.children.append(child_vertice[level][i])
            graph_du_jeu.add_vertice(child_vertice[level][i])
            # On ajoute les noeufs enfants du noeuf enfant

            get_graph(child_vertice[level][i].etat, is_ami, level + 1, total_level, child_vertice, graph_du_jeu, i + 1)

    return graph_du_jeu


def minimax(morpion_state, is_ami):
    """
    cette fonction doit retourner le meilleur mouvement étant donné un état du jeu
    """
    # On commence par générer un graph avec tous les états du jeu
    horizon = 1
    graph_du_jeu = GrapheDeJeu()
    graph = get_graph(morpion_state, is_ami, 0, horizon, {}, graph_du_jeu, 0)
    print(graph)
    # On parcourt ce graph et on regarde la Max,MinValue de chacun des etats feuilles
    Q = Queue()
<<<<<<< HEAD:minimax.py
    # Initialisation du parcours de graph
    Q.put(graph.noeuds[0])
    # parcours de graph
    print("Parcours de graph")
    max_val=0
    while not Q.empty():
        cur=Q.get()
        val = cur.MaxValue()

        if val > max_val:
            max_val=val
            print("best configuration updated:")
            print(cur.etat.etat)
            best_scenario = cur.etat.etat
        # Ajout des enfants
        for c in cur.children:
            Q.put(c)

    # il faut faire remonter certaines valeurs et baisser les autres

    return best_scenario
=======
    for child in graph.noeuds:
        q.put(child)
        child.maxValue()
        print(child.maxValue())
    # cur_vertice.MaxValue()
    return 0
>>>>>>> c1a606a8044b24ea5ecbd5ec310ae62094ae815f:alpha_beta.py


if __name__ == "__main__":
    morpion = Morpion()
    print(morpion.game_over())
    print(morpion.next_possible_moves())
<<<<<<< HEAD:minimax.py
    morpion.add_moves([(0, 1),(2,0)])
    count=0
    #print(morpion.state_evaluation(False))
    best_next_move = minimax(morpion,False)
    morpion.add_move(best_next_move[-1])
    print(morpion)
    #print(morpion.game_over())
    #print(morpion.winner())
=======
    morpion.add_moves([(0, 1), (1, 0)])
    print(morpion)
    best_next_move = minimax(morpion, False)
    morpion.add_move(best_next_move)
    print(morpion)

    # print(morpion.game_over())
    # print(morpion.winner())
>>>>>>> c1a606a8044b24ea5ecbd5ec310ae62094ae815f:alpha_beta.py
