FROM python:3.9-slim

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the application files
COPY . .

# Command to run the Flask app
CMD ["python", "app.py"]
