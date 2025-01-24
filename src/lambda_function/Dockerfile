# Use the AWS Lambda Python 3.9 base image
FROM public.ecr.aws/lambda/python:3.9

# Set the working directory to the Lambda task root
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy application code and requirements file to the working directory
COPY handler.py ./
COPY requirements.txt ./

# Install dependencies into the Lambda task root
RUN pip install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Define the CMD to invoke the Lambda function handler
CMD ["handler.process"]