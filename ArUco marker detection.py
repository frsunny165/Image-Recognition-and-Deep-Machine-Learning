import cv2
import numpy as np
from cv2 import aruco
import os
from tkinter import Tk, filedialog

# Helper Functions

# Function to generate ArUco markers and save them as images
def generate_aruco_markers():
    try:
        aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)  # Predefined dictionary for 6x6 ArUco markers
        marker_size = 200  # Marker size in pixels

        os.makedirs('markers', exist_ok=True)  # Create a folder to save markers

        for i in range(4):  # Generate 4 markers
            marker_image = aruco.drawMarker(aruco_dict, i, marker_size)  # Draw marker
            cv2.imwrite(f'markers/marker_{i}.png', marker_image)  # Save marker as an image
        print("Successfully generated ArUco markers")
        return True
    except Exception as e:
        print(f"Error generating ArUco markers: {str(e)}")
        return False

# Function to detect ArUco markers in a given frame
def detect_markers(frame):
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert frame to grayscale
        aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)  # Predefined dictionary for detection
        parameters = aruco.DetectorParameters()  # Detection parameters
        detector = aruco.ArucoDetector(aruco_dict, parameters)  # ArUco detector
        corners, ids, rejected = detector.detectMarkers(gray)  # Detect markers
        return corners, ids
    except Exception as e:
        print(f"Error detecting markers: {str(e)}")
        return None, None

# Function to apply filters to the frame
def apply_filters(frame, filter_type):
    try:
        if filter_type == 'grayscale':
            return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
        elif filter_type == 'blur':
            return cv2.GaussianBlur(frame, (5, 5), 0)  # Apply Gaussian blur
        elif filter_type == 'edge':
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return cv2.Canny(gray, 100, 200)  # Apply edge detection
        elif filter_type == 'sharpen':
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])  # Sharpening kernel
            return cv2.filter2D(frame, -1, kernel)  # Apply sharpening filter
        return frame
    except Exception as e:
        print(f"Error applying filter {filter_type}: {str(e)}")
        return frame

# Function to save the output frame to a file
def save_output(frame):
    try:
        Tk().withdraw()  # Hide the root Tkinter window
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg"),
            ("All files", "*.*")
        ])
        if file_path:
            cv2.imwrite(file_path, frame)  # Save the frame to the selected file
            print(f"Frame saved to {file_path}")
    except Exception as e:
        print(f"Error saving output: {str(e)}")

# GUI Classes

# Class for button objects
class Button:
    def __init__(self, x, y, width, height, text, action):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action = action  # Function to execute when the button is clicked

    # Check if the button was clicked
    def is_clicked(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height

    # Draw the button on the frame
    def draw(self, img, color=(200, 200, 200), text_color=(0, 0, 0)):
        cv2.rectangle(img, (self.x, self.y), (self.x + self.width, self.y + self.height), color, -1)
        cv2.rectangle(img, (self.x, self.y), (self.x + self.width, self.y + self.height), (0, 0, 0), 1)

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        thickness = 1
        text_size = cv2.getTextSize(self.text, font, font_scale, thickness)[0]
        text_x = self.x + (self.width - text_size[0]) // 2
        text_y = self.y + (self.height + text_size[1]) // 2

        cv2.putText(img, self.text, (text_x, text_y), font, font_scale, text_color, thickness)

# Class for the GUI interface
class GUI:
    def __init__(self):
        self.buttons = []  # List of buttons
        self.current_filter = None  # Currently applied filter
        self.should_quit = False  # Flag to indicate quitting the application
        self.save_action = False  # Flag for saving frame
        self.transformed_frame = None  # Transformed frame after applying filters
        self.setup_buttons()  # Initialize buttons

    # Setup buttons with their positions and actions
    def setup_buttons(self):
        button_width = 150
        button_height = 30
        margin = 10
        x, y = margin, margin

        # Add filter buttons
        self.buttons.append(Button(x, y, button_width, button_height, "Grayscale", lambda: self.set_filter('grayscale')))
        x += button_width + margin
        self.buttons.append(Button(x, y, button_width, button_height, "Blur", lambda: self.set_filter('blur')))
        x += button_width + margin
        self.buttons.append(Button(x, y, button_width, button_height, "Edge Detection", lambda: self.set_filter('edge')))
        x += button_width + margin
        self.buttons.append(Button(x, y, button_width, button_height, "Sharpen", lambda: self.set_filter('sharpen')))

        # Add control buttons
        x = margin
        y += button_height + margin
        self.buttons.append(Button(x, y, button_width, button_height, "Save Frame", self.save_frame))
        x += button_width + margin
        self.buttons.append(Button(x, y, button_width, button_height, "Quit", self.quit))

    # Draw all buttons on the frame
    def draw_buttons(self, frame):
        for button in self.buttons:
            button.draw(frame)

    # Handle mouse click events
    def handle_click(self, x, y, frame):
        for button in self.buttons:
            if button.is_clicked(x, y):
                if button.text == "Save Frame":
                    self.save_frame()
                else:
                    button.action()

    # Set the current filter
    def set_filter(self, filter_type):
        self.current_filter = filter_type
        print(f"Filter set to: {filter_type}")

    # Save the current transformed frame
    def save_frame(self):
        if self.transformed_frame is not None:
            save_output(self.transformed_frame)

    # Quit the application
    def quit(self):
        self.should_quit = True

# Main function to run the application
def main():
    cap = cv2.VideoCapture(0)  # Open the default camera
    if not cap.isOpened():
        print("Error: Could not open camera")
        return

    gui = GUI()  # Initialize GUI

    try:
        while not gui.should_quit:
            ret, frame = cap.read()  # Capture frame from camera
            if not ret:
                print("Failed to grab frame")
                break

            display_frame = frame.copy()  # Create a copy for display

            # Apply the selected filter
            if gui.current_filter:
                display_frame = apply_filters(display_frame, gui.current_filter)
                gui.transformed_frame = display_frame

            # Draw GUI buttons
            gui.draw_buttons(display_frame)

            cv2.imshow('Camera Feed', display_frame)  # Show the camera feed with GUI

            # Handle mouse click events
            def mouse_event(event, x, y, flags, param):
                if event == cv2.EVENT_LBUTTONDOWN:
                    gui.handle_click(x, y, frame)

            cv2.setMouseCallback('Camera Feed', mouse_event)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # Quit if 'q' is pressed
                break
    finally:
        cap.release()  # Release the camera
        cv2.destroyAllWindows()  # Close all OpenCV windows

if __name__ == '__main__':
    main()
