import json
import os

def extract_data(json_file, output_file):
  """
  Extracts all keys and values from a JSON website dump and writes them to a text file.

  Args:
    json_file: Path to the JSON file containing the website dump.
    output_file: Path to the text file where the extracted data will be written.
  """

  with open(json_file, 'r') as f:
    data = json.load(f)

  with open(output_file, 'w') as f:
    for item in data:
      # Loop through each item in the data
      for key, value in item.items():
        # Extract all key-value pairs
        f.write(f"{key}: {value}\n")

# Example usage
json_file = os.environ['JSON_PATH']
output_file = "extracted_data.txt"

extract_data(json_file, output_file)

print(f"Data extracted from {json_file} and written to {output_file}")
