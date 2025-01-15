# Use an official Python runtime as a parent image
FROM python:3.10-alpine

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Expose a port for debugging or monitoring if needed (optional)
EXPOSE 8080

CMD ["python", "main.py"]
