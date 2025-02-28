import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os


class ImageLabelingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Labeling")

        # Main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas and scrollbars
        self.canvas = tk.Canvas(self.main_frame)
        self.v_scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.h_scrollbar = ttk.Scrollbar(self.main_frame, orient="horizontal", command=self.canvas.xview)

        # Configure canvas
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)

        # Grid layout
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Configure grid weights
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Button frame
        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(fill=tk.X)

        # Buttons
        self.rotate_btn = ttk.Button(self.button_frame, text="Rotate", command=lambda: self.process_image(1))
        self.grayscale_btn = ttk.Button(self.button_frame, text="Grayscale", command=lambda: self.process_image(3))
        self.save_btn = ttk.Button(self.button_frame, text="Save", command=self.save_images_and_data)

        self.rotate_btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.grayscale_btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.save_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Sliders for brightness and color adjustment
        self.slider_frame = ttk.Frame(root)
        self.slider_frame.pack(fill=tk.X, pady=10)

        self.brightness_label = ttk.Label(self.slider_frame, text="Brightness")
        self.brightness_label.pack(side=tk.LEFT, padx=5)

        self.brightness_slider = ttk.Scale(
            self.slider_frame, from_=-100, to=100, orient="horizontal", command=self.adjust_brightness
        )
        self.brightness_slider.set(0)
        self.brightness_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.image = None
        self.photo = None
        self.roi_start = None
        self.roi_end = None
        self.roi = None
        self.processed_image = None
        self.brightness_adjusted_image = None
        self.processed_data = []

        self.canvas.bind("<ButtonPress-1>", self.start_roi)
        self.canvas.bind("<B1-Motion>", self.draw_roi)
        self.canvas.bind("<ButtonRelease-1>", self.end_roi)

    def load_image(self, path):
        # Convert path format
        path = os.path.normpath(path)

        if not os.path.exists(path):
            print(f"Error: Image {path} not found!")
            return

        try:
            # Load image using PIL first (for webp support)
            pil_image = Image.open(path)
            # Convert to RGB if needed
            if pil_image.mode != "RGB":
                pil_image = pil_image.convert("RGB")

            # Convert PIL image to numpy array for OpenCV processing
            self.image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

            # Create PhotoImage for display
            self.photo = ImageTk.PhotoImage(pil_image)

            # Update canvas
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

            print("Image loaded successfully!")

        except Exception as e:
            print(f"Error loading image: {str(e)}")
            return

    def start_roi(self, event):
        self.roi_start = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.canvas.delete("roi")

    def draw_roi(self, event):
        if self.roi_start:
            self.canvas.delete("roi")
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)
            self.canvas.create_rectangle(
                self.roi_start[0], self.roi_start[1], x, y, outline="green", width=2, tags="roi"
            )

    def end_roi(self, event):
        self.roi_end = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.extract_roi()

    def extract_roi(self):
        if self.roi_start and self.roi_end and self.image is not None:
            x1, y1 = int(self.roi_start[0]), int(self.roi_start[1])
            x2, y2 = int(self.roi_end[0]), int(self.roi_end[1])

            # Ensure coordinates are within bounds
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)

            # Ensure coordinates don't exceed image dimensions
            height, width = self.image.shape[:2]
            x1, x2 = max(0, min(x1, width)), max(0, min(x2, width))
            y1, y2 = max(0, min(y1, height)), max(0, min(y2, height))

            # Get ROI from image
            self.roi = self.image[y1:y2, x1:x2].copy()

            # Show ROI in separate window
            cv2.imshow("Selected ROI", self.roi)

    def process_image(self, choice):
        if self.roi is None:
            print("Please select ROI first!")
            return

        if choice == 1:  # Rotate
            center = (self.roi.shape[1] // 2, self.roi.shape[0] // 2)
            matrix = cv2.getRotationMatrix2D(center, 45, 1.0)
            self.processed_image = cv2.warpAffine(self.roi, matrix, (self.roi.shape[1], self.roi.shape[0]))
        elif choice == 3:  # Grayscale
            gray = cv2.cvtColor(self.roi, cv2.COLOR_BGR2GRAY)
            self.processed_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        if self.processed_image is not None:
            cv2.imshow("Processed ROI", self.processed_image)

    def adjust_brightness(self, value):
        if self.roi is None:
            print("Please select ROI first!")
            return

        value = float(value)
        self.brightness_adjusted_image = cv2.convertScaleAbs(self.roi, alpha=1, beta=value)
        cv2.imshow("Brightness Adjusted ROI", self.brightness_adjusted_image)

    def save_images_and_data(self):
        if self.roi is None:
            print("No ROI selected!")
            return

        # Save augmented ROI images
        save_path = filedialog.askdirectory(title="Select Save Directory")
        if not save_path:
            return

        roi_path = os.path.join(save_path, "roi.jpg")
        normalized_path = os.path.join(save_path, "roi_normalized.jpg")
        standardized_path = os.path.join(save_path, "roi_standardized.jpg")
        data_file_path = os.path.join(save_path, "processed_data.txt")

        # Save ROI
        cv2.imwrite(roi_path, self.roi)

        # Normalize and save
        normalized = self.roi / 255.0
        cv2.imwrite(normalized_path, (normalized * 255).astype(np.uint8))

        # Standardize and save
        mean, std = self.roi.mean(), self.roi.std()
        standardized = (self.roi - mean) / (std if std > 0 else 1)
        cv2.imwrite(standardized_path, np.clip((standardized * 127 + 127), 0, 255).astype(np.uint8))

        # Save data
        with open(data_file_path, "w") as file:
            file.write(f"ROI: {self.roi.size}\n")
            file.write(" ".join(map(str, self.roi.flatten())) + "\n")
            file.write(f"Normalized: {normalized.size}\n")
            file.write(" ".join(map(str, normalized.flatten())) + "\n")
            file.write(f"Standardized: {standardized.size}\n")
            file.write(" ".join(map(str, standardized.flatten())) + "\n")

        print(f"Saved images and data to {save_path}")


def main():
    root = tk.Tk()
    app = ImageLabelingApp(root)
    app.load_image(r"D:\One pice\ddd.webp")
    root.mainloop()


if __name__ == "__main__":
    main()
