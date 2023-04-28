import cv2
import mysql.connector
from matplotlib import pyplot as plt
import numpy as np
import imutils
from flask import Flask, render_template, request
import easyocr
import re

app = Flask(__name__)

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="project"
)

# Route to display the index page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

# Route to process the car details
@app.route('/car_details', methods=['POST'])
def get_car_details():
    # Get uploaded image
    img = cv2.imdecode(np.fromstring(request.files['file'].read(), np.uint8), cv2.IMREAD_UNCHANGED)

    # Preprocess image for number plate detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
    edged = cv2.Canny(bfilter, 30, 200) #Edge detection

    # Find contours and sort by area to get the location of the number plate
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break

    # Crop the number plate
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0,255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)
    (x,y) = np.where(mask==255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]

    # Read number plate using OCR
    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)
    number_plate = result[0][-2]
    number_plate = re.sub(r'[^a-zA-Z0-9]', '', number_plate)

    # Query database for car details
    cursor = db.cursor()
    query = "SELECT * FROM latest_car_info WHERE number_plate = %s"
    cursor.execute(query, (number_plate,))
    result = cursor.fetchone()

    # If car details not found, display error message
    if result is None:
        return render_template('car_details.html', error_message="Car details not found")

    # Get car details from database
    registration_date = result[1]
    owner_name = result[2]
    vehicle_class = result[3]
    fuel_type = result[4]
    color = result[5]

    # Display car details
    return render_template('car_details.html', number_plate=number_plate, registration_date=registration_date, owner_name=owner_name, vehicle_class=vehicle_class, fuel_type=fuel_type, color=color)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)

