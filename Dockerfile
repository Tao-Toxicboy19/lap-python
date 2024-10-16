# Step 1: Use a base image with Python
FROM python:3.10-slim

# Step 2: Set environment variables to prevent buffering and set Streamlit config defaults
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLE_CORS=true

# Step 3: Set the working directory in the container
WORKDIR /app

# Step 4: Copy the requirements.txt file into the container
COPY requirements.txt ./requirements.txt

# Step 5: Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the rest of your app code into the container
COPY . /app

# Step 7: Expose the port that Streamlit will use (default 8501)
EXPOSE 8501

# Step 8: Command to run Streamlit when the container starts
CMD ["streamlit", "run", "app.py"]