import cv2
import os

def locate_measurement_points(image_path, output_path):
    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    # Define output file paths
    output_image_path = os.path.join(output_path, "highlighted_image.png")
    output_text_path = os.path.join(output_path, "measurement_points.txt")
    gray_image_path = os.path.join(output_path, "gray.png")
    binary_image_path = os.path.join(output_path, "binary.png")

    # Open a file to write the output
    with open(output_text_path, 'w') as file:
        # Load the image
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        cv2.namedWindow("Original_image", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Original_image", 400, 820)
        cv2.imshow("Original_image", image)
        cv2.waitKey(1)

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(gray_image_path, gray)
        cv2.namedWindow("Gray_image", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Gray_image", 400, 820)
        cv2.imshow("Gray_image", gray)
        cv2.waitKey(1)

        # Apply Canny edge detection
        edges = cv2.Canny(gray, 150, 150)
        cv2.imwrite(binary_image_path, edges)
        cv2.namedWindow("Binary_image", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Binary_image", 400, 820)
        cv2.imshow("Binary_image", edges)
        cv2.waitKey(1)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        n = 0
        for contour in contours:
            # Compute the bounding box for each contour
            x, y, w, h = cv2.boundingRect(contour)

            # Draw rectangles around detected measurement points
            if 45 > w > 20 and 45 > h > 20:  # Adjust this threshold as needed
                n += 1
                # Calculate center coordinates
                center_x = x + w // 2
                center_y = y + h // 2
                image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
                # Write the number next to the rectangle
                cv2.putText(image, str(n), (x + 10, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                print(f"Measurement Point {n}: X={center_x}, Y={center_y}")
                print(f"Measurement Point {n}: X={center_x}, Y={center_y}", file=file)

        # Save the new image with highlighted measurement points
        cv2.imwrite(output_image_path, image)
        print(f"Highlighted image saved as {output_image_path}")

        cv2.namedWindow("shapes_detected", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("shapes_detected", 400, 820)
        cv2.imshow("shapes_detected", image)
        cv2.waitKey(0)


input_image_path = "Projektarbete i elektroteknik\github\DUT.png" #Picture of PCBA
output_path = "Projektarbete i elektroteknik\github\V1" #Place path to folder for output

locate_measurement_points(input_image_path, output_path)
