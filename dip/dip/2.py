from PIL import Image

def is_red(pixel):
    # Check if a pixel is red based on RGB values
    red_threshold = 200
    return pixel[0] > red_threshold and pixel[1] < 100 and pixel[2] < 100

def cast_rays(image, light_source):
    width, height = image.size
    shadow_color = (50, 50, 50)  # Color for shadowed pixels

    for x in range(width):
        for y in range(height):
            # Check if the pixel is red (blocker)
            if is_red(image.getpixel((x, y))):
                # Cast a ray from the pixel to the light source
                ray = (light_source[0] - x, light_source[1] - y)

                # Check for intersections with objects (not implemented in this basic example)
                # For simplicity, let's assume all rays hit the light source without obstruction
                # You might need a more sophisticated approach for real-world scenarios.

                # If the ray doesn't intersect with any object, consider the pixel in shadow
                image.putpixel((x, y), shadow_color)

    return image

def main():
    # Load the image
    input_image_path = "1.png"
    output_image_path = "output.png"
    image = Image.open(input_image_path)

    # Define the light source position (adjust based on your scene)
    light_source = (10, 10)

    # Cast rays and identify shadows
    result_image = cast_rays(image.copy(), light_source)

    # Save the result
    result_image.save(output_image_path)
    print(f"Result saved to {output_image_path}")

if __name__ == "__main__":
    main()

