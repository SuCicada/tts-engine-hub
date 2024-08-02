FROM python:3.10-slim

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN apt update && apt install make && make install &&\
        rm -rf /var/lib/apt/lists/* &&\
        apt-get clean && pip cache purge

# Make port 80 available to the world outside this container
EXPOSE 41402

# Run app.py when the container launches
CMD ["make", "run"]
