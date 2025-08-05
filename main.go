package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"path/filepath"

	"github.com/pebbe/zmq4"
)

func main() {
	// Load environments file
	envPath := "/app/mailenv-data/host-environments.json"
	hostEnvironments := make(map[string]interface{})

	data, err := os.ReadFile(envPath)
	if err != nil {
		log.Printf("❌ host-environments.json not found: %v", err)
	} else {
		err = json.Unmarshal(data, &hostEnvironments)
		if err != nil {
			log.Fatalf("❌ Failed to parse host-environments.json: %v", err)
		}
		log.Printf("✅ host-environments.json loaded: %+v", hostEnvironments)
	}

	port := 9210
	bindAddr := fmt.Sprintf("tcp://*:%d", port)

	// Start ZeroMQ REP server
	context, _ := zmq4.NewContext()
	socket, _ := context.NewSocket(zmq4.REP)
	defer socket.Close()

	err = socket.Bind(bindAddr)
	if err != nil {
		log.Fatalf("❌ Failed to bind: %v", err)
	}

	mountDir := "/app/mailenv-data"
	log.Printf("🚀 Mailenv SMTP MQ server bound to %s", bindAddr)
	log.Printf("📁 Using mount directory: %s", mountDir)

	// Function to process a single payload
	processPayload := func(p map[string]interface{}) bool {
		envKey, ok := p["smtp-env"].(string)
		if !ok || hostEnvironments[envKey] == nil {
			log.Printf("❌ Invalid SMTP Env: %v", envKey)
			return false
		}

		maildrop := filepath.Join(mountDir, envKey, "mail")
		if _, err := os.Stat(maildrop); os.IsNotExist(err) {
			log.Printf("❌ Invalid Path: %s", maildrop)
			return false
		}

		msgID, _ := p["message_id"].(string)
		filePath := filepath.Join(maildrop, msgID)

		fileData, _ := json.Marshal(p)
		if err := os.WriteFile(filePath, fileData, 0644); err != nil {
			log.Printf("❌ Failed to write file: %v", err)
			return false
		}

		log.Println("📤 ok")
		return true
	}

	for {
		msg, err := socket.Recv(0)
		if err != nil {
			log.Printf("❌ Failed to receive: %v", err)
			continue
		}

		log.Println("📨 Received request")

		var raw interface{}
		if err := json.Unmarshal([]byte(msg), &raw); err != nil {
			log.Printf("❌ Invalid JSON: %v", err)
			socket.Send("error", 0)
			continue
		}

		successCount := 0

		switch v := raw.(type) {
		case map[string]interface{}:
			if processPayload(v) {
				successCount++
			}
		case []interface{}:
			for _, item := range v {
				if p, ok := item.(map[string]interface{}); ok {
					if processPayload(p) {
						successCount++
					}
				} else {
					log.Printf("⚠️ Skipping non-object item: %v", item)
				}
			}
		default:
			log.Printf("❌ Unexpected JSON type: %T", v)
			socket.Send("error", 0)
			continue
		}

		resp := fmt.Sprintf("ok (%d processed)", successCount)
		socket.Send(resp, 0)
	}
}
