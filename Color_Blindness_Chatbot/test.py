import tkinter as tk
import webbrowser
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import os
import random


# Global variables
image_paths = []
image_labels = []
predictions = []
i = 0

# Function to read image paths based on dataset structure
def list_images(data_dir):
    categories = os.listdir(data_dir)
    image_paths = []
    for category in categories:
        category_path = os.path.join(data_dir, category)
        if os.path.isdir(category_path):
            for filename in os.listdir(category_path):
                if filename.endswith(".png"):
                    image_path = os.path.join(category_path, filename)
                    image_paths.append(image_path)
    return image_paths

# to start the test blind test
def start_test():
    global image_paths, image_labels, predictions, i

    # Clear previous results and shuffle image paths
    predictions = []
    image_labels = []
    i = 0
    random.shuffle(image_paths)

    # Load image labels from folder names
    image_labels = [os.path.basename(os.path.dirname(path)) for path in image_paths]

    start_button.pack_forget() # hiding start button

    quit_button.pack(side=tk.LEFT, padx=20, pady=20)  # display quit test

    input_frame.pack(side=tk.RIGHT, padx=20)  # display input frame for user input

    display_image()

# Method to display the image and accept user input
def display_image():
    global i, image_paths

    if i < len(image_paths):
        # Load and display image
        image = cv2.imread(image_paths[i])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        image_label.config(image=image)
        image_label.image = image

        input_field.delete(0, tk.END)  # clear input field for user's next input

        input_field.focus_set()  # set focus to the input field

    else:
        calculate_results()  # show finals results of test

# Method to handle user input
def get_prediction():
    global i, predictions

    # Get user input
    user_input = input_field.get()

    # Validate input
    if user_input.isdigit():
        predictions.append(int(user_input))
        i += 1
        display_image()
    else:
        messagebox.showerror("Error", "Invalid entry. Please enter a number.")
# redirects to webpage
def open_url(event):
    webbrowser.open_new("https://www.color-blind-test.com/")

# Method to show the results
def calculate_results():
    global predictions, image_labels

    predicted_labels_str = [str(pred) for pred in predictions]  # converting user predicted values to string

    # calculate accuracy based on actual and predicted vales
    correct_predictions = sum(1 for pred, label in zip(predicted_labels_str, image_labels) if pred == label)
    total_images = len(image_labels)
    accuracy = (correct_predictions / total_images) * 100

    if accuracy > 80:
        result = "Normal Color Vision (likely)"
    elif 50 < accuracy <= 80:
        result = "Possible Mild Color Blindness"
    elif accuracy <= 50:
        result = "Possible Moderate/Severe Color Blindness"
    show_results(accuracy,result)

# display results
def show_results(accuracy,result):

    # a new window for showing results
    results_window = tk.Toplevel(window)
    results_window.title("Test Results")

    # normal label
    normal_label = tk.Label(results_window, text=f"Accuracy: {accuracy:.2f}%\n\nResult: {result}")
    normal_label.pack()

    # label for the clickable link
    link_label = tk.Label(results_window, text="Click Here for more tests.", cursor="hand2", fg="blue")
    link_label.pack()

    # bind the function to the clickable link label
    link_label.bind("<Button-1>", open_url)

    # Quit button
    quit_button = tk.Button(results_window, text="Quit Test", command=confirm_quit, width=10, height=3)
    quit_button.pack(side=tk.LEFT, padx=20, pady=20)

#  confirm quitting the test
def confirm_quit():
    if messagebox.askyesno("Quit Test", "Are you sure you want to quit?"):
        window.destroy()

# Main window
window = tk.Tk()
window.title("Color Blindness Test")
window.geometry("800x600")

# Load image paths
data_dir = "dataset/ordered"  # Update with your dataset path
image_paths = list_images(data_dir)

# Start test button
start_button = tk.Button(window, text="Start Test", command=start_test, width=20, height=5)
start_button.place(relx=0.5, rely=0.5, anchor="center")

# Image display
image_label = tk.Label(window)
image_label.pack(side=tk.LEFT, padx=20)

# Text input field
input_frame = tk.Frame(window)
input_field = tk.Entry(input_frame, width=10)
input_field.pack(side=tk.TOP, padx=5, pady=5)
input_button = tk.Button(input_frame, text="Enter", command=get_prediction)
input_button.pack(side=tk.BOTTOM, padx=5, pady=5)

# Quit button
quit_button = tk.Button(window, text="Quit Test", command=confirm_quit, width=10, height=3)

window.mainloop()
