void selection_sort(int *array, int size) {
	for (int i = 0; i < size; ++i) {
		// Index of smallest element is initially the current element
		int min_index = i;

		// Look for the smallest element in the array
		for (int j = i + 1; j < size; ++j)
			if (array[j] < array[min_index]) min_index = j;

		// Need to swap elements? If so, swap them
		if (array[i] != array[min_index]) {
			int tmp = array[i];
			array[i] = array[min_index];
			array[min_index] = tmp;
		}
	}
}
