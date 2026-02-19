import cv2
from PIL import Image
import os
import time

# ASCII characters used to build the output text
# From darkest to lightest
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width / 1.65  # Adjust for terminal character aspect ratio
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayify(image):
    grayscale_image = image.convert("L")
    return grayscale_image

def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    return characters

def main():
    # Initialize the camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("Live ASCII Video started. Press 'q' to quit.")
    
    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                break

            # Convert OpenCV image (BGR) to PIL image (RGB)
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # Process image
            new_width = 100
            image = resize_image(image, new_width)
            image = grayify(image)
            
            ascii_str = pixels_to_ascii(image)
            pixel_count = len(ascii_str)
            ascii_img = "\n".join([ascii_str[index:(index + new_width)] for index in range(0, pixel_count, new_width)])

            # Clear terminal and print using ANSI escape codes
            # \033[H moves cursor to top-left, \033[32m makes text green
            print("\033[H\033[32m" + ascii_img, end="")

            # Small delay to reduce CPU usage
            # time.sleep(0.01)

            # Check for 'q' key to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        # Release the capture and close windows
        cap.release()
        cv2.destroyAllWindows()
        print("\nExiting...")

if __name__ == "__main__":
    main()
