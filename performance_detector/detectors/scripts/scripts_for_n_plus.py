
import json
from performance_detector.data_processing.trace_parser import TraceParser
from performance_detector.detectors.n_plus_one_detector import NPlusOneDetector
from performance_detector.detectors.duplicate_span_id_detector import DuplicateSpanIDDetector

def detect_issues_in_traces(json_file_path):
    # Parse traces from JSON file
    traces = TraceParser.parse_from_file(json_file_path)

    # Initialize detectors
    n_plus_one_detector = NPlusOneDetector()
    duplicate_span_id_detector = DuplicateSpanIDDetector()

    # Dictionary to store issues by trace ID
    issues_by_trace = {}

    # Iterate over each trace
    for trace in traces:
        # Detect N+1 query issues
        n_plus_one_issues = n_plus_one_detector.detect_n_plus_one_queries(trace)
        duplicate_span_id_issues = duplicate_span_id_detector.detect_duplicate_span_ids(trace)

        # Store issues in dictionary
        issues_by_trace[trace.trace_id] = {
            "N+1 Query Issues": n_plus_one_issues,
            "Duplicate Span ID Issues": duplicate_span_id_issues,
        }

    return issues_by_trace

def main():
    # Example usage with a JSON file of traces
    json_file_path = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\cat-api_traces_1719225841.json"
    # json_file_path = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\\trace_generate_pairs_with_error.json"
    issues_by_trace = detect_issues_in_traces(json_file_path)

    for trace_id, issues in issues_by_trace.items():
        print(f"Issues found in trace {trace_id}:")
        if issues["N+1 Query Issues"]:
            print("N+1 Query Issues:")
            for issue in issues["N+1 Query Issues"]:
                print(f"- {issue}")
        if issues["Duplicate Span ID Issues"]:
            print("Duplicate Span ID Issues:")
            for issue in issues["Duplicate Span ID Issues"]:
                print(f"- {issue}")

if __name__ == "__main__":
    main()
