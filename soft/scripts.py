from ultralytics import YOLO
import cv2
import os
from read import detect_license_plate

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
                for license_plate in license_plates:
                    x1, y1, x2, y2, score, class_id = license_plate

                    license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]

                    # Convert the cropped license plate image to grayscale and apply threshold
                    license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                    license_plate_crop_gray_thresh = cv2.threshold(license_plate_crop_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

                    # Save the processed license plate image to a temporary file
                    temp_filename = 'temp_license_plate.jpg'
                    cv2.imwrite(temp_filename, license_plate_crop_gray_thresh)

                    # Use the detect_license_plate function to read the license plate from the processed image
                    license_plate_text = detect_license_plate(temp_filename)
                    result_text = f"License plate from {image_file}: {license_plate_text}"
                    print(result_text)

                    # Compare detected license plate with the image file name
                    if license_plate_text in image_file:
                        correct_count += 1
                    else:
                        incorrect_count += 1
    #f.write(f"{image_file}: {license_plate_text} - {'T' if correct_count else 'F'}\n")
    # Calculate statistics
    total_detected = correct_count + incorrect_count
    correct_percentage = (correct_count / total_detected) * 100 if total_detected else 0
    incorrect_percentage = (incorrect_count / total_detected) * 100 if total_detected else 0

    # Write summary to the output file
    with open(output_file, 'a') as f:
        f.write(f"Dung {correct_count} ({correct_percentage:.2f}%)\n")
        f.write(f"Sai: {incorrect_count} ({incorrect_percentage:.2f}%)\n")
    # Write result for each image to the output file
    
    
# Test the function
if __name__ == "__main__":
    folder_path = "E:/TTTN/Plate_Recognize/BienSo"  # Replace with the path to your folder containing images
    output_file = "ketqua2.txt"
    detect_and_process_license_plate_from_folder(folder_path, output_file)
