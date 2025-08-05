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
    server_port = 9210
    

    
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
    print("📤 Sending 10 requests...")

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
    
    # Do 10 requests, waiting each time for a response
    for request in range(100):
        print(f"📤 Sending request {request}...")
        socket.send(json.dumps(payload).encode('utf-8'))
        
        # Get the reply
        message = socket.recv()
        print(f"📥 Received reply {request} [ {message} ]")
    
    # Record end time
    end_time = time.time()
    end_datetime = datetime.now()
    duration = end_time - start_time
    
    print("✅ All requests completed!")
    print(f"⏰ End time: {end_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏱️ Total duration: {duration:.2f} seconds")
    
    print(f"📊 Requests per second: {100/duration:.2f} req/sec")
    
    # Clean up
    socket.close()
    context.term()

if __name__ == "__main__":
    main() 