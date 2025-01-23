FROM public.ecr.aws/lambda/python:3.9

# Copy the code
COPY handler.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install dependencies
RUN pip install -r requirements.txt

# Invoke the function handler in handler.py when receiving an event
CMD ["handler.process"]