import os
from PIL import Image

input_folder = "memes_input/"

# Iterate through all files in the input folder
for filename in os.listdir(input_folder):
    # Check if the file is a WebP image
    if filename.endswith(".webp"):
        # Construct the full paths for input and output
        webp_filepath = os.path.join(input_folder, filename)
        jpg_filepath = os.path.join(input_folder, os.path.splitext(filename)[0] + ".jpg")

        # Open the WebP image
        with Image.open(webp_filepath) as img:
            # Save the image as JPEG
            img.save(jpg_filepath, "JPEG")

        # Delete the original WebP file
        os.remove(webp_filepath)

if __name__ == "__main__":
    print("All WebP images in 'memes_input/' have been converted to JPEG.")