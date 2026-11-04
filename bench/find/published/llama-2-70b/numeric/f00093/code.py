
import numpy as np
import matplotlib.pyplot as plt

# Define the structure of the neural network
n_inputs = 1
n_hidden = 16
n_outputs = 1

# Initialize the weights and biases for the neural network
weights = np.random.rand(n_inputs, n_hidden)
biases = np.zeros((n_hidden, 1))

# Define the sigmoid activation function
def sig