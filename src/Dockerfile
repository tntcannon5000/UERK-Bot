# Use the official Python 3.11 image as the base image
FROM public.ecr.aws/lambda/python:3.11

# Copy the requirements.txt file to the container
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the Lambda function code to the container
COPY app/* ${LAMBDA_TASK_ROOT}

# Set the command to run the Lambda function
CMD [ app.handler ]