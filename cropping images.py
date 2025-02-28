import cv2

def crop_with_roi(image_path, save_path, data_file):
    
    # Load the image
    image = cv2.imread("D:\One pice\ddd.webp")
    if image is None:
        print("Error: Unable to load the image.")
        return

    # Display instructions
    print("Instructions:")
    print("1. Select the region of interest (ROI) by clicking and dragging.")
    print("2. Press Enter or Space to confirm the selection.")
    print("3. Press 'c' to cancel and retry.")

    # Select ROI
    roi = cv2.selectROI("Select ROI", image, showCrosshair=True, fromCenter=False)

    # If ROI is valid
    if roi != (0, 0, 0, 0):
        x, y, w, h = map(int, roi)  # ROI coordinates
        cropped_image = image[y:y+h, x:x+w]  # Crop the image

        # Save the cropped image
        cv2.imwrite(save_path, cropped_image)
        print(f"Cropped image saved to: {save_path}")

        # Save ROI coordinates to the data file
        with open(data_file, 'w') as file:
            file.write(f"ROI Coordinates: x={x}, y={y}, w={w}, h={h}\n")
        print(f"ROI coordinates saved to: {data_file}")

        # Show the cropped image
        cv2.imshow("Cropped Image", cropped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No valid ROI selected. Exiting.")

    cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    input_image = "input.jpg"  # Replace with your input image path
    output_image = "cropped_image.jpg"  # Replace with your desired output path
    output_data_file = "roi_data.txt"  # Replace with your desired ROI data file path
    crop_with_roi(input_image, output_image, output_data_file)
