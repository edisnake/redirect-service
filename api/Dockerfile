FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy the application code
COPY . .
# Install the application dependencies
RUN pip install --no-cache-dir -r  requirements.txt

EXPOSE 8006

# Giving sometime to the DB to fully start
# Sleep is required here since the depends_on in docker-compose file only ensures that the dependent container
# starts after the specified container has started, but it does not wait for the container to be up and running
ENTRYPOINT ["sh", "-c", "sleep 12 && exec uvicorn main:app --reload --host 0.0.0.0 --port 8006"]
