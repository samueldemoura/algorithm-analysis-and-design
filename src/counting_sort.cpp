#include <iostream>

void counting_sort(int *array, int size, int k) {
	int count[k + 1];
	int aux[size];

	for (int i = 0; i < k; ++i)
		count[i] = 0;

	for (int i = 0; i < size; ++i)
		++count[array[i]], aux[i] = array[i];

	for (int i = 1; i < k; ++i)
		count[i] += count[i - 1];

	for (int i = size - 1; i > -1; --i)
		array[--count[aux[i]]] = aux[i];
}
