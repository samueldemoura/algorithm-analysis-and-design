void merge(int *array, int low, int mid, int high) {
	int aux[high - low + 1];
	int i = 0;
	int l1 = low;
	int r1 = mid;
	int l2 = r1 + 1;
	int r2 = high;

	// Merge items in order
	while (l1 <= r1 && l2 <= r2) {
		if (array[l1] < array[l2])
			aux[i++] = array[l1++];
		else
			aux[i++] = array[l2++];
	}

	// Copy over remaining items
	while (l1 <= r1)
		aux[i++] = array[l1++];
	while (l2 <= r2)
		aux[i++] = array[l2++];

	// Copy over to the original input array
	for (int j = low; j <= high; ++j)
		array[j] = aux[j - low];
}

void merge_sort_inner(int *array, int low, int high) {
	if (low < high) {
		int mid = (low + high) / 2;
		merge_sort_inner(array, low, mid);
		merge_sort_inner(array, mid + 1, high);
		merge(array, low, mid, high);
	}
}

void merge_sort(int *array, int size) {
	merge_sort_inner(array, 0, size);
}
