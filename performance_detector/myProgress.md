# My Progress

## Day 1: Environment Setup and Initial Exploration (June 21, 2024 - Friday)

### Tasks Completed:
- Installed Docker & Docker Compose.
- Cloned the repository.
- Started the services with `docker compose up`.
- Accessed the cat-api HTTP API documentation.
- Made API calls using the "Try it out" button.
- Explored traces in the Jaeger UI related to the API calls.

### Summary:
Set up the development environment, explored the API, and reviewed traces in Jaeger UI.

---
## Day 2: Research and Tracing (June 22, 2024 - Saturday)

### Tasks Completed:
- Researched tracing resources and terminology.
- Explored various tools for monitoring.
- Wrote scripts to collect traces from both the terminal and Jaeger UI into my IDE.
- Studied common issues that can be found in traces.

### Summary:
Focused on understanding tracing and monitoring tools, collected traces for analysis

---
## Day 3: Designing and Implementing the Tool (June 23, 2024 - Sunday)

### Tasks Completed:
- Decided on the structure of the tool.
- Implemented two files in the `data_processing` subdirectory to handle JSON trace files: `trace_parser.py` and `trace_elements.py`.
- Developed two kinds of issue detectors: 
  - `N+1 queries detector`
  - `Duplicate span ID detector`

---
## Day 4: Deeper into Traces and Logs (June 24, 2024 - Monday)
### Tasks Completed:
- Developed `large_http_payload_detector.py` to detect the Large HTTP Payload problem. 
- I started digging deeper into traces. I wanted to mark traces with high latency, but I noticed that "high" is very different when working with different kind of spans. So started making fingerprints based on each `span.kind`.
Using mean and standard deviation was useless because the std value was very high, indicating that there is a wide dispersion in the data, making it difficult to use mean ± std for anomaly detection.   
- So, I made fingerprints using Median and Interquartile Range (IQR) method and implemented an anomaly detector that uses these fingerprints.
- Developed `exception_trace_detector.py` to find traces that are countering an exception.
- Developed `log_parser.py` in the `data_processing` subdirectory to make senses of the logs and the runtime information. The implemented function would monitor logs, label them with services, and one of the labels below, saved in .txt files. 
  - exception
  - warning 
  - error 
  - 500 Internal Server Error
  - info 
  - other