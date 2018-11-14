# Starting from Python version 3
FROM python:latest

# Define the repository of the app
WORKDIR /usr/src/app

# Install the required packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app.py file to the app repository
COPY app.py .

CMD [ "python", "./app.py" ]
