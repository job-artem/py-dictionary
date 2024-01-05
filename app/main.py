class Dictionary:
    def __init__(self, initial_capacity=16, load_factor=0.75):
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets = [None] * self.capacity

    def _hash(self, key):
        return hash(key) % self.capacity

    def _resize(self):
        new_capacity = self.capacity * 2
        new_buckets = [None] * new_capacity

        # Rehash existing key-value pairs into the new buckets
        for bucket in self.buckets:
            if bucket is not None:
                for key, value in bucket:
                    new_index = hash(key) % new_capacity
                    new_bucket = new_buckets[new_index]

                    if new_bucket is None:
                        new_buckets[new_index] = [(key, value)]
                    else:
                        new_bucket.append((key, value))

        self.capacity = new_capacity
        self.buckets = new_buckets

    def __len__(self):
        return self.size

    def __setitem__(self, key, value):
        index = self._hash(key)
        bucket = self.buckets[index]

        if bucket is None:
            # No collision, create a new bucket
            self.buckets[index] = [(key, value)]
        else:
            # Check if the key already exists in the bucket
            for i, (existing_key, _) in enumerate(bucket):
                if existing_key == key:
                    # Key already exists, update the value
                    bucket[i] = (key, value)
                    break
            else:
                # Key doesn't exist, add a new key-value pair to the bucket
                bucket.append((key, value))
        self.size += 1

        # Check if the load factor exceeds the threshold, and resize if necessary
        if self.size > self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]

        if bucket is not None:
            for existing_key, value in bucket:
                if existing_key == key:
                    return value

        raise KeyError(f"Key '{key}' not found")
