from performance_detector.data_processing.trace_elements import Trace, Span, Tag
from performance_detector.detectors.base_detector import BaseDetector


class DuplicateSpanIDDetector(BaseDetector):
    def __init__(self):
        super().__init__()

    def detect_duplicate_span_ids(self, trace: Trace):
        issues = []

        span_ids_seen = set()
        for span in trace.spans:
            if span.span_id in span_ids_seen:
                # Found a duplicate span ID issue
                issue_description = f"Duplicate Span ID issue detected in '{span.operation_name}': Span ID '{span.span_id}' is duplicated."
                if self.has_namespace_and_function(span):
                    issue_description += f" (Namespace: {span.namespace}, Function: {span.function})"
                issues.append(issue_description)
            else:
                span_ids_seen.add(span.span_id)

        return issues

    def has_namespace_and_function(self, span: Span):
        # Check if the span has 'code.namespace' and 'code.function' tags
        for tag in span.tags:
            if tag.key == 'code.namespace':
                span.namespace = tag.value
            elif tag.key == 'code.function':
                span.function = tag.value

        return hasattr(span, 'namespace') and hasattr(span, 'function')
