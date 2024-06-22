import requests
import time
import json
import os


def fetch_traces(service_name):
    try:
        response = requests.get(f"http://localhost:16686/api/traces?service={service_name}")
        response.raise_for_status()  # Raise an error for bad status codes

        # Check if the response contains JSON data
        if response.text:
            traces = response.json()
            return traces
        else:
            print("No traces found.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except ValueError:
        print("Failed to decode JSON from the response.")
        return None


def save_traces(traces, service_name):

    # Define the filename based on the service name and current timestamp
    filename = f"traces/{service_name}_traces_{int(time.time())}.json"

    # Save traces to the file
    with open(filename, 'w') as f:
        json.dump(traces, f, indent=4)

    print(f"Traces saved to {filename}")


# Retry logic to ensure traces are available
service_name = "cat-api"  # Specify the service name
for _ in range(5):  # Retry up to 5 times
    traces = fetch_traces(service_name)
    if traces and traces.get('data'):
        break
    else:
        print("Retrying...")
        time.sleep(5)  # Wait for 5 seconds before retrying

# Analyze and save traces if available
if traces and traces.get('data'):
    save_traces(traces, service_name)
else:
    print("No trace data to analyze.")
print("end")