import cv2
import numpy as np

# Global variables
drawing = False  # True if the mouse is being dragged
mode = 'rectangle'  # Default drawing mode: rectangle
start_x, start_y = -1, -1  # Starting coordinates for shapes
image = np.zeros((600, 800, 3), dtype=np.uint8)  # Create a black image
text = "OpenCV"  # Default text for text mode

# Mouse callback function to handle drawing logic
def draw(event, x, y, flags, param):
    global start_x, start_y, drawing, mode, image

    # When the left mouse button is pressed, start drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_x, start_y = x, y

    # When the mouse is moved while the button is pressed, draw on a temporary image
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            temp_image = image.copy()  # Use a temporary image to avoid altering the original
            if mode == 'rectangle':
                # Draw a rectangle from start point to current mouse position
                cv2.rectangle(temp_image, (start_x, start_y), (x, y), (0, 255, 0), 2)
            elif mode == 'circle':
                # Draw a circle with radius based on distance from the start point
                radius = int(((x - start_x) ** 2 + (y - start_y) ** 2) ** 0.5)
                cv2.circle(temp_image, (start_x, start_y), radius, (255, 0, 0), 2)
            # Show the temporary image
            cv2.imshow('Interactive Drawing', temp_image)

    # When the left mouse button is released, finalize the drawing on the original image
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == 'rectangle':
            cv2.rectangle(image, (start_x, start_y), (x, y), (0, 255, 0), 2)
        elif mode == 'circle':
            radius = int(((x - start_x) ** 2 + (y - start_y) ** 2) ** 0.5)
            cv2.circle(image, (start_x, start_y), radius, (255, 0, 0), 2)
        elif mode == 'text':
            # Draw text at the release position
            cv2.putText(image, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
        # Show the updated image
        cv2.imshow('Interactive Drawing', image)

# Main function for the interactive drawing application
def interactive_drawing():
    global mode, text

    # Create a window and set a mouse callback for drawing
    cv2.namedWindow('Interactive Drawing')
    cv2.setMouseCallback('Interactive Drawing', draw)

    # Print available controls for the user
    print("Keyboard controls:")
    print("r - switch to rectangle mode")
    print("c - switch to circle mode")
    print("t - switch to text mode")
    print("q - quit the application")

    while True:
        # Display the image in the window
        cv2.imshow('Interactive Drawing', image)
        key = cv2.waitKey(1) & 0xFF  # Wait for a key press

        if key == ord('r'):
            mode = 'rectangle'  # Switch to rectangle mode
            print("Mode: Rectangle")
        elif key == ord('c'):
            mode = 'circle'  # Switch to circle mode
            print("Mode: Circle")
        elif key == ord('t'):
            mode = 'text'  # Switch to text mode
            text = input("Enter text to add: ")  # Get custom text from user
            print("Mode: Text")
        elif key == ord('q'):
            break  # Exit the application

    # Close all OpenCV windows
    cv2.destroyAllWindows()

# Entry point of the program
if __name__ == "__main__":
    interactive_drawing()
