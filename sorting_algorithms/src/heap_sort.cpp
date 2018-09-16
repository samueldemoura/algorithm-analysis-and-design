#define FATHER(i) (i - 1)/2
#define LEFT_CHILD(i) (2 * i) + 1
#define RIGHT_CHILD(i) (2 * i) + 2

void max_heapify(int *heap, int heap_size, int i = 0) {
	if (i >= heap_size) {
		// This shouldn't happen, right? Check later.
	}

	int biggest = i;
	if (LEFT_CHILD(i) < heap_size && heap[LEFT_CHILD(i)] > heap[biggest])
		biggest = LEFT_CHILD(i);

	if (RIGHT_CHILD(i) < heap_size && heap[RIGHT_CHILD(i)] > heap[biggest])
		biggest = RIGHT_CHILD(i);

	if (biggest != i) {
		int tmp = heap[i];
		heap[i] = heap[biggest];
		heap[biggest] = tmp;

		max_heapify(heap, heap_size, biggest);
	}
}

void build_max_heap(int *heap, int heap_size) {
	for (int i = (heap_size / 2) - 1; i >= 0; --i)
		max_heapify(heap, heap_size, i);
}

void heap_sort(int *heap, int heap_size) {
	build_max_heap(heap, heap_size);

	for (int i = 0; i < heap_size; ++i) {
		max_heapify(heap, heap_size - i, 0);
		int tmp = heap[0];
		heap[0] = heap[heap_size - i - 1];
		heap[heap_size - i - 1] = tmp;
	}
}
