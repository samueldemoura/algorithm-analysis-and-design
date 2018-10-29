import random
import numpy as np


def build_paths_matrix(np_ar):
    idx_to_weights = np.zeros((np_ar.shape[0], np_ar.shape[1], 2))
    idx_to_weights[:, :, 1] = ar
    idx_to_weights[:, :, 0] = np.arange((np_ar.shape[0]))
    print('2\n', idx_to_weights, end='\n\n')
    return idx_to_weights


def sorted_ar(np_ar):
    sorted_idxs = np.argsort(np_ar[:, -1])
    return np_ar[sorted_idxs]


def construction_phase(idx_to_weights_ar):
    remaining_points = list(range(idx_to_weights_ar.shape[0]))
    solution = []

    # Random starting vertex
    idx_from = random.randrange(len(remaining_points))
    solution.append(remaining_points.pop(idx_from))

    while len(remaining_points):
        alpha_slice = int(round(alpha * (len(remaining_points) - 1)))

        possible_paths = idx_to_weights_ar[idx_from, remaining_points]

        # Choosing next vertex
        rcl = sorted_ar(possible_paths)[:1 + alpha_slice]
        random_choice = random.randrange(len(rcl))
        next_vertex = int(rcl[random_choice, 0])

        # Moving chosen vertex from 'remaining_points' to 'solution'
        solution.append(remaining_points.pop(remaining_points.index(next_vertex)))
        idx_from = solution[-1]

    print('Solution:', solution)
    print('Sum:', np.sum(idx_to_weights_ar[solution, 1]))


alpha = 0.0

num_vertices = 4
ar = np.random.rand(num_vertices, num_vertices)
print('1\n', ar)

paths_matrix = build_paths_matrix(ar)

construction_phase(paths_matrix)
