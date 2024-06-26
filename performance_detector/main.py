import json
from performance_detector.data_processing.trace_parser import TraceParser
from performance_detector.detectors.n_plus_one_detector import NPlusOneDetector
from performance_detector.detectors.duplicate_span_id_detector import DuplicateSpanIDDetector
from performance_detector.detectors.large_http_payload_detector import LargeHttpPayloadDetector
from performance_detector.detectors.error_detector import ErrorDetector
from performance_detector.detectors.anomaly_detector_with_fingerprints import AnomalyDetectorWithFingerprints

def detect_issues_in_traces(json_file_path):
    # Parse traces from JSON file
    traces = TraceParser.parse_from_file(json_file_path)

    # Initialize detectors
    n_plus_one_detector = NPlusOneDetector()
    duplicate_span_id_detector = DuplicateSpanIDDetector()
    large_http_payload_detector = LargeHttpPayloadDetector()
    error_detector = ErrorDetector()
    anomaly_detector = AnomalyDetectorWithFingerprints()

    issues_by_trace = {}

    # Iterate over each trace
    for trace in traces:
        # Detect issues with each detector
        n_plus_one_issues = n_plus_one_detector.detect_n_plus_one_queries(trace)
        duplicate_span_id_issues = duplicate_span_id_detector.detect_duplicate_span_ids(trace)
        large_http_payload_issues = large_http_payload_detector.detect_large_http_payloads(trace)
        error_issues = error_detector.detect_errors(trace)
        anomaly_issues = anomaly_detector.detect_anomalies(trace)

        issues_by_trace[trace.trace_id] = {
            "N+1 Query Issues": n_plus_one_issues,
            "Duplicate Span ID Issues": duplicate_span_id_issues,
            "Large HTTP Payload Issues": large_http_payload_issues,
            "Error Issues": error_issues,
            "Anomaly Issues": anomaly_issues,
        }

    return issues_by_trace

def main():
    json_file_path = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\cat-api_traces_1719040788.json"
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
        if issues["Large HTTP Payload Issues"]:
            print("Large HTTP Payload Issues:")
            for issue in issues["Large HTTP Payload Issues"]:
                print(f"- {issue}")
        if issues["Error Issues"]:
            print("Error Issues:")
            for issue in issues["Error Issues"]:
                print(f"- {issue}")
        if issues["Anomaly Issues"]:
            print("Anomaly Issues:")
            for issue in issues["Anomaly Issues"]:
                print(f"- {issue}")

if __name__ == "__main__":
    main()
