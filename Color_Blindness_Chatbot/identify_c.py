import numpy as np
import cv2


# Function to detect the color of the object being shown by the user
def detect_object_color(imageFrame, lower, upper, color_name):
    # Convert the imageFrame to HSV color space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # Create a mask for the specified color
    mask = cv2.inRange(hsvFrame, lower, upper)

    # Morphological operations (Dilation with smaller kernel)
    kernel = np.ones((3, 3), "uint8")
    mask = cv2.dilate(mask, kernel)

    # find contours for the specified color
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # check if contours were found
    if contours:
        # find the largest contour
        max_contour = max(contours, key=cv2.contourArea)

        # bounding box coordinates of the largest contour
        x, y, w, h = cv2.boundingRect(max_contour)

        # rectangle around the object if it falls within the defined color boundaries
        if 0 < x < boundary_left and 0 < y < boundary_top:
            color = (255, 255, 255)  # White color
            if color_name == "red":
                color = (0, 0, 255)  # Red color
            elif color_name == "green":
                color = (0, 255, 0)  # Green color
            elif color_name == "blue":
                color = (255, 0, 0)  # Blue color
            elif color_name == "yellow":
                color = (0, 255, 255)  # Yellow color
            elif color_name == "black":
                color = (0, 0, 0)  # Black color
            elif color_name == "white":
                color = (255, 255, 255)  # White color
            elif color_name == "brown":
                color = (139, 69, 19)  # Brown color
            elif color_name == "maroon":
                color = (128, 0, 0)  # Maroon color
            elif color_name == "grey":
                color = (128, 128, 128)  # Grey color
            elif color_name == "orange":
                color = (255, 165, 0)  # Orange color
            elif color_name == "pink":
                color = (255, 192, 203)  # Pink color

            cv2.rectangle(imageFrame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(imageFrame, color_name + " Object", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)

    # point indicating the location for the user to place the object
    cv2.circle(imageFrame, (point_x, point_y), 5, (0, 0, 0), -1)

    return imageFrame


# capturing video through webcam
webcam = cv2.VideoCapture(0)

# boundaries for left and top sides of the frame
boundary_left = 200
boundary_top = 200

# coordinates of the point where the user should place the object
point_x = 100
point_y = 100

while True:
    # read the video from the webcam
    _, imageFrame = webcam.read()

    # color ranges for each color of interest (narrowed a bit)
    colors = {
        "red": ([160, 100, 100], [170, 255, 255]),  # red range
        "green": ([29, 52, 72], [100, 255, 255]),  # green range
        "blue": ([94, 80, 2], [120, 255, 255]),  # blue range
        "yellow": ([20, 100, 100], [30, 255, 255]),  # yellow range
        "black": ([0, 0, 0], [180, 255, 30]),  # black range
        "white": ([0, 0, 200], [180, 30, 255]),  # white range
        "brown": ([10, 50, 50], [20, 255, 255]),  # brown range
        "maroon": ([0, 100, 100], [10, 255, 255]),  # maroon range
        "grey": ([0, 0, 100], [180, 30, 200]),  # grey range
        "orange": ([5, 100, 100], [15, 255, 255]),  # orange range
        "pink": ([150, 100, 100], [160, 255, 255]),  # pink range
    }

    # detect the color of the object shown by the user for each color
    for color_name, (lower, upper) in colors.items():
        imageFrame = detect_object_color(imageFrame, np.array(lower), np.array(upper), color_name)

    # display the image frame
    cv2.imshow("Object Color Detection in Real-Time", imageFrame)

    # 'q' key to quit the program
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# release the webcam and close all windows
webcam.release()
cv2.destroyAllWindows()
