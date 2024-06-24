from performance_detector.data_processing.trace_parser import TraceParser
from performance_detector.detectors.large_http_payload_detector import LargeHttpPayloadDetector

def main():
    json_file_path = "/trace_exploration/traces/cat-recommender-api_traces_1719226007.json"
    traces = TraceParser.parse_from_file(json_file_path)

    http_payload_detector = LargeHttpPayloadDetector()

    for trace in traces:
        issues = http_payload_detector.detect(trace)
        for issue in issues:
            print(issue)

if __name__ == "__main__":
    main()
