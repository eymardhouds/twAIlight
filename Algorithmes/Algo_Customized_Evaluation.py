# -*- coding: utf-8 -*-
from copy import deepcopy

from Joueur_Interne import JoueurInterne
from Algorithmes.Algo_Aleatoire import AlgoAleatoireInterne
from Algorithmes.Algo_NegaMax import AlgoNegaMax
from Cartes.Map_Dust2 import MapDust2
from Cartes.Map_TheTrap import MapTheTrap
from Cartes.Map_Map8 import Map8
from Serveur_Interne import ServeurInterne


class AlgoCustomizedEvaluation(JoueurInterne):
    """
    Une réécriture de la classe JoueurInterne, qui suit une fonction d'évaluation personnalisée

    """

    @staticmethod
    def customized_evaluation(game_map):
        """Renvoie une évaluation personnalisée d'une carte

        :return: cus_eval
        """

        if game_map.game_over():
            return game_map.state_evaluation()

        n_hum, n_vamp, n_lg = game_map.populations()

        cus_eval = n_vamp - n_lg  # Evaluation classique

        # Recherche du nombre de sous-groupes
        n_ss_vamp = 0
        n_ss_lg = 0
        for i_j in game_map.content:
            _, n_vamp, n_lg = game_map.content[i_j]
            if n_vamp:
                n_ss_vamp += 1
            if n_lg:
                n_ss_lg += 1
        cus_eval += -0.1 * (n_ss_vamp - n_ss_lg)

        # Distance des plus proches humains
        d_hum_vamp = None
        d_hum_lg = None

        for i, j in game_map.content:
            _, n_vamp, n_lg = game_map.content[(i, j)]

            # Si la case est peuplée de monstres, on cherche les humains les plus proches
            if n_vamp:
                for x, y in game_map.content:
                    n_hum, _, _ = game_map.content[(x, y)]
                    if 0 < n_hum <= n_vamp:
                        current_distance = max(abs(i - x), abs(j - y))
                        if d_hum_vamp is None:
                            d_hum_vamp = current_distance
                        elif d_hum_vamp > current_distance:
                            d_hum_vamp = current_distance
                        if d_hum_vamp == 1:
                            break

            if n_lg:
                for x, y in game_map.content:
                    n_hum, _, _ = game_map.content[(x, y)]
                    if 0 < n_hum <= n_lg:
                        current_distance = max(abs(i - x), abs(j - y))
                        if d_hum_lg is None:
                            d_hum_lg = current_distance
                        elif d_hum_lg > current_distance:
                            d_hum_lg = current_distance
                        if d_hum_lg == 1:
                            break

        # S'il n'y a plus d'humains sur la carte
        if d_hum_lg is not None and d_hum_vamp is not None:
            cus_eval += -0.1 * (d_hum_vamp - d_hum_lg)

        return cus_eval

    def evaluate_moves(self, moves):
        """ Renvoie l'évaluation de mouvements sur une carte

        :param moves: mouvements proposés
        :return: évaluation
        """
        cur_evaluation = 0
        for proba, updated_positions in self.map.possible_outcomes(moves):
            carte = deepcopy(self.map)
            carte.update_positions(updated_positions)
            move_evaluation = AlgoCustomizedEvaluation.customized_evaluation(carte)
            cur_evaluation += proba * move_evaluation
        return cur_evaluation

    def next_moves(self, show_map=True):
        """ Renvoie le prochain mouvement prometteur avec l'évaluation personnalisée

        :param show_map: (boolean) Affichage de la carte
        :return: list
        """
        if show_map: self.map.print_map()

        # Evaluation actuelle de la carte
        current_evaluation = AlgoCustomizedEvaluation.customized_evaluation(self.map)

        better_moves = None
        better_evaluation = None

        for moves in self.map.next_possible_moves(self.is_vamp):
            if self.is_vamp:
                # Si le mouvement est intéressant pour les vampires
                if self.evaluate_moves(moves) > current_evaluation:
                    return moves

                if better_moves is None:
                    better_moves = moves
                    better_evaluation = self.evaluate_moves(moves)
                elif better_evaluation < self.evaluate_moves(moves):
                    better_moves = moves
                    better_evaluation = self.evaluate_moves(moves)
            else:
                # Si le mouvement est intéressant pour les loup-garous
                if self.evaluate_moves(moves) < current_evaluation:
                    return moves

                if better_moves is None:
                    better_moves = moves
                    better_evaluation = self.evaluate_moves(moves)
                elif better_evaluation > self.evaluate_moves(moves):
                    better_moves = moves
                    better_evaluation = self.evaluate_moves(moves)

        else:
            # On ne trouve pas de mouvement améliorant la situation du joueur,
            # On renvoie le moins pire des mouvements trouvés
            return better_moves

    @classmethod
    def nb_vertices_created(cls):
        return 0


if __name__ == '__main__':
    Joueur1 = AlgoCustomizedEvaluation
    Joueur2 = AlgoNegaMax
    MapDust2 = MapTheTrap
    Serveur = ServeurInterne(MapDust2, Joueur1, Joueur2, name1="Evaluation", name2="NegaMax", print_map=True)
    Serveur.start()
