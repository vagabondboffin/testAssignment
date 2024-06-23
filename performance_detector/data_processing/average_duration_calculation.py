from performance_detector.data_processing.trace_parser import TraceParser


def calculate_average_duration(json_file_path):
    traces = TraceParser.parse_from_file(json_file_path)

    for trace in traces:
        total_duration = 0
        num_spans = len(trace.spans)

        if num_spans == 0:
            average_duration = 0
        else:
            for span in trace.spans:
                total_duration += span.duration

            average_duration = total_duration / num_spans

        print(f"Trace {trace.trace_id}: Average duration of spans = {average_duration:.2f} ms")


def main():
    json_file_path = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\\cat-api_traces_1719040788.json"
    calculate_average_duration(json_file_path)


if __name__ == "__main__":
    main()
