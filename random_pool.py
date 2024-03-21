import np
from scipy.stats import entropy


class RandomPool:
    pool = []

    def hash_to_binary(self, hash_str):
        """Convert hex hash to binary."""
        return bin(int(hash_str, 16))[2:].zfill(256)

    def add_to_pool(self, hash_str):
        """Add binary hash to the pool."""
        binary_hash = self.hash_to_binary(hash_str)
        self.pool.append(binary_hash)

    def pool_entropy(self):
        """Estimate the entropy of the pool."""
        bit_string = ''.join(self.pool)
        bit_counts = [bit_string.count('0'), bit_string.count('1')]
        return entropy(bit_counts, base=2)

    def assess_randomness(self):
        """A simple uniformity check on the pool's distribution of 0s and 1s."""
        bit_string = ''.join(self.pool)
        zeros = bit_string.count('0')
        ones = bit_string.count('1')
        total_bits = len(bit_string)
        p_zeros = zeros / total_bits
        p_ones = ones / total_bits
        return abs(p_zeros - 0.5) < 0.05 and abs(p_ones - 0.5) < 0.05

    def generate_sample_and_remove(self, min_val = 0, max_val = 1):
        max_value = 2 ** 256 - 1
        """Generate a sample from the pool uniformly and remove the used hash."""
        if not self.pool:
            raise ValueError("The pool is empty.")
        index = np.random.randint(0, len(self.pool))
        selected_hash = self.pool.pop(index)
        # Convert binary back to int for the sample, or perform another desired operation
        sample = int(selected_hash, 2)
        normalized_value = sample / max_value

        scaled_value = (normalized_value*(max_val - min_val)) + min_val
        return scaled_value
