class Dictionary:
    def __init__(self, initial_capacity=8, load_factor=2/3):
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets = [None] * self.capacity

    def __setitem__(self, key, value):
        hash_value = self._hash(key)
        index = hash_value % self.capacity
        node = self.buckets[index]

        if node is None:
            # No collision, create a new node
            self.buckets[index] = [(key, hash_value, value)]
        else:
            # Check if the key already exists in the node
            for i, (existing_key, _, _) in enumerate(node):
                if existing_key == key:
                    # Key already exists, update the value
                    node[i] = (key, hash_value, value)
                    break
            else:
                # Key doesn't exist, add a new node to the bucket
                node.append((key, hash_value, value))

        self.size += 1

        # Check if the load factor exceeds the threshold, and resize if necessary
        if self.size > self.capacity * self.load_factor:
            self._resize()

    def __getitem__(self, key):
        hash_value = self._hash(key)
        index = hash_value % self.capacity
        node = self.buckets[index]

        if node is not None:
            for existing_key, existing_hash, value in node:
                if existing_key == key:
                    # Check if the hash values match to avoid false positives
                    if hash_value == existing_hash:
                        return value

        raise KeyError(f"Key '{key}' not found")

    def __len__(self):
        return self.size

    def _hash(self, key):
        return hash(key)

    def _resize(self):
        new_capacity = self.capacity * 2
        new_buckets = [None] * new_capacity

        # Rehash existing key-value pairs into the new buckets
        for bucket in self.buckets:
            if bucket is not None:
                for key, hash_value, value in bucket:
                    new_index = hash_value % new_capacity
                    new_node = new_buckets[new_index]

                    if new_node is None:
                        new_buckets[new_index] = [(key, hash_value, value)]
                    else:
                        new_node.append((key, hash_value, value))

        self.capacity = new_capacity
        self.buckets = new_buckets
