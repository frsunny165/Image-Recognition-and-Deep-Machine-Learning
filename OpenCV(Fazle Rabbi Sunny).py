import numpy as np
import cv2

# Create a black image of size 400x400 with 3 color channels (RGB) and set all pixels to white (255)
img = np.ones((400, 400, 3), np.uint8) * 255

# Draw a red ellipse (outer part) at (190, 80) with axes lengths (60, 60), rotated 120 degrees,
# covering an angle of 0 to 300 degrees, and filled (-1 thickness)
img = cv2.ellipse(img, (190, 80), (60, 60), 120, 0, 300, (0, 0, 255), -1)

# Draw a smaller white ellipse (inner part) within the red one
img = cv2.ellipse(img, (190, 80), (20, 20), 120, 0, 300, (255, 255, 255), -1)

# Draw a green ellipse (outer part) at (116, 200) with axes lengths (60, 60), rotated 0 degrees,
# covering an angle of 0 to 300 degrees, and filled
img = cv2.ellipse(img, (116, 200), (60, 60), 0, 0, 300, (0, 255, 0), -1)

# Draw a smaller white ellipse (inner part) within the green one
img = cv2.ellipse(img, (116, 200), (20, 20), 0, 0, 300, (255, 255, 255), -1)

# Draw a blue ellipse (outer part) at (260, 200) with axes lengths (60, 60), rotated 300 degrees,
# covering an angle of 0 to 300 degrees, and filled
img = cv2.ellipse(img, (260, 200), (60, 60), 300, 0, 300, (255, 0, 0), -1)

# Draw a smaller white ellipse (inner part) within the blue one
img = cv2.ellipse(img, (260, 200), (20, 20), 300, 0, 300, (255, 255, 255), -1)

# Define font type for text
font = cv2.FONT_HERSHEY_SIMPLEX

# Add the text "OpenCV" at position (20, 350), with font size 3, black color (0, 0, 0),
# thickness of 8, and anti-aliased edges
cv2.putText(img, "OpenCV", (20, 350), font, 3, (0, 0, 0), 8, cv2.LINE_AA)

# Display the created image in a window titled 'My first img show'
cv2.imshow('My first img show', img)

cv2.waitKey(0)
