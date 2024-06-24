import json
from statistics import mean, stdev
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
                    if tag.value in categorized_spans:
                        categorized_spans[tag.value].append(span.duration)
                    break  # No need to check further tags once span.kind is found

    return categorized_spans


def calculate_fingerprints(categorized_spans):
    fingerprints = {}

    for span_kind, durations in categorized_spans.items():
        if durations:
            fingerprints[span_kind] = {
                'mean_latency': mean(durations),
                'std_latency': stdev(durations) if len(durations) > 1 else 0.0
                # stdev requires at least two data points
            }
        else:
            fingerprints[span_kind] = {
                'mean_latency': 0.0,
                'std_latency': 0.0
            }

    return fingerprints


def save_fingerprints_to_file(fingerprints, output_file_path):
    with open(output_file_path, 'w') as file:
        json.dump(fingerprints, file, indent=4)


def main(file_paths, output_file_path):
    traces = load_traces_from_files(file_paths)
    categorized_spans = categorize_spans_by_kind(traces)
    fingerprints = calculate_fingerprints(categorized_spans)
    save_fingerprints_to_file(fingerprints, output_file_path)
    print(f"Fingerprints saved to {output_file_path}")




if __name__ == "__main__":
    path1 = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\cat-api_traces_1719225841.json"
    path2 = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\cat-api_traces_1719040788.json"
    path3 = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\\trace_get_all_cats.json"
    path4 = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\\trace_generate_pairs.json"
    json_file_paths = [path1, path2, path3, path4]
    output_file_path = "/performance_detector/detectors/fingerprints_mean_std.json"
    main(json_file_paths, output_file_path)
