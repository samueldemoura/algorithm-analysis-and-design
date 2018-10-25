'''Embarassing attempt at implementing Held-Karp's algorithm.'''
import sys
import numpy as np

class DynamicTSP():

	memo = None
	weights = None
	dimension = None

	def recursive_tsp(self, pos=0, bitmask=0):
		if (bitmask == (1 << self.dimension) - 1):
			# Looping back
			return self.weights[pos, 0]
		if not np.isnan(self.memo[pos, bitmask]):
			# Already calculated
			return self.memo[pos, bitmask]

		# Not yet calculated
		best_value = np.inf

		for i in range(0, self.dimension):
			if bitmask & (1 << i) == 0 and i != pos:
				best_value = min(
					best_value,
					self.weights[pos, i] + self.recursive_tsp(i, bitmask | (1 << i))
					)

		self.memo[pos, bitmask] = best_value
		return best_value

if __name__ == '__main__':
	# Read input from stdin
	tsp = DynamicTSP()

	tsp.dimension = int(sys.stdin.readline())
	tsp.weights = np.zeros([tsp.dimension, tsp.dimension], dtype=int)
	tsp.memo = np.full([tsp.dimension, 2**tsp.dimension], np.nan) # ouch
	tsp.memo_path = []

	for i in range(0, tsp.dimension):
		for j, value in enumerate(sys.stdin.readline().split()):
			tsp.weights[i, j] = int(value)

	print(tsp.recursive_tsp())
