int partition(int *array, int low, int high) {
	int pivot = array[high]; // Pivot is rightmost element at first

	int j = low - 1;
	for (int i = low; i < high; ++i) {
		if (array[i] < pivot) {
			++j;
			int tmp = array[i];
			array[i] = array[j];
			array[j] = tmp;
		}
	}

	int tmp = array[j+1];
	array[j+1] = array[high];
	array[high] = tmp;

	return j + 1;
}

void quick_sort_inner(int *array, int low, int high) {
	if (low < high) {
		int part = partition(array, low, high);
		quick_sort_inner(array, low, part - 1);
		quick_sort_inner(array, part + 1, high);
	}
}

void quick_sort(int *array, int size) {
	quick_sort_inner(array, 0, size - 1);
}
