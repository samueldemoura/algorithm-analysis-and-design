void insertion_sort(int *array, int size) {
	for (int i = 0; i < size; ++i) {
		for (int j = i; j > 0 && array[j-1] > array[j]; --j) {
			int tmp = array[j];
			array[j] = array[j-1];
			array[j-1] = tmp;
		}
	}
}
