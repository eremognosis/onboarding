FROM nvidia/cuda:12.1.0-base-ubuntu22.04

# Install Python and essential tools
RUN apt-get update && apt-get install -y python3 python3-pip git

WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the models and data
COPY . .

# Expose the Flask port
EXPOSE 8000

# Start the server
CMD ["python3", "AI/server.py"]