# main.py (Updated)
import argparse
import json
from data_processing.trace_parser import TraceParser
from detectors.n_plus_one_detector import NPlusOneDetector


def main(trace_file):
    # Load and parse trace data using TraceParser
    try:
        traces = TraceParser.parse_from_file(trace_file)
    except FileNotFoundError:
        print(f"Trace file '{trace_file}' not found. Please check the file path.")
        return
    except json.JSONDecodeError:
        print(f"Invalid JSON format in trace file '{trace_file}'.")
        return

    # Initialize detectors
    n_plus_one_detector = NPlusOneDetector()

    # Run detectors
    for trace in traces:
        n_plus_one_issues = n_plus_one_detector.detect_n_plus_one_queries(trace)
        for issue in n_plus_one_issues:
            print(f"N+1 Query Issue found: {issue}")


if __name__ == "__main__":
    print("hello")
    parser = argparse.ArgumentParser(description='Performance Detector CLI Tool')
    parser.add_argument('trace_file', type=str, help='Path to the trace JSON file')
    args = parser.parse_args()

    main(args.trace_file)
