from performance_detector.detectors.base_detector import BaseDetector
from performance_detector.data_processing.trace_parser import TraceParser
from performance_detector.data_processing.trace_elements import Trace, Span, Tag
import json
class ErrorDetector(BaseDetector):
    def __init__(self):
        super().__init__()

    def is_error_span(self, span: Span) -> bool:
        for tag in span.tags:
            if tag.key == 'error' and tag.value:
                return True
        return False

    def get_http_status_code(self, span: Span) -> str:
        for tag in span.tags:
            if tag.key == 'http.status_code':
                return tag.value
        return None

    def get_code_details(self, span: Span) -> dict:
        details = {}
        for tag in span.tags:
            if tag.key == 'code.function':
                details['function'] = tag.value
            elif tag.key == 'code.namespace':
                details['namespace'] = tag.value
        return details

    def get_exception_message(self, span: Span) -> str:
        if span.logs:
            for log in span.logs:
                if 'event' in log and log['event'] == 'exception':
                    if 'message' in log:
                        return log['message']
        return None

    def build_error_hierarchy(self, span: Span, trace: Trace, visited_spans: set) -> dict:
        if span.span_id in visited_spans:
            return {}
        visited_spans.add(span.span_id)

        error_info = {
            'span_id': span.span_id,
            'operation_name': span.operation_name,
            'is_http': self.is_http_span(span),
            'http_status_code': self.get_http_status_code(span) if self.is_http_span(span) else None,
            'code_details': self.get_code_details(span) if not self.is_http_span(span) else None,
            'exception_message': self.get_exception_message(span),
            'children': []
        }

        # Recursively add child span errors
        for ref in span.references:
            if ref['refType'] == 'CHILD_OF':
                child_span = self.find_span_by_id(trace, ref['spanID'])
                if child_span and self.is_error_span(child_span):
                    error_info['children'].append(self.build_error_hierarchy(child_span, trace, visited_spans))

        return error_info

    def analyze_errors(self, trace: Trace) -> list:
        error_hierarchies = []
        visited_spans = set()

        for span in trace.spans:
            #print(self.is_error_span(span))
            if self.is_error_span(span):
                error_hierarchy = self.build_error_hierarchy(span, trace, visited_spans)
                error_hierarchies.append(error_hierarchy)

        return error_hierarchies

    def detect_errors(self, trace: list) -> dict:
        result = {}
        error_hierarchies = self.analyze_errors(trace)
        result[trace.trace_id] = error_hierarchies

        return result

# Example usage
# path1 = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\cat-api_traces_1719225841.json"
# path2 = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\cat-api_traces_1719040788.json"
# path3 = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\\trace_get_all_cats.json"
# path4 = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\\trace_generate_pairs_with_error.json"
# trace_files = [path3, path4]
# traces = []
# for file in trace_files:
#     traces.extend(TraceParser.parse_from_file(file))
#
# detector = ErrorDetector()
# error_analysis_results = detector.detect_errors(traces)

#with open('files/error_analysis_results2.json', 'w') as f:
    #json.dump(error_analysis_results, f, indent=4)
