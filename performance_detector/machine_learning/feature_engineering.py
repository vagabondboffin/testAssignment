import pandas as pd
from typing import List, Dict, Union

from performance_detector.data_processing.trace_elements import Trace, Span, Tag
from performance_detector.data_processing.trace_parser import TraceParser


from sklearn.preprocessing import LabelEncoder


class FeatureEngineering:
    def __init__(self):
        pass

    def extract_features(self, traces: List[dict]) -> pd.DataFrame:
        data = []

        for trace in traces:
            trace_id = trace.trace_id

            for span in trace.spans:
                span_id = span.span_id
                duration = span.duration
                process_id = span.process_id
                operation_name = span.operation_name.split()[0]  # Take the first word
                has_logs = 1 if span.logs else 0
                start_time = span.start_time
                has_warnings = 1 if span.warnings else 0
                is_child = 1 if span.references else 0
                is_http = self.is_http_span(span)
                is_database = self.is_db_span(span)

                # Prepare the row for the DataFrame
                data.append({
                    'trace_id': trace_id,
                    'span_id': span_id,
                    'duration': duration,
                    'process_id': process_id,
                    'operation_name': operation_name,
                    'has_logs': has_logs,
                    'start_time': start_time,
                    'has_warnings': has_warnings,
                    'is_child': is_child,
                    'is_http': 1 if is_http else 0,
                    'is_database': 1 if is_database else 0
                })

        # Create DataFrame
        df = pd.DataFrame(data)

        # Encoding categorical variables
        df['operation_name'] = df['operation_name'].astype('category').cat.codes
        df['process_id'] = df['process_id'].astype('category').cat.codes

        # Return the final DataFrame
        return df

    def encode_categorical(self, column: pd.Series) -> pd.Series:
        # Use LabelEncoder to encode categorical columns
        le = LabelEncoder()
        encoded_column = le.fit_transform(column)
        return encoded_column

    def extract_operation_name(self, operation_name: str) -> str:
        # Extract the first word from the operation name
        if operation_name:
            return operation_name.split()[0]
        return ""

    def has_logs(self, logs: List[str]) -> bool:
        # Check if logs list is non-empty
        return bool(logs)

    def has_warning(self, warning: str) -> bool:
        # Check if warning string is not None or empty
        return bool(warning)

    def is_child(self, references: List[str]) -> bool:
        # Check if references list is non-empty
        return bool(references)

    def _find_common_span_attributes(self, traces: List[Trace]) -> List[str]:
        # Find common attributes among all spans
        if not traces:
            return []

        common_attributes = set(traces[0].spans[0].__dict__.keys())  # Initialize with attributes of the first span
        for trace in traces:
            for span in trace.spans:
                common_attributes.intersection_update(span.__dict__.keys())

        return list(common_attributes)

    def _find_common_tag_attributes(self, traces: List[Trace]) -> List[str]:
        # Find common tag keys among all tags in all spans across all traces
        if not traces:
            return []

        common_tag_keys = set()
        initial_span_tags = traces[0].spans[0].tags if traces[0].spans else []

        # Initialize with tag keys from the first span's tags
        common_tag_keys.update(tag.key for tag in initial_span_tags)

        # Check if 'span.kind' and 'internal.span.format' have values
        if 'span.kind' in common_tag_keys:
            common_tag_keys.remove('span.kind')
        if 'internal.span.format' in common_tag_keys:
            common_tag_keys.remove('internal.span.format')

        for trace in traces:
            for span in trace.spans:
                span_tag_keys = set(tag.key for tag in span.tags)
                common_tag_keys.intersection_update(span_tag_keys)

        return list(common_tag_keys)

    def is_http_span(self, span: Span) -> bool:
        # Check if the span has HTTP-related tags or operation name
        http_keys = ['http.url', 'http.method', 'http.status_code', 'http.response_content_length']
        for tag in span.tags:
            if tag.key in http_keys:
                return True
        if any(method in span.operation_name for method in ['GET', 'POST', 'PUT', 'DELETE']):
            return True
        return False

    def is_db_span(self, span: Span) -> bool:
        # Check if the span is related to a database operation based on its tags
        for tag in span.tags:
            if tag.key == 'db.statement':
                return True
        return False


if __name__ == "__main__":
    path1 = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\cat-api_traces_1719225841.json"
    path2 = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\cat-api_traces_1719040788.json"
    path3 = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\\trace_get_all_cats.json"
    path4 = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\\trace_generate_pairs_with_error.json"
    path5 = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\\trace_add_cat.json"
    path6 = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\\trace_find_cats_by_name.json"
    path7 = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\\trace_generate_pairs.json"
    path8 = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\\trace_get_all_cats.json"
    path9 = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\\trace_generate_pairs_with_error.json"
    trace_files = [path1, path2, path3, path4, path9, path8, path7, path6, path5]
    traces = []
    for file in trace_files:
        traces.extend(TraceParser.parse_from_file(file))  # List of Trace objects

    fe = FeatureEngineering()
    df = fe.extract_features(traces)
    df.to_csv('spans_features.csv', index=False)

    print(df.head())  # Display the first few rows of the DataFrame
