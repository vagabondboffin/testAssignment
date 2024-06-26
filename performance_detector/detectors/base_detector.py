from performance_detector.data_processing.trace_elements import Trace, Span


class BaseDetector:
    def __init__(self):
        pass

    def format_issue(self, issue_type: str, spans: list, trace: Trace) -> str:
        namespace, function = self.find_namespace_function(spans, trace)
        return f"{issue_type} issue detected in '{namespace}' -> '{function}': {len(spans)} spans involved."

    def find_namespace_function(self, spans: list, trace: Trace) -> tuple:
        for span in spans:
            for tag in span.tags:
                if tag.key == 'code.namespace':
                    namespace = tag.value
                elif tag.key == 'code.function':
                    function = tag.value

            if 'namespace' in locals() and 'function' in locals():
                break

            # Check references if namespace and function not found in tags
            if 'namespace' not in locals() or 'function' not in locals():
                for ref in span.references:
                    if ref['refType'] == 'CHILD_OF':
                        parent_span = self.find_span_by_id(trace, ref['spanID'])
                        if parent_span:
                            for tag in parent_span.tags:
                                if tag.key == 'code.namespace':
                                    namespace = tag.value
                                elif tag.key == 'code.function':
                                    function = tag.value

                            if 'namespace' in locals() and 'function' in locals():
                                break

        return namespace, function

    def find_span_by_id(self, trace: Trace, span_id: str) -> Span:
        # Find a span by its span_id in the given trace
        for span in trace.spans:
            if span.span_id == span_id:
                return span
        return None

    def is_http_span(self, span: Span) -> bool:
        # Check if the span has HTTP-related tags
        for tag in span.tags:
            if tag.key in ['http.url', 'http.method', 'http.status_code', 'http.response_content_length']:
                return True
        # Check if the operation name contains HTTP methods
        if any(method in span.operation_name for method in ['GET', 'POST', 'PUT', 'DELETE']):
            return True
        return False