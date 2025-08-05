#!/usr/bin/env python3

import zmq
import sys
import os
import time
from datetime import datetime
import json

def main():
    # Read host from SMTPHOST file and transform it
    server_ip = "localhost"
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

    
    
    # Do 10 requests, waiting each time for a response
    for request in range(10):
        payload = {
            "from": "test@mailenv.com",
            "to": "test@mailenv.com",
            "subject": "Test email",
            "body": "This is a test email",
            "smtp-env": "smtp-255733",
            "message_id": ''.join(__import__('random').choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=16)),
            
        }
        print(f"📤 Sending request {request}...")
        socket.send(json.dumps(payload).encode('utf-8'))
        # socket.send(b"hi")
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
    print(f"📊 Requests per second: {1000/duration:.2f} req/sec")
    
    # Clean up
    socket.close()
    context.term()

if __name__ == "__main__":
    main() 