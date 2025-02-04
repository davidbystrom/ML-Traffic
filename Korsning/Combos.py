import itertools

# Define the characters to use for combinations
letters = ['G', 'r', 'y']

# Generate all combinations of length 6
combinations = [''.join(comb) for comb in itertools.product(letters, repeat=6)]

# Display the list of combinations
print(combinations)