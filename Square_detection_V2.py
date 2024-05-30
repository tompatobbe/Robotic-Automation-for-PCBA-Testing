import cv2
import os

def locate_measurement_points(image_path, output_path):
    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    # Define output file paths
    output_image_path = os.path.join(output_path, "highlighted_image_V2.png")
    output_text_path = os.path.join(output_path, "measurement_points_V2.txt")
    gray_image_path = os.path.join(output_path, "gray_V2.png")
    binary_image_path = os.path.join(output_path, "binary_V2.png")
    equalized_image_path = os.path.join(output_path, "Gray_equalized_image_V2.png")

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
        
        # Enhance contrast using histogram equalization
        equalized = cv2.equalizeHist(gray)
        cv2.imwrite(binary_image_path, equalized)
        cv2.namedWindow("Gray_equalized_image", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Gray_equalized_image", 400, 820)
        cv2.imshow("Gray_equalized_image", equalized)
        cv2.waitKey(1)



        # Apply adaptive thresholding
        blockSize = 11  # Try different values: 11, 13, 15, etc.
        C = 2  # Try different values: 2, 5, 10, etc.
        thresh = cv2.adaptiveThreshold(equalized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, blockSize, C)
        cv2.imwrite(equalized_image_path, thresh)
        cv2.namedWindow("Thresholded Image", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Thresholded Image", 400, 820)
        cv2.imshow("Thresholded Image", thresh)
        cv2.waitKey(1)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        n = 0
        for contour in contours:
            # Approximate the contour
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            
            # Check if the approximated contour has 4 sides (square/rectangle)
            if len(approx) == 4:
                # Compute the bounding box for each contour
                x, y, w, h = cv2.boundingRect(approx)

                # Check if the contour is approximately square
                if 10 < w < 20 and 10 < h < 20 and abs(w - h) < 5:  # Adjust size criteria as needed
                    n += 1
                    # Calculate center coordinates
                    center_x = x + w // 2
                    center_y = y + h // 2
                    # Draw rectangles around detected measurement points
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # Write the number next to the rectangle
                    cv2.putText(image, str(n), (x + 10, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    print(f"Measurement Point {n}: X={center_x}, Y={center_y}")
                    print(f"Measurement Point {n}: X={center_x}, Y={center_y}", file=file)

        # Save the new image with highlighted measurement points
        cv2.imwrite(output_image_path, image)
        cv2.namedWindow("shapes_detected", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("shapes_detected", 400, 820)
        cv2.imshow("shapes_detected", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


input_image_path = "Projektarbete i elektroteknik\github\DUT.png"
output_image_path = "Projektarbete i elektroteknik\github\V2"
locate_measurement_points(input_image_path, output_image_path)