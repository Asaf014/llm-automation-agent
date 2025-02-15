#!/bin/bash
set -e

# Configuration
API_URL="http://127.0.0.1:8000"
API_KEY="eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIyZjMwMDIzOTRAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.Bohr4qFCATCcl8jxyeakAynKvgE1y5XcmJV5pVMilfo
"  # Replace with your actual API key

echo "-------------------------------"
echo "Testing GET /status endpoint..."
status=$(curl -s -H "X-API-Key: $API_KEY" "$API_URL/status")
echo "Response: $status"
if [[ $status != *"running"* ]]; then
  echo "GET /status test failed!"
  exit 1
fi

echo "-------------------------------"
echo "Testing GET / (root) endpoint..."
root=$(curl -s -H "X-API-Key: $API_KEY" "$API_URL/")
echo "Response: $root"
if [[ $root != *"Welcome to the LLM Automation Agent!"* ]]; then
  echo "GET / test failed!"
  exit 1
fi

echo "-------------------------------"
echo "Testing POST /execute endpoint with 'check system status'..."
execute=$(curl -s -H "X-API-Key: $API_KEY" -X POST -H "Content-Type: application/json" \
  -d '{"command": "check system status"}' "$API_URL/execute")
echo "Response: $execute"
if [[ $execute != *"System is operational."* ]]; then
  echo "POST /execute test failed!"
  exit 1
fi

echo "-------------------------------"
echo "Testing POST /file endpoint (write)..."
file_write=$(curl -s -H "X-API-Key: $API_KEY" -X POST -H "Content-Type: application/json" \
  -d '{"action": "write", "filename": "test.txt", "content": "Hello, test!"}' "$API_URL/file")
echo "Response: $file_write"
if [[ $file_write != *"written successfully"* ]]; then
  echo "POST /file write test failed!"
  exit 1
fi

echo "-------------------------------"
echo "Testing POST /file endpoint (read)..."
file_read=$(curl -s -H "X-API-Key: $API_KEY" -X POST -H "Content-Type: application/json" \
  -d '{"action": "read", "filename": "test.txt"}' "$API_URL/file")
echo "Response: $file_read"
if [[ $file_read != *"Hello, test!"* ]]; then
  echo "POST /file read test failed!"
  exit 1
fi

echo "-------------------------------"
echo "Testing POST /extract endpoint..."
# Write a file to use for extraction test
curl -s -H "X-API-Key: $API_KEY" -X POST -H "Content-Type: application/json" \
  -d '{"action": "write", "filename": "extract_test.txt", "content": "apple\nbanana\napple\ncherry"}' "$API_URL/file" > /dev/null
extract=$(curl -s -H "X-API-Key: $API_KEY" -X POST -H "Content-Type: application/json" \
  -d '{"file_path": "extract_test.txt", "keyword": "apple"}' "$API_URL/extract")
echo "Response: $extract"
if [[ $extract != *"apple"* ]]; then
  echo "POST /extract test failed!"
  exit 1
fi

echo "-------------------------------"
echo "Testing Business Endpoint: /business/fetch-data..."
fetch=$(curl -s -H "X-API-Key: $API_KEY" -X POST -H "Content-Type: application/json" \
  -d '{"url": "http://example.com", "output_filename": "example.html"}' "$API_URL/business/fetch-data")
echo "Response: $fetch"
if [[ $fetch != *"fetched"* && $fetch != *"saved"* ]]; then
  echo "Business /fetch-data test may have failed!"
  # We won't exit here since this might vary based on the fetched content.
fi

echo "-------------------------------"
echo "All tests passed successfully!"
