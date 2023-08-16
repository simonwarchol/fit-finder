#!/bin/bash

# Input and output file paths
input_file="vectors.json"
output_file="rounded_vectors.json"

# Read the input JSON file
data=$(cat "$input_file")

# Function to round a floating-point number to 5 decimal points
function round {
    printf "%.5f" "$1"
}

# Process each vector in the JSON data
new_data=$(echo "$data" | jq '. | to_entries | map_values(.value.vector |= map(map(round)))')

# Save the updated data to the output file
echo "$new_data" > "$output_file"

echo "New JSON file created: $output_file"