import csv
import json

# Input JSONL file path
input_file = 'rumah123_sale_properties.jsonl'

# Output CSV file path
output_file = 'rumah123_sale_properties.csv'

# Read the JSONL file and collect all keys dynamically
data = []
fieldnames = set()  # To collect all unique keys

with open(input_file, 'r', encoding='utf-8') as jsonl_file:
    for line in jsonl_file:
        json_obj = json.loads(line.strip())  # Parse each line as JSON
        data.append(json_obj)  # Add the JSON object to the list
        fieldnames.update(json_obj.keys())  # Collect keys

fieldnames = list(fieldnames)  # Convert the set of keys to a list

# Write the data to a CSV file
with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()  # Write the column headers
    writer.writerows(data)  # Write all rows

print(f"Data has been successfully written to {output_file}")