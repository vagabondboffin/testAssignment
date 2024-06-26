# Performance Detector

## Overview

This project provides a set of tools for detecting performance issues and anomalies in trace data. The solution includes various detectors implemented for different types of performance issues and two anomaly detection models utilizing machine learning techniques.

## Directory Structure

The project is organized into three main subdirectories:

1. **data_processing**
   - `trace_elements.py`: Defines the structure of traces, spans, and tags.
   - `trace_parser.py`: Parses trace data from JSON files.
   - `log_parser.py`: Captures logs from different services and Categorizes them.

2. **detectors**
   - `duplicate_span_id_detector.py`: Detects duplicate span IDs within traces. 
   - `n_plus_one_detector.py`: Detects N+1 query issues in traces. 
   - `large_http_payload_detector.py`: Detects spans with large HTTP payloads. F
   - `error_detector.py`: Detects spans containing errors in a hierarchy manner.
   - `anomaly_detector_with_fingerprints.py`: Detects anomalies using fingerprinting techniques. 
   - `base_detector.py`: Base class that all detectors inherit from.

3. **machine_learning**
   - `feature_engineering.py`: Contains functions for feature extraction and preprocessing.
   - `isolation_forest_AD.py`: Implements an anomaly detector using the Isolation Forest algorithm.
   - `lstm_encoder_AD.py`: Implements an anomaly detector using LSTM Encoder-Decoder for time series data.

## Main Script

- **main.py**: Runs all the detectors on a given set of trace data and prints the detected issues.

## Daily Progress

- **myProgress.md**: A daily log of progress and activities carried out during the 5-day task period.


