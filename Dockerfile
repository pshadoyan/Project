FROM nvidia/cuda:11.4.2-devel-ubuntu20.04

# Install Tesseract and OpenCV dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    libopencv-dev \
    python3-opencv

# Set the pytesseract OCR engine config
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata
ENV TESSERACT_CONFIG="--oem 3 --psm 6"

# Copy the Python script into the container
COPY . .

# Install Python requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Start the Python script when the container is run
CMD ["python3", "main.py"]

