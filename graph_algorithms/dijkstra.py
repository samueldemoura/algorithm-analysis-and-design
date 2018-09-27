'''Implementation of Prim's algortihm.'''
import sys
import numpy as np

if __name__ == '__main__':
	# Read size from stdin, create adjacency matrix
	matrix_size = int(sys.stdin.readline())
	matrix_original = np.full([matrix_size, matrix_size], np.nan)

	# Auxiliary matrix. Third dimension stores: cheapest cost
	# to connect a vertex, which vertex that cost refers to, if cost
	# was previously calculated.
	aux = np.full([matrix_size, matrix_size, 3], np.nan)

	# Array to keep track of cost to get to a certain vertex
	cost_sum = np.zeros([matrix_size])

	# Read weights from stdin
	for i, line in enumerate(sys.stdin):
		for j, element in enumerate(line.split()):
			matrix_original[i, j + i + 1] = int(element)

	# Make a copy of the matrix that we can alter
	matrix = matrix_original.copy()

	# Output matrix with our solution
	matrix_solution = np.zeros([matrix_size, matrix_size])

	# Lists to keep track of which vertexes are in/out of the solution
	in_tree = [0] # initially, the solution contains only vertex 0
	out_of_tree = [i for i in range(1, matrix_size)] # everyone else is out

	'''Taken from Wikipedia:
	Grow the tree by one edge: of the edges that connect the tree to
	vertices not yet in the tree, find the minimum-weight edge, and
	transfer it to the tree.
	'''
	while out_of_tree:
		possible_connections = []

		# Calculate connection cost estimates from each vertex in the tree
		for vertex_from in in_tree:
			for vertex_to in out_of_tree:
				# Write to auxiliary matrix if calculated cost is smaller
				old_cost = aux[vertex_from, vertex_to, 0]
				new_cost = matrix_original[vertex_from, vertex_to] + cost_sum[vertex_from]

				# Treat case where we look in the bottom left of the matrix
				if np.isnan(new_cost):
					new_cost = matrix_original[vertex_to, vertex_from] + cost_sum[vertex_from]

				if (new_cost < old_cost or
					np.isnan(old_cost) and np.isnan(aux[vertex_from, vertex_to, 2])):
					# Found a connection with smaller cost than previously seen
					aux[vertex_from, vertex_to, 0] = new_cost
					aux[vertex_from, vertex_to, 1] = vertex_from
					aux[vertex_from, vertex_to, 2] = True

					possible_connections.append((vertex_from, vertex_to, new_cost))
				else:
					# Old cost was better
					possible_connections.append((vertex_from, vertex_to, old_cost))

		# Find the minimum-weight edge
		possible_connections.sort(key=lambda x: x[2])
		smallest = possible_connections[0]

		# Connect it to the tree
		in_tree.append(smallest[1])
		out_of_tree.remove(smallest[1])

		# Write down cost to get to this vertex
		#print('Connected {0} to {1}, took {2} to get here'.format(smallest[0], smallest[1], smallest[2]))
		cost_sum[smallest[1]] = smallest[2]

		# Write to the solution matrix (min & max are to guarantee we write on the top right)
		matrix_solution[min(smallest[0:2]), max(smallest[0:2])] = smallest[2]

	print(matrix_solution)
