"""
Purpose is to keep a check on the least recently used cache.

I used a dictionary where the key is used to access the value of the dictionary while the value
of the dictionary contains the pointer to the node in the doubly linked list which contains the
value of the cache that can be updated.

Reason to use the doubly linked list is to maintain the order of the cache , this way i can easily
detect the the least recentlu used cache (right before the tail node)

Reason to use a doubly linked list instead of a singly linked list is the direct access to the node
and deletion done in O(1) time

I imported time from the library to calculate the time of the cache and length of the capacity with
O function to get the space complexity

The current_size method returns the current number of items in the cache at any point in time. It helps
you understand how many items are currently stored in the cache.

The space_complexity method provides a theoretical understanding of how much space the cache could
potentially use based on its maximum capacity.

"""


from time import perf_counter

class ListNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer greater than 0.")
        self.capacity = capacity
        self.cache = {}
        self.head = ListNode(0, 0)  # Dummy head
        self.tail = ListNode(0, 0)  # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head
        self.accesses = 0  # Tracks the total number of get and put operations
        self.misses = 0   # Tracks the number of cache misses

    def _move_to_head(self, node: ListNode):
        """Move an existing node to the head of the doubly linked list."""
        self._remove(node)
        self._add_to_head(node)

    def _add_to_head(self, node: ListNode):
        """Add a new node right after the head."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _pop_tail(self) -> ListNode:
        """Remove and return the least recently used node (just before the tail)."""
        lru_node = self.tail.prev
        self._remove(lru_node)
        return lru_node

    def _remove(self, node: ListNode):
        """Detach a node from the doubly linked list."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def get(self, key: int) -> int:
        """Retrieve the value of the key if it exists, otherwise return -1."""
        start_time = perf_counter()  # Start timing
        self.accesses += 1  # Increment total accesses

        if key in self.cache:
            node = self.cache[key]
            self._move_to_head(node)
            elapsed_time = perf_counter() - start_time
            print(f"Get operation time: {elapsed_time:.6f} seconds")
            return node.value

        # Cache miss
        self.misses += 1
        elapsed_time = perf_counter() - start_time
        print(f"Get operation time: {elapsed_time:.6f} seconds")
        return -1

    def put(self, key: int, value: int):
        """Insert a new key-value pair or update an existing key-value pair."""
        self.accesses += 1
        start_time = perf_counter()  # Start timing

        if key in self.cache:
            # Update existing node
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            self.misses += 1
            # Insert new node
            new_node = ListNode(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)

            # Evict the least recently used node if capacity is exceeded
            if len(self.cache) > self.capacity:
                lru_node = self._pop_tail()
                del self.cache[lru_node.key]

        elapsed_time = perf_counter() - start_time
        print(f"Put operation time: {elapsed_time:.6f} seconds")

    def current_size(self) -> int:
        """Return the current number of items in the cache."""
        return len(self.cache)

    def miss_rate(self) -> float:
        """Calculate and return the cache miss rate."""
        if self.accesses == 0:
            return 0.0  # Avoid division by zero
        return (self.misses / self.accesses) * 100


# Example Usage
if __name__ == "__main__":
    cache = LRUCache(3)
    cache.put(1, 1)  # Insert 1
    cache.put(2, 2)  # Insert 2
    print(cache.get(1))  # Access 1 (Hit)
    cache.put(3, 3)  # Insert 3
    cache.put(4, 4)  # Insert 4 (Evicts 2)
    print(cache.get(2))  # Access 2 (Miss)
    print(cache.miss_rate())  # Print miss rate
