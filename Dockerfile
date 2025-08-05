FROM python:3.9-slim

WORKDIR /app


RUN apt-get update && apt-get install -y cron




# Copy all MTA files
COPY 0mq .
COPY test-0mq.py .
COPY requirements.txt .

# COPY transport_map_sample.json .

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh 

# Ensure cron.log exists and is writable
RUN touch /var/log/mailenv.log && chmod 666 /var/log/mailenv.log

#CMD ["/bin/bash"]
CMD ["/app/entrypoint.sh"] 