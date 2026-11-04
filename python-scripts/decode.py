import os
import re
from PIL import Image

# Configuration
header_file = "images.h"
output_folder = "output_images"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

def extract_arrays_from_header(header_path):
    with open(header_path, 'r') as f:
        content = f.read()

    pattern = r'const uint8_t (\w+)\[.*?\] = \{(.*?)\};'
    matches = re.findall(pattern, content, re.DOTALL)

    arrays = {}
    for var_name, array_data in matches:
        # Remove comments and whitespace
        clean_data = array_data.replace('\n', ' ').replace('\r', ' ')
        clean_data = re.sub(r'/\*.*?\*/', '', clean_data)  # Remove C-style comments
        clean_data = re.sub(r'//.*?\n', '', clean_data)  # Remove C++ style comments
        values = [int(val.strip()) for val in clean_data.split(',') if val.strip().isdigit()]
        arrays[var_name] = values

    return arrays

def save_image_from_array(array_data, filename, size=(32, 32)):
    if len(array_data) != size[0] * size[1] * 3:
        print(f"Error: Array length {len(array_data)} does not match expected image size.")
        return

    img = Image.new("RGB", size)
    pixels = [tuple(array_data[i:i+3]) for i in range(0, len(array_data), 3)]
    img.putdata(pixels)
    img.save(filename)
    print(f"Saved image: {filename}")

def convert_header_to_images():
    arrays = extract_arrays_from_header(header_file)

    for name, data in arrays.items():
        output_path = os.path.join(output_folder, f"{name}.png")
        save_image_from_array(data, output_path)

if __name__ == "__main__":
    convert_header_to_images()