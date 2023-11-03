FROM python:3.11

# Define the variable at the top of the Dockerfile
ARG APP_NAME=greenbutton

ENV TZ="America/Chicago"

# Upgrade pip and install requirements
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Set up the virtual environment with the specified directory name
RUN python -m venv ${APP_NAME}-env
RUN /bin/bash -c "source ${APP_NAME}-env/bin/activate"

RUN pip install -r requirements.txt

# Use the variable for the subsequent work directory
WORKDIR /usr/src/app/${APP_NAME}
