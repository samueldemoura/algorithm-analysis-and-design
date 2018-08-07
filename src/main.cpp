#include <iostream>
#include <string>
#include "sorting_algorithms.h"

int main() {
	int array_size = 10;
	int array[array_size];

	for (int i = 0; true; ++i) {
		// Decide which sorting algorithm we're using
		std::string method;

		switch (i) {
		case 0:
			method = "Selection Sort"; break;
		case 1:
			method = "Insertion Sort"; break;
		case 2:
			method = "Merge Sort"; break;
		case 3:
			method = "Quick Sort"; break;
		default:
			i = -1;
		} if (i < 0) break; // Exit loop

		// Generate random int array
		for (int j = 0; j < array_size; ++j) array[j] = rand() % (array_size + 1);

		// Print it out
		std::cout << "=> Array before sorting: ";
		for (int i = 0; i < array_size; ++i) std::cout << array[i] << " ";
		std::cout << "\n";

		// Sort it
		switch (i) {
		case 0:
			selection_sort(array, array_size); break;
		case 1:
			insertion_sort(array, array_size); break;
		case 2:
			merge_sort(array, array_size); break;
		case 3:
			quick_sort(array, array_size); break;
		}

		// Print out the sorted array
		std::cout << "=> After " << method << ": ";
		for (int i = 0; i < array_size; ++i) std::cout << array[i] << " ";
		std::cout << "\n\n";

	}

	return 0;
}
