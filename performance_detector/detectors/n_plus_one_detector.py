from performance_detector.detectors.base_detector import BaseDetector
from performance_detector.data_processing.trace_elements import Trace, Span, Tag


class NPlusOneDetector(BaseDetector):
    """
    NPlusOneDetector detects N+1 query issues in traces.

    Definition:
    N+1 Queries are a performance problem in which the application makes database queries in a loop,
    instead of making a single query that returns or modifies all the information at once.

    Detection Criteria:
    - The detector looks for a set of sequential, non-overlapping database spans with similar descriptions.
    - Total duration of involved spans must exceed 50ms.
    - Total count of involved spans must exceed a threshold (usually five spans).
    - Involved spans must have full queries as their descriptions (some SDKs truncate queries and add an ellipsis to the end).
    - There must be at least one database span that precedes the repeating spans (this is called the "source" span).

    Source:
    https://docs.sentry.io/product/issues/issue-details/performance-issues/n-one-queries/
    """

    def __init__(self):
        super().__init__()

    def detect_n_plus_one_queries(self, trace: Trace) -> list:
        n_plus_one_issues = []

        # Find all db_spans in the trace
        db_spans = [span for span in trace.spans if self.is_db_span(span)]

        # Detect N+1 query issues
        if db_spans:
            db_span_sequences = self.find_db_span_sequences(db_spans)
            for sequence in db_span_sequences:
                if self.is_n_plus_one_issue(sequence, db_spans):
                    issue_description = self.format_issue("N+1 Query", sequence, trace)
                    n_plus_one_issues.append(issue_description)

        return n_plus_one_issues

    def is_db_span(self, span: Span) -> bool:
        # Check if the span is related to a database operation based on its tags
        for tag in span.tags:
            if tag.key == 'db.statement':
                return True
        return False

    def find_db_span_sequences(self, db_spans: list) -> list:
        # Function to find sequences of db_spans in the trace
        sequences = []
        current_sequence = []

        for span in db_spans:
            if not current_sequence or self.are_similar_spans(current_sequence[-1], span):
                current_sequence.append(span)
            else:
                if len(current_sequence) > 1:
                    sequences.append(current_sequence)
                current_sequence = [span]

        if current_sequence and len(current_sequence) > 1:
            sequences.append(current_sequence)

        return sequences

    def are_similar_spans(self, span1: Span, span2: Span) -> bool:
        return span1.operation_name == span2.operation_name

    def is_n_plus_one_issue(self, sequence: list, db_spans: list) -> bool:
        # Check if a sequence of db_spans represents an N+1 query issue
        total_duration = sum(span.duration for span in sequence)
        total_count = len(sequence)

        # Check if spans have full queries and if there's a source span
        if not self.have_full_queries(sequence) or not self.has_source_span(sequence, db_spans):
            return False

        return total_duration > 50 and total_count > 5

    def have_full_queries(self, sequence: list) -> bool:
        # Check if all spans in the sequence have full queries (no ellipsis at the end)
        for span in sequence:
            for tag in span.tags:
                if tag.key == 'db.statement' and tag.value.endswith('...'):
                    return False
        return True

    def has_source_span(self, sequence: list, db_spans: list) -> bool:
        first_span = sequence[0]
        first_span_index = db_spans.index(first_span)

        return first_span_index > 0

