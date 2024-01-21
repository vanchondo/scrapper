# FROM selenium/standalone-chrome:latest
FROM python:3.9

# # Set working directory
# WORKDIR /usr/src/app

# # Install Python and any additional dependencies
# USER root
# RUN apt-get update \
#     && apt-get install -y python3 python3-pip \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

ADD . .
RUN pip install -r requirements.txt

CMD ["python", "./main.py"]