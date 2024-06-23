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

### Summary:
Designed the tool's structure and implemented core components for processing trace files and detecting specific issues.

---
