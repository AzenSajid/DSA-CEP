from Omar_CEP import LRUCache

def test_case():
    cache = LRUCache(50)

    for i in range(50):
        cache.put(i, i * 10) 

    print("Retrieving values for odd keys:")
    for i in range(1, 100, 2):
        value = cache.get(i)
        print(f"Key: {i}, Value: {value}")

    prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    print("\nFilling the cache with prime numbers:")
    for prime in prime_numbers:
        cache.put(prime, prime * 10) 

    final_miss_rate = cache.miss_rate()
    print(f"\nAccesses: {cache.accesses}, Misses: {cache.misses}")
    print(f"\nFinal Miss Rate: {final_miss_rate}%")

test_case()

