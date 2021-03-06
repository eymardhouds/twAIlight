import time
from itertools import product
import random
from copy import copy, deepcopy

import numpy as np
from scipy import signal

from twAIlight.Map import Map
#from twAIlight.Cartes.Map_Ligne13 import MapLigne13
from twAIlight.Cartes.Map_Ligne13 import MapLigne13
from twAIlight.Cartes.Map_Map8 import Map8
from twAIlight.Cartes.Map_TheTrap import MapTheTrap

def create_matrix1(carte):
    return [[carte.content[i,j][0] for j in range(carte.size[1])] for i in range(carte.size[0])]
   
def test_create_matrix1(carte):
    # Création de matrice 1 : Pure Python
    start_time = time.time()
    for _ in range(1000):
        matrix1 = [[carte.content[i,j][0] for j in range(carte.size[1])] for i in range(carte.size[0])]
    end_time = time.time()
    print(end_time - start_time)


def test_create_matrix2(carte):
    # Création de matrice 2 : Pure Numpy
    start_time = time.time()
    for _ in range(1000):
        matrix2 = np.reshape(np.array(list(carte.content.values()))[:,0], carte.size)
    end_time = time.time()
    print(end_time - start_time)

def create_matrix3(carte):
    return np.array([[carte.content[i,j][0] for j in range(carte.size[1])] for i in range(carte.size[0])])

def test_create_matrix3(carte):
    # Création de matrice 3 : Mix
    start_time = time.time()
    for _ in range(1000):
        matrix3 = create_matrix3(carte)
    end_time = time.time()
    print(end_time - start_time)

def test_create_matrix4(carte):
    # Création de matrice 4 : Full Numpy 2
    start_time = time.time()
    for _ in range(1000):
        temp = np.array(list(map(list,carte.content.values())))
        matrix4 = temp.reshape((carte.size[0], carte.size[1], 3))[:,:,0]
    end_time = time.time()
    print(end_time - start_time)


def test_convolve1(carte, matrix1, kernel):
    # Produit de convolution 1: Full Python
    start_time = time.time()
    for _ in range(1000):
        conv1 = [[0 for _ in range(carte.size[1])] for _ in range(carte.size[0])]
        for i,j in product(range(len(matrix1)), range(len(matrix1[0]))):
            for x in range(len(kernel)):
                for y in range(len(kernel[0])):
                    if 0 <= i+(x-1) < len(matrix1) and 0 <= j+(y-1) < len(matrix1[0]):
                        conv1[i][j] += kernel[x][y] * matrix1[i+(x-1)][j+(y-1)]
    end_time = time.time()
    print(end_time - start_time)

def test_convolve2(matrix2, kernel):
    # Produit de convolution 2: Full numpy
    start_time = time.time()
    for _ in range(1000):
        conv2 = signal.convolve2d(matrix2, kernel, mode="same")
    end_time = time.time()
    print(end_time - start_time)

def main_test_convolution():
    carte = MapLigne13()
    test_create_matrix1(carte)
    test_create_matrix2(carte)
    test_create_matrix3(carte)
    test_create_matrix4(carte)
    # La création 1 Pur Python gagne de 20% environ

    mat = create_matrix1(carte)
    np_mat = create_matrix3(carte)
    kernel = [[1,1,1], [1,2,1], [1,1,1]]
    test_convolve1(carte, mat, kernel)
    test_convolve2(np_mat, kernel)

def test_ranked_moves(carte):
    start_time = time.time()
    for _ in range(1000):
        carte.next_ranked_moves(True)
    end_time = time.time()
    print(end_time - start_time)

def test_possible_moves(carte):
    start_time = time.time()
    for _ in range(1000):
        carte.next_possible_moves(True)
    end_time = time.time()
    print(end_time - start_time)

def test_probable_outcome(carte):
    start_time = time.time()
    for _ in range(1000):
        carte.most_probable_outcome([(6,4,5,7,4)])
    end_time = time.time()
    print(end_time - start_time)

def test_repartitions_recursive(carte, pop_m, n_case):
    start_time = time.time()
    #print(carte.repartitions_recursive(pop_m, n_case))
    for _ in range(100):
        carte.repartitions_recursive(pop_m, n_case)
    end_time = time.time()
    print(end_time - start_time)


def test_relevant_repartitions(carte, pop_m, n_case):
    start_time = time.time()
    #print(carte.relevant_repartitions(pop_m, n_case))
    for _ in range(100):
        carte.relevant_repartitions(pop_m, n_case)
    end_time = time.time()
    print(end_time - start_time)

def test_copy(carte):
    moves = random.choice(carte.next_possible_moves(is_vamp=True))
    carte.print_map()
    
    child = copy(carte)
    #print(child.content)
    child.print_map()
    child.compute_moves(moves)
    carte.print_map()
    child.print_map()

def test_main_map(carte):
    is_vamp = False
    for _ in range(5):
        carte.print_map()
        if carte.game_over(): break
        is_vamp = not is_vamp
        next_moves = carte.next_ranked_moves(is_vamp)
        print("{} possible moves".format(len(next_moves)))
        print(next_moves[:3])
        carte.compute_moves(random.choice(next_moves[:5]))

if __name__ == '__main__':
    carte = Map8()
    # POP_M = 1
    # N_CASE = 8
    #test_relevant_repartitions(carte, POP_M, N_CASE)
    #test_repartitions_recursive(carte, POP_M, N_CASE)
    import cProfile
    #cProfile.run("test_possible_moves(carte)")
    def to_test(carte):
        next_moves = carte.next_possible_moves(True, nb_group_max=None, stay_enabled=None)
        #carte.print_map()
        return len(next_moves), next_moves
    cProfile.run("print(to_test(carte))")
