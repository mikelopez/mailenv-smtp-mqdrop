#!/usr/bin/env python3

import zmq
import sys
import os
import time
from datetime import datetime
import json

def main():
    # Read host from SMTPHOST file and transform it
    server_ip = "18.191.211.54"
    #server_ip = "localhost"
    server_port = 9210

    TOTAL_REQUESTS = 100
    BATCH_SIZE = 10
    NUM_BATCHES = TOTAL_REQUESTS // BATCH_SIZE

    
    connection_string = f"tcp://{server_ip}:{server_port}"
    print(f"🔌 Connecting to ZeroMQ server at {connection_string}")
    
    # Record start time
    start_time = time.time()
    start_datetime = datetime.now()
    print(f"🚀 Starting test at: {start_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
    
    context = zmq.Context()
    
    # Socket to talk to server
    socket = context.socket(zmq.REQ)
    socket.connect(connection_string)
    
    print("✅ Connected to server")
    print(f"📤 Sending {NUM_BATCHES} batches of {BATCH_SIZE} messages each...")

    payload = {
        "from": "test@mailenv.com",
        "to": "test@mailenv.com",
        "subject": "Test email",
        "body": "This is a test email",
        "smtp-env": "smtp-255733",  # Add required smtp-env field
        "message_id": "msgid-1234567890abcdef",
        "thread_id": "thread-abcdef1234567890",
        "user_id": "user-9876543210",
        "account_id": "acct-1122334455",
        "transaction_id": "txn-9988776655",
        "campaign_id": "camp-5566778899",
        "mailing_list_id": "mlist-4433221100",
        "customer_id": "cust-1234abcd5678efgh",
        "organization_id": "org-8765wxyz4321lmno",
        "timestamp": "2024-06-01T12:34:56Z",
        "priority": "normal",
        "attachments": [
            {"filename": "test.pdf", "id": "att-001", "size": 123456},
            {"filename": "image.png", "id": "att-002", "size": 654321}
        ],
        "headers": {
            "X-Mailenv-Tracking": "track-abc123",
            "X-Fake-Header": "fake-value"
        },
        "flags": ["bulk", "test", "automated"],
        "ip_address": "192.0.2.123",
        "server_id": "srv-0001",
        "session_id": "sess-abcdef123456",
        "random_token": "tok-xyz987654321",
        "extra_data": {
            "foo": "bar",
            "baz": 42,
            "qux": [1, 2, 3]
        }
    }
    
    # Create batches of 10 messages
    for batch in range(NUM_BATCHES):
        # Create a batch by appending payload 10 times
        batch_payload = []
        for i in range(BATCH_SIZE):
            # Create a copy of the payload with unique message_id for each message
            message_payload = payload.copy()
            message_payload["message_id"] = f"msgid-{batch}-{i}-{int(time.time())}"
            batch_payload.append(message_payload)
        
        print(f"📤 Sending batch {batch + 1}/{NUM_BATCHES} with {BATCH_SIZE} messages...")
        socket.send(json.dumps(batch_payload).encode('utf-8'))
        
        # Get the reply
        message = socket.recv()
        print(f"📥 Received reply for batch {batch + 1} [ {message} ]")
    
    # Record end time
    end_time = time.time()
    end_datetime = datetime.now()
    duration = end_time - start_time
    
    print("✅ All batches completed!")
    print(f"⏰ End time: {end_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏱️ Total duration: {duration:.2f} seconds")
    print(f"📊 Total messages sent: {TOTAL_REQUESTS}")
    print(f"📊 Batches sent: {NUM_BATCHES}")
    print(f"📊 Messages per batch: {BATCH_SIZE}")
    print(f"📊 Messages per second: {TOTAL_REQUESTS/duration:.2f} msg/sec")
    
    # Clean up
    socket.close()
    context.term()

if __name__ == "__main__":
    main() 