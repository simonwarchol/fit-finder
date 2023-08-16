# import json
#
import numpy as np
from tqdm import tqdm
#
# # Input and output file paths
# input_file = "vectors.json"
# output_file = "indexed_vectors.json"
#
# # Load the input JSON file
# with open(input_file, "r") as file:
#     data = json.load(file)
#
#
# # Function to round a floating-point number to 5 decimal points
# def round_value(value):
#     return round(value, 4)
#
#
# vector_matrix = None
# i = 0
# # Process each vector in the JSON data
# for key in tqdm(data):
#     vector = np.array(data[key]["vector"])
#     # rounded_vector = [round_value(value) for value in vector]
#     data[key]["vector"] = i
#     if vector_matrix is None:
#         vector_matrix = vector
#     else:
#         vector_matrix = np.vstack((vector_matrix, vector))
#     i += 1
#
# # Save the updated data to the output file
# with open(output_file, "w") as file:
#     json.dump(data, file, indent=3)
#
# np.save("vector_matrix.npy", vector_matrix)
#
# print("New JSON file created:", output_file)
file = np.load("vector_matrix.npy")
np.save("vector_matrix.npy", file.astype(np.float32))
