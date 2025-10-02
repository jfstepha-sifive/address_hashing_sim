import numpy as np
import sys

if __name__ == "__main__":
    data_bits = int(sys.argv[1])
    print(f"generating {1<<data_bits} cases")
    rng = np.random.default_rng()
    dataRange = rng.permutation(1<<data_bits)
    print("done.")