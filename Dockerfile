# Starting from Python version 3
FROM python:latest

# Define the repository of the app
WORKDIR /app

# Install the required packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app.py file to the app repository
COPY app.py .

# Expose API port 5000
EXPOSE 5000

CMD [ "python", "./app.py" ]
