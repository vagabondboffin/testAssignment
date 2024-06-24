import subprocess
import re
import datetime
import signal

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
                    category = categorize_log_line(line)
                    if category:
                        log_entry = f"[{timestamp}][{service.upper()}][{category.upper()}] {log_message}"
                        if category == 'otel_collector_prometheus_exporter':
                            process_otel_collector_prometheus_exporter(log_message)
                        elif category.endswith('_http_server_duration'):
                            process_http_server_duration(log_message, category)
                        else:
                            print(log_entry)
                            log_buffer.append(log_entry)
    except KeyboardInterrupt:
        print("\nStopping log parsing...")
        save_logs_to_file()
    finally:
        process.kill()

def extract_service_and_message(line):
    # Extract service name from the log line
    service = line.split()[0].rstrip('-1')
    log_message = ' '.join(line.split()[1:])
    return service, log_message

def categorize_log_line(line):
    # Extract the service name from the log line
    service = line.split()[0].rstrip('-1')

    # Define categorization rules based on keywords or patterns
    if re.search(r'exception', line, re.IGNORECASE):
        return 'exception'
    elif re.search(r'error', line, re.IGNORECASE):
        return 'error'
    elif re.search(r'500 Internal Server Error', line, re.IGNORECASE):
        return '500_internal_server_error'
    elif re.search(r'info|completed|success', line, re.IGNORECASE):
        return 'info'
    elif re.search(r'warning', line, re.IGNORECASE):
        return 'warning'
    elif re.search(r'debug', line, re.IGNORECASE):
        return 'debug'
    elif re.search(r'http_server_duration', line, re.IGNORECASE):
        return f"{service}_http_server_duration"
    elif service == 'otel_collector' and re.search(r'prometheus', line, re.IGNORECASE):
        return 'otel_collector_prometheus_exporter'
    else:
        return 'other'

def process_otel_collector_prometheus_exporter(line):
    # Extract relevant information from the Prometheus exporter logs
    match = re.search(r'error gathering metrics: collected metric http_server_duration', line)
    if match:
        print("Error gathering http_server_duration metrics in the Prometheus exporter.")
        # You can add further processing or error handling here

def process_http_server_duration(line, category):
    # Extract relevant information from the http_server_duration log line
    match = re.search(r'label:\{name:"http_method" value:"(\w+)"\} label:\{name:"http_route" value:"([^"]+)"\} label:\{name:"http_status_code" value:"(\d+)"\} histogram:\{sample_count:(\d+) sample_sum:(\d+\.\d+)', line)
    if match:
        http_method = match.group(1)
        http_route = match.group(2)
        http_status_code = match.group(3)
        sample_count = int(match.group(4))
        sample_sum = float(match.group(5))
        print(f"[{category}] HTTP Method: {http_method}, HTTP Route: {http_route}, HTTP Status Code: {http_status_code}, Sample Count: {sample_count}, Sample Sum: {sample_sum}")

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