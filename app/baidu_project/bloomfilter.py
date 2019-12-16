from bloom_filter import BloomFilter
bloom = BloomFilter(max_elements=10000, error_rate=0.1)



a = 'test1-key' not in bloom
print(a)
# bloom.add("test1-key")
# a = 'test1-key' in bloom
# print('after', a)