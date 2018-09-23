'''Implementation of Prim's algortihm.'''
import sys
import numpy as np

if __name__ == '__main__':
	# Read size from stdin, create adjacency matrix
	matrix_size = int(sys.stdin.readline())
	matrix_original = np.full([matrix_size, matrix_size], np.nan)

	# Auxiliary matrix. Third dimension stores: cheapest cost
	# to connect a vertex, which edge that cost refers to, if cost
	# was previously calculated.
	aux = np.full([matrix_size, matrix_size, 3], np.nan)

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
		# Calculate connection cost estimates from each vertex in the tree
		for vertex_from in in_tree:
			for vertex_to in out_of_tree:
				# Write to auxiliary matrix if calculated cost is smaller
				old_cost = aux[vertex_from, vertex_to, 0]
				new_cost = matrix_original[vertex_from, vertex_to]

				# TODO: instead of two checks, maybe make this line work:
				#new_cost = matrix_original[vertex_to, vertex_from] if np.isnan(new_cost) else new_cost

				if (new_cost < old_cost or np.isnan(old_cost) and
					np.isnan(aux[vertex_from, vertex_to, 2])):
					aux[vertex_from, vertex_to, 0] = new_cost
					aux[vertex_from, vertex_to, 1] = vertex_from
					aux[vertex_from, vertex_to, 2] = True

				'''Ugly workaround: input is actually a symmetrical matrix
				being treated as a diagonal matrix, so we must check with
				coordinates inverted as well.'''
				old_cost = aux[vertex_from, vertex_to, 0]
				new_cost = matrix_original[vertex_to, vertex_from]

				if (new_cost < old_cost or np.isnan(old_cost) and
					np.isnan(aux[vertex_to, vertex_from, 2])):
					aux[vertex_from, vertex_to, 0] = new_cost
					aux[vertex_from, vertex_to, 1] = vertex_from
					aux[vertex_from, vertex_to, 2] = True

		# Find the minimum-weight edge
		smallest = None
		for vertex in in_tree:
			try:
				tmp = np.nanargmin(aux[vertex, :, 0])
				if smallest == None or aux[vertex, tmp, 0] < aux[smallest[0], smallest[1], 0]:
					smallest = (vertex, tmp)
			except ValueError:
				# All-NaN slice encountered.
				# TODO: figure out if we should really just skip this?
				continue

		# And connect it to the tree
		in_tree.append(smallest[1])
		out_of_tree.remove(smallest[1])

		# Write to the solution matrix
		'''Ugly workaround: use min() & max() to guarantee we only write on the
		top-right part of the solution matrix.'''
		matrix_solution[min(smallest), max(smallest)] = aux[smallest[0], smallest[1], 0]

		# Remove from auxiliary matrix so it doesn't get returned again
		aux[smallest[0], smallest[1], 0] = np.nan

	print('=> Input matrix:')
	print(matrix_original)

	print('\n=> Solution matrix:')
	print(matrix_solution)
