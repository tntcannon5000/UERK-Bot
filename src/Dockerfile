# Use the official Python 3.11 image as the base image
FROM public.ecr.aws/lambda/python:3.11

# Install necessary build tools (including gcc) using yum
RUN yum update -y && yum install -y gcc make 

# Copy requirements.txt to the container
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install Python dependencies 
RUN pip install -r requirements.txt

# Copy the Lambda function code to the container
COPY app/* ${LAMBDA_TASK_ROOT}

# Set the command to run the Lambda function
CMD [ "app.handler" ] 