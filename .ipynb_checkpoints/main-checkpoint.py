import os
import numpy as np
from PIL import Image

def zoom_image(input_path, output_path, zoom_factor):
    input_image = Image.open(input_path)
    input_array = np.array(input_image)

    height, width, _ = input_array.shape
    new_height = int(height * zoom_factor)
    new_width = int(width * zoom_factor)
    output_array = np.zeros((new_height, new_width, 3), dtype=np.uint8)

    for y_out in range(new_height):
        for x_out in range(new_width):
            x_in = x_out / zoom_factor
            y_in = y_out / zoom_factor
            x1, y1 = int(x_in), int(y_in)
            x2, y2 = min(x1 + 1, width - 1), min(y1 + 1, height - 1)
            dx, dy = x_in - x1, y_in - y1

            for channel in range(3):
                interpolated_value = (1 - dx) * (1 - dy) * input_array[y1, x1, channel] + \
                                     dx * (1 - dy) * input_array[y1, x2, channel] + \
                                     (1 - dx) * dy * input_array[y2, x1, channel] + \
                                     dx * dy * input_array[y2, x2, channel]
                output_array[y_out, x_out, channel] = int(interpolated_value)

    output_image = Image.fromarray(output_array)
    output_image.save(output_path)
    return output_path

if __name__ == "__main__":
    input_image_path = "images/input_image.jpeg"
    output_image_path = "images/output_zoomed.png"

    zoom_factor = float(input("Enter the zoom factor (e.g., 2.0 for 2x zoom): "))
    zoom_image(input_image_path, output_image_path, zoom_factor)

    print(f"Zoomed image saved as {output_image_path}")
