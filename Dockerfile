FROM python:3.11-slim-buster

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Use the openai_api_key secret
RUN --mount=type=secret,id=openai_api_key,dst=/run/secrets/openai_api_key \
    echo "export OPENAI_API_KEY=$(cat /run/secrets/openai_api_key)" >> /app/env.sh

CMD [ "sh", "-c", ". /app/env.sh && python main.py" ]