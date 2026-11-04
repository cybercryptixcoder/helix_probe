
def approx_function(x):
    return x * (x - 5) * (x + 5)

input_values = [-128, 0, 128, -100, -50, -25, 25, 50, 100, -20, -10, -5, 5, 10, 20]
output_values = [approx_function(x) for x in input_values]
print(list(zip(input_values, output_values)))
