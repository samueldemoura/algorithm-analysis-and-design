'''Simplest possible implementation of Kruskal's algortihm.'''
import sys
import numpy as np

if __name__ == '__main__':
	# Read size from stdin, create adjacency matrix
	matrix_size = int(sys.stdin.readline())
	matrix_original = np.full([matrix_size, matrix_size], np.nan)

	# Keeps track of which "sub-trees" are connected
	aux = [i for i in range(0, matrix_size)]

	# Read weights from stdin
	for i, line in enumerate(sys.stdin):
		for j, element in enumerate(line.split()):
			matrix_original[i, j + i + 1] = int(element)

	# Make a copy of the matrix that we can alter
	matrix = matrix_original.copy()

	# Output matrix with our solution
	matrix_solution = np.zeros([matrix_size, matrix_size])

	# Connect sub-trees
	for i in range(0, matrix_size ** 2):
		smallest = np.unravel_index(np.nanargmin(matrix), matrix.shape)

		if aux[smallest[0]] != aux[smallest[1]]:
			# Safe to connect
			'''print('Connected! Value {0} at ({1}, {2})'.format(
				matrix[smallest], smallest[0], smallest[1])
			)'''

			# Higher id gets replaced with lower id
			left_id = aux[smallest[0]]
			right_id = aux[smallest[1]]
			new_id = left_id if left_id < right_id else right_id
			old_id = left_id if left_id > right_id else right_id

			aux[:] = [new_id if x == old_id else x for x in aux]

			# Write this connection in the solution matrix
			matrix_solution[smallest] = matrix[smallest]

			# Remove element from array so nanargmin returns a new value next time
			matrix[smallest] = np.nan

	print('=> Input matrix:')
	print(matrix_original)

	print('\n=> Solution matrix:')
	print(matrix_solution)
