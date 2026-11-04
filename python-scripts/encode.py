import os
from PIL import Image

# Configuration
input_folder = "cifar10"  # Folder containing 32x32 RGB images
output_header = "images.h"

def image_to_c_array(image_path):
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img = img.resize((32, 32))
        pixels = list(img.getdata())
        flat_pixels = [value for pixel in pixels for value in pixel]
        return flat_pixels

def format_c_array(data, var_name):
    c_array = f"const uint8_t {var_name}[32 * 32 * 3] = {{\n"
    for i in range(0, len(data), 12):
        line = ", ".join(f"{val:3}" for val in data[i:i+12])
        c_array += f"    {line},\n"
    c_array += "};\n\n"
    return c_array

def generate_header():
    header_content = "#ifndef IMAGES_H\n#define IMAGES_H\n\n#include <stdint.h>\n\n"
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            name = os.path.splitext(filename)[0]
            var_name = f"img_{name.replace('-', '_').replace(' ', '_')}"
            print(f"Processing {filename} -> {var_name}")
            img_data = image_to_c_array(os.path.join(input_folder, filename))
            header_content += format_c_array(img_data, var_name)

    header_content += "#endif // IMAGES_H\n"

    with open(output_header, "w") as f:
        f.write(header_content)
    print(f"\nHeader file written to {output_header}")

if __name__ == "__main__":
    generate_header()