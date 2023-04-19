import base64
import pytesseract
import cv2
import numpy as np
from obswebsocket import obsws, requests

# Connect to OBS using the WebSocket API
ws = obsws("localhost", 4444)
ws.connect()

try:
    # Continuously retrieve video frames from OBS and extract text
    while True:
        # Get a screenshot of the current preview output in OBS
        screenshot = ws.call(requests.GetPreviewScreenshot())
        img_bytes = base64.b64decode(screenshot["img"])
        img_array = np.frombuffer(img_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_array, flags=cv2.IMREAD_COLOR)

        # Convert the image to grayscale and apply some filters to remove noise
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 3)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Use pytesseract to extract text from the image
        text = pytesseract.image_to_string(thresh, config=pytesseract_config)

        # Process the extracted text (e.g., remove any unwanted characters or words)
        processed_text = process_text(text)

        # Do something with the extracted text (e.g., send it to a chatbot)
        send_text(processed_text)

except KeyboardInterrupt:
    # Gracefully exit the loop if the user presses Ctrl+C
    pass

# Disconnect from OBS
ws.disconnect()

