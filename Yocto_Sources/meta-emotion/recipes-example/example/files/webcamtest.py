import cv2

# Set up video capture
cap = cv2.VideoCapture(0)  # 0 represents the first available camera

# Check if camera opened successfully
if not cap.isOpened():
    print("Failed to open camera")
    exit()

# Read frame from camera
ret, frame = cap.read()

if not ret:
    print("Failed to capture frame")
    exit()

# Release the video capture
cap.release()

# Save the frame as an image file
image_path = "captured_image.jpg"
cv2.imwrite(image_path, frame)

print("Image saved successfully:", image_path)

