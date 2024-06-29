# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY migrate_json_to_sql.py .
COPY wait_for_mysql.py .
COPY pokemons_data.json .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Run the shell script
CMD ["./run-scripts.sh"]
