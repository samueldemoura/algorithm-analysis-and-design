#include <iostream>
#include <string>
#include "sorting_algorithms.h"
#define TOTAL_ALGORITHMS 2

int main() {
	int array_size = 10;
	int array[array_size];

	for (int i = 0; i < TOTAL_ALGORITHMS; ++i) {
		// Decide which sorting algorithm we're using
		std::string method;

		switch (i) {
		case 0:
			method = "Selection Sort";
		case 1:
			method = "Insertion Sort";
		}

		// Generate random int array
		for (int j = 0; j < array_size; ++j) array[j] = rand() % (array_size + 1);

		// Print it out
		std::cout << "=> Array before sorting: ";
		for (int i = 0; i < array_size; ++i) std::cout << array[i] << " ";
		std::cout << "\n";

		// Sort it
		switch (i) {
		case 0:
			selection_sort(array, array_size);
		case 1:
			insertion_sort(array, array_size);
		}

		// Print out the sorted array
		std::cout << "=> After " << method << ": ";
		for (int i = 0; i < array_size; ++i) std::cout << array[i] << " ";
		std::cout << "\n\n";

	}

	return 0;
}
