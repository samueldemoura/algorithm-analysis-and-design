import sys
import numpy as np

if __name__ == '__main__':
	# Read input from stdin
	number_of_items, capacity = sys.stdin.readline().split()

	# :(
	number_of_items = int(number_of_items)
	capacity = int(capacity)

	weight = np.zeros([number_of_items], dtype=int)
	value = np.zeros([number_of_items], dtype=int)

	memo = np.zeros([capacity + 1, number_of_items + 1])
	items_taken = [[None for i in range(0, number_of_items + 1)] for j in range (0, capacity + 1)]

	for i in range(0, number_of_items):
		tmp_weight, tmp_value = sys.stdin.readline().split()
		weight[i] = int(tmp_weight)
		value[i] = int(tmp_value)

	# Algorithm starts here
	for remaining_capacity in range(0, capacity + 1):
		for i in range(0, number_of_items + 1):
			if remaining_capacity == 0 or i == 0:
				# No more items can fit in the knapsack or invalid item
				memo[remaining_capacity, i] = 0
				items_taken[remaining_capacity][i] = []

			elif remaining_capacity < weight[i - 1]:
				# This item doesn't fit
				memo[remaining_capacity, i] = memo[remaining_capacity, i - 1]
				items_taken[remaining_capacity][i] = [] + items_taken[remaining_capacity][i - 1]

			else:
				# Choose between taking this item or not
				take = memo[remaining_capacity - weight[i - 1], i - 1] + value[i - 1]
				dont_take = memo[remaining_capacity, i - 1]

				memo[remaining_capacity, i] = max(take, dont_take)
				items_taken[remaining_capacity][i] = []

				if take > dont_take:
					items_taken[remaining_capacity][i] += items_taken[remaining_capacity - weight[i - 1]][i - 1]
					items_taken[remaining_capacity][i].append(i - 1)
				else:
					items_taken[remaining_capacity][i] += items_taken[remaining_capacity][i - 1]

	# Print result
	best_i, best_j = np.unravel_index(memo.argmax(), memo.shape)
	print('-> Best solution:\nValue: {0}\nItems taken: {1}'.format(
		memo[best_i, best_j], str(items_taken[best_i][best_j]))
	)
