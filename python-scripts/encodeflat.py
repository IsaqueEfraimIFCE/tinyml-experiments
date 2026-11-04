import os
from PIL import Image

# Config
input_folder = "cifar10"  # Folder with 32x32 RGB images
output_header = "images.h"
image_size = (32, 32)  # 32x32 pixels
channels = 3           # RGB

def image_to_flat_array(image_path):
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img = img.resize(image_size)
        pixels = list(img.getdata())
        flat_pixels = [value for pixel in pixels for value in pixel]
        return flat_pixels

def generate_header():
    all_data = []
    image_count = 0

    for filename in sorted(os.listdir(input_folder)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            path = os.path.join(input_folder, filename)
            print(f"Adding {filename} to header...")
            img_data = image_to_flat_array(path)
            all_data.extend(img_data)
            image_count += 1

    header = "#ifndef IMAGES_H\n#define IMAGES_H\n\n#include <stdint.h>\n\n"
    header += f"#define IMAGE_COUNT {image_count}\n\n"
    header += f"const uint8_t image_data[{len(all_data)}] = {{\n"

    for i in range(0, len(all_data), 12):
        chunk = ", ".join(f"{val:3}" for val in all_data[i:i+12])
        header += f"    {chunk},\n"

    header += "};\n\n#endif // IMAGES_H\n"

    with open(output_header, "w") as f:
        f.write(header)

    print(f"\nHeader written to {output_header} with {image_count} image(s).")

if __name__ == "__main__":
    generate_header()