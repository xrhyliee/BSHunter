FROM apify/actor-python:3.11

# Copy all files to the image
COPY . ./

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Set the entrypoint to the actor main script
CMD python main/actor_main.py
