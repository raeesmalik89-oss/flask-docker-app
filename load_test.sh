
#!/bin/bash

echo "Starting load test..."
echo "Testing main page..."

for i in {1..5}; do
    echo "Request $i:"
    curl -s -w "Time: %{time_total}s, Status: %{http_code}\n" http://localhost:8080/ > /dev/null
    sleep 1
done

echo "Load test completed!"
