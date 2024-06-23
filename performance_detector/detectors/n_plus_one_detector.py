from base_detector import BaseDetector
from performance_detector.data_processing.trace_elements import Trace, Span, Tag


class NPlusOneDetector(BaseDetector):
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
                if self.is_n_plus_one_issue(sequence):
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
        # Placeholder function to define similarity between spans (customize as needed)
        # For example, compare operation name, query text, etc.
        return span1.operation_name == span2.operation_name

    def is_n_plus_one_issue(self, sequence: list) -> bool:
        # Check if a sequence of db_spans represents an N+1 query issue
        total_duration = sum(span.duration for span in sequence)
        total_count = len(sequence)

        return total_duration > 50 and total_count > 5

