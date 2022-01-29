# Python RNG
import random
random.seed(42)

# Numpy RNG
import numpy as np
np.random.seed(42)

# TF RNG
from tensorflow.python.framework import random_seed
random_seed.set_seed(42)
