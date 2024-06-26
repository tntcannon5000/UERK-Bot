# Stage 2: Build the Lambda function image
FROM public.ecr.aws/lambda/python:3.10

# Copy dependencies from the pre-built image
COPY --from=dependencies-image-shitpostbot /var/task/dependencies /var/task/

# Copy the Lambda function code 
COPY app/* ${LAMBDA_TASK_ROOT}

# Set the command to run the Lambda function
CMD [ "app.handler" ] 