FROM python:3.10-slim-buster as requirements-stage

# Generate dependencies list
WORKDIR /tmp
RUN pip install hatch
COPY ./pyproject.toml /tmp/
RUN hatch dep show requirements --project-only > /tmp/requirements.txt

FROM python:3.10-slim

# Install dependencies
WORKDIR /isbn_api
COPY --from=requirements-stage /tmp/requirements.txt /isbn_api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /isbn_api/requirements.txt

# Copy code
COPY ./isbn_api /isbn_api/isbn_api

# Start server
CMD ["uvicorn", "isbn_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
