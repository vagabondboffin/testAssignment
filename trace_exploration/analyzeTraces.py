import requests
import time

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

# Retry logic to ensure traces are available
service_name = "cat-api"  # Specify the service name
for _ in range(5):  # Retry up to 5 times
    traces = fetch_traces(service_name)
    if traces and traces.get('data'):
        break
    else:
        print("Retrying...")
        time.sleep(5)  # Wait for 5 seconds before retrying

# Analyze traces if available
if traces and traces.get('data'):
    for trace in traces['data']:
        # Implement logic to detect N+1 query problem
        print(trace)
else:
    print("No trace data to analyze.")
