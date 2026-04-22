FROM apify/actor-python-selenium:3.11

# Install Python dependencies first
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy all files to the image
COPY . ./

# Set Python path to include root directory
ENV PYTHONPATH=/usr/src/app:$PYTHONPATH

# Set the entrypoint to the actor main script
CMD ["python", "actor_main.py"]
