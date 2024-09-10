from ultralytics import YOLO
import cv2
import os

def detect_and_process_license_plate_from_folder(folder_path, output_file):
    license_plate_detector = YOLO('license_plate_detector.pt')

    # Check if the folder path exists
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder path specified does not exist: {folder_path}")

    # Get the list of image files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('jpg', 'jpeg', 'png'))]

    correct_count = 0
    incorrect_count = 0

    with open(output_file, 'w') as f:
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            frame = cv2.imread(image_path)

            if frame is not None:
                # Detect license plate and process the image
                results = license_plate_detector(frame)[0]
                license_plates = results.boxes.data.tolist()
                if license_plates:
                    correct_count += 1
                else:
                    incorrect_count += 1

    # Calculate statistics
    total_detected = correct_count + incorrect_count
    correct_percentage = (correct_count / total_detected) * 100 if total_detected else 0
    incorrect_percentage = (incorrect_count / total_detected) * 100 if total_detected else 0

    # Write summary to the output file
    with open(output_file, 'a') as f:
        f.write(f"Bien so {correct_count} ({correct_percentage:.2f}%)\n")
        f.write(f"Khong bien: {incorrect_count} ({incorrect_percentage:.2f}%)\n")

# Test the function
if __name__ == "__main__":
    folder_path = "E:/TTTN/Plate_Recognize/BienSo"  # Replace with the path to your folder containing images
    output_file = "ketqua3.txt"
    detect_and_process_license_plate_from_folder(folder_path, output_file)
