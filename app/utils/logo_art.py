import PIL.Image

# Define the ASCII characters to use
ASCII_CHARS = "@%#*+=-:. "


def resize_image(image, new_width=100):
    """Resize the image to a smaller width while maintaining aspect ratio."""
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image


def grayify(image):
    """Convert the image to grayscale."""
    return image.convert("L")


def pixels_to_ascii(image):
    """Map each pixel to an ASCII character."""
    pixels = image.getdata()
    # Ensure pixel values are in range 0-255 and properly scaled to ASCII_CHARS length
    ascii_str = "".join(
        ASCII_CHARS[min(int(pixel * len(ASCII_CHARS) / 256), len(ASCII_CHARS) - 1)]
        for pixel in pixels
    )
    return ascii_str


def image_to_ascii(image_path, new_width=100):
    """Convert the image at the given path to ASCII art."""
    try:
        image = PIL.Image.open(image_path).convert("L")  # Convert to grayscale
    except Exception as e:
        print(f"Error opening image: {e}")
        return None

    image = resize_image(image, new_width)
    ascii_str = pixels_to_ascii(image)

    # Format the ASCII string with line breaks
    img_width = image.width
    ascii_str_len = len(ascii_str)
    ascii_img = ""
    for i in range(0, ascii_str_len, img_width):
        ascii_img += ascii_str[i : i + img_width] + "\n"

    return ascii_img


# # Path to the image file
# image_path = "./eia_logo.png"
# # You can tweak the new_width parameter for finer or coarser results.
# ascii_art = image_to_ascii(image_path, new_width=50)

# Print the ASCII art
# if ascii_art:
#     print(ascii_art)
