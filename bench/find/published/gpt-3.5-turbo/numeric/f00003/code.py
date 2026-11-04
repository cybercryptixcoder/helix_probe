
import numpy as np

def f(x):
    # Coefficients for the polynomial curve
    coeffs = [3.0, -2.5, 1.2, -0.3]
    
    # Compute the value of the polynomial curve
    y = np.polyval(coeffs, x)
    
    return y

# Test the function on a range of values
x_values = np.linspace(-128, 128, num=100)
output_values = f(x_values)

# Print the output values
print(output_values)
