import json
import numpy as np
from performance_detector.data_processing.trace_elements import Trace
from performance_detector.data_processing.trace_parser import TraceParser


def load_traces_from_files(file_paths):
    traces = []
    for file_path in file_paths:
        traces.extend(TraceParser.parse_from_file(file_path))
    return traces


def categorize_spans_by_kind(traces):
    categorized_spans = {'client': [], 'server': [], 'internal': []}

    for trace in traces:
        for span in trace.spans:
            for tag in span.tags:
                if tag.key == 'span.kind':
                    kind = tag.value.lower()
                    if kind in categorized_spans:
                        categorized_spans[kind].append(span.duration)
                    break  # No need to check further tags once span.kind is found

    return categorized_spans


def calculate_iqr_fingerprints(categorized_spans):
    fingerprints = {}

    for span_kind, durations in categorized_spans.items():
        if durations:
            durations_array = np.array(durations)
            median_latency = np.median(durations_array)
            q1 = np.percentile(durations_array, 25)
            q3 = np.percentile(durations_array, 75)
            iqr = q3 - q1

            fingerprints[span_kind] = {
                'median_latency': median_latency,
                'iqr_latency': iqr,
                'lower_bound': q1 - 1.5 * iqr,
                'upper_bound': q3 + 1.5 * iqr
            }
        else:
            fingerprints[span_kind] = {
                'median_latency': 0.0,
                'iqr_latency': 0.0,
                'lower_bound': 0.0,
                'upper_bound': 0.0
            }

    return fingerprints


def save_fingerprints_to_file(fingerprints, output_file_path):
    with open(output_file_path, 'w') as file:
        json.dump(fingerprints, file, indent=4)


def main(file_paths, output_file_path):
    traces = load_traces_from_files(file_paths)
    categorized_spans = categorize_spans_by_kind(traces)
    fingerprints = calculate_iqr_fingerprints(categorized_spans)
    save_fingerprints_to_file(fingerprints, output_file_path)
    print(f"Fingerprints saved to {output_file_path}")


if __name__ == "__main__":
    path1 = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\cat-api_traces_1719225841.json"
    path2 = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\cat-api_traces_1719040788.json"
    path3 = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\\trace_get_all_cats.json"
    path4 = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\\trace_generate_pairs.json"
    json_file_paths = [path1, path2, path3, path4]
    output_file_path = "/performance_detector/detectors/files/fingerprints_IQR.json"
    main(json_file_paths, output_file_path)
