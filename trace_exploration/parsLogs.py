import subprocess
import re
import datetime
import signal

# Define the services you want to monitor
#SERVICES_TO_MONITOR = ['cat-api', 'cat-recommender-api', 'otel_collector', 'grafana']
SERVICES_TO_MONITOR = ['cat-api']
# Buffer to store logs temporarily
log_buffer = []

def parse_logs():
    # Command to run Docker services and capture their output
    command = 'docker-compose logs --tail=0 --follow'

    # Start the subprocess to capture real-time logs
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    try:
        for line in iter(process.stdout.readline, ''):
            line = line.strip()  # Remove leading/trailing whitespace and newline
            if line:
                service, log_message = extract_service_and_message(line)
                if service and log_message:
                    timestamp = datetime.datetime.utcnow().isoformat()  # Capture timestamp
                    category = categorize_log_line(log_message)
                    if category:
                        log_entry = f"[{timestamp}][{service.upper()}][{category.upper()}] {log_message}"
                        print(log_entry)
                        log_buffer.append(log_entry)
    except KeyboardInterrupt:
        print("\nStopping log parsing...")
        save_logs_to_file()
    finally:
        process.kill()

def extract_service_and_message(line):
    # Extract service name from the log line
    for service in SERVICES_TO_MONITOR:
        if service in line:
            return service, line
    return None, None

def categorize_log_line(line):
    # Define categorization rules based on keywords or patterns
    if re.search(r'error|exception|failed|500 Internal Server Error', line, re.IGNORECASE):
        return 'error'
    elif re.search(r'info|completed|success', line, re.IGNORECASE):
        return 'info'
    elif re.search(r'warning', line, re.IGNORECASE):
        return 'warning'
    elif re.search(r'debug', line, re.IGNORECASE):
        return 'debug'
    else:
        return 'other'  # Unclassified line

def save_logs_to_file():
    if log_buffer:
        try:
            filename = f"captured_logs_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
            with open(filename, 'w') as file:
                for log_entry in log_buffer:
                    file.write(log_entry + '\n')
            print(f"Captured logs saved to {filename}")
        except Exception as e:
            print(f"Error saving logs to file: {e}")

if __name__ == "__main__":
    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, lambda signal, frame: save_logs_to_file() or exit(0))

    # Start parsing logs
    parse_logs()
