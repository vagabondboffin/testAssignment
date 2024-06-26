import json
from performance_detector.data_processing.trace_elements import Trace
from performance_detector.data_processing.trace_parser import TraceParser
from performance_detector.detectors.base_detector import BaseDetector


class AnomalyDetectorWithFingerprints(BaseDetector):
    def __init__(self):
        super().__init__()
        self.fingerprints = self.load_fingerprints()

    def load_fingerprints(self):
        fingerprint_file_path = "A:\py\pythonProjects\\testAssignment\performance_detector\detectors\\files\\fingerprints_IQR.json"
        with open(fingerprint_file_path, 'r') as file:
            return json.load(file)

    def detect_anomalies(self, trace: Trace) -> list:
        anomalies = []

        for span in trace.spans:
            span_kind = self.get_span_kind(span)
            if span_kind and span_kind in self.fingerprints:
                lower_bound = self.fingerprints[span_kind]['lower_bound']
                upper_bound = self.fingerprints[span_kind]['upper_bound']

                if not (lower_bound <= span.duration <= upper_bound):
                    anomalies.append(self.format_anomaly(span, span_kind))

        return anomalies

    def get_span_kind(self, span) -> str:
        for tag in span.tags:
            if tag.key == 'span.kind':
                return tag.value.lower()
        return None

    def format_anomaly(self, span, span_kind) -> dict:
        return {
            'span_id': span.span_id,
            'operation_name': span.operation_name,
            'kind': span_kind,
            'duration': span.duration,
            'description': f"Anomalous {span_kind} span detected"
        }


def main(trace_files, fingerprint_file_path, output_file_path):
    traces = []
    for file_path in trace_files:
        traces.extend(TraceParser.parse_from_file(file_path))

    detector = AnomalyDetectorWithFingerprints(fingerprint_file_path)
    all_anomalies = []

    for trace in traces:
        anomalies = detector.detect_anomalies(trace)
        if anomalies:
            all_anomalies.append({
                'trace_id': trace.trace_id,
                'anomalies': anomalies
            })

    with open(output_file_path, 'w') as file:
        json.dump(all_anomalies, file, indent=4)

    output_file_path = "A:\py\pythonProjects\\testAssignment\performance_detector\detectors\\files\\anomalies_detected_with_fingerprint.json"
    print(f"Anomalies saved to {output_file_path}")

