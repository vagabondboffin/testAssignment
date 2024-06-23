import json
from .trace_elements import Trace


class TraceParser:
    @staticmethod
    def parse_multiple(raw_traces: dict) -> list:
        traces = []
        for trace_data in raw_traces['data']:
            trace_id = trace_data['traceID']
            spans = trace_data['spans']
            processes = trace_data.get('processes')
            warnings = trace_data.get('warnings')
            trace = Trace(trace_id=trace_id, spans=spans, processes=processes, warnings=warnings)
            traces.append(trace)

        return traces

    @staticmethod
    def parse_from_file(file_path: str) -> list:
        with open(file_path, 'r') as file:
            raw_traces = json.load(file)
        return TraceParser.parse_multiple(raw_traces)
