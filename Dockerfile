### Build and install packages
FROM python:3.8 as build-python

RUN apt-get -y update \
    && apt-get install -y gettext \
    # Cleanup apt cache
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt 
# After install all package
FROM python:3.8-slim
# permission
RUN groupadd -r django && useradd -r -g django django
# install package libary
RUN apt-get update \
    && apt-get install -y \
    libxml2 \
    libssl1.1 \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    shared-mime-info \
    mime-support \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
# create static file
RUN mkdir -p /app/media /app/static /app/log \
    && chown -R django:django /app/
# Copy file in build-python to local
COPY --from=build-python /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
COPY --from=build-python /usr/local/bin/ /usr/local/bin/
COPY . /app
# Move to app
WORKDIR /app
# port
EXPOSE 8000
ENV PYTHONUNBUFFERED 1


CMD ["gunicorn", "--bind", ":8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "partsfinder.asgi:application"]
