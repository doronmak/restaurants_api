FROM python:3

# set the working directory in the container
WORKDIR /api

# copy the dependencies file to the working directory
COPY requirements/prod.txt .

# install dependencies
RUN pip install -r prod.txt

# copy the content of the local src directory to the working directory
COPY src .

# command to run on container start
CMD [ "python", "/api/main.py" ]


