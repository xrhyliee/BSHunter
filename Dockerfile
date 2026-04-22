FROM apify/actor-python:3.11

# Install Python dependencies first
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy all files to the image
COPY . ./

# Set the entrypoint to the actor main script
CMD python actor_main.py
