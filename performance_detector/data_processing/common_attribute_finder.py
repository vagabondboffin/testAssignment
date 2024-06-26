from collections import defaultdict
from performance_detector.data_processing.trace_elements import Trace, Span, Tag
from performance_detector.data_processing.trace_parser import TraceParser
from typing import List, Dict, Union
from collections import Counter


class CommonAttributesFinder:
    def __init__(self):
        pass

    def find_common_attributes(self, traces: List[Trace]) -> Dict[str, Union[List[str], Dict[str, List[str]]]]:
        common_span_attributes = self._find_common_span_attributes(traces)
        common_tag_attributes = self._find_common_tag_attributes(traces)

        return {
            'common_span_attributes': common_span_attributes,
            'common_tag_attributes': common_tag_attributes
        }

    def _find_common_span_attributes(self, traces: List[Trace]) -> List[str]:
        if not traces:
            return []

        common_attributes = set(vars(traces[0].spans[0]).keys())  # Initial set with attributes of the first span

        for trace in traces:
            for span in trace.spans:
                common_attributes.intersection_update(vars(span).keys())

        return list(common_attributes)


    def _find_common_tag_attributes(self, traces: List[Trace]) -> List[str]:
        # Find common tag keys among all tags in all spans across all traces
        if not traces:
            return []

        common_tag_keys = set()
        initial_span_tags = traces[0].spans[0].tags if traces[0].spans else []

        common_tag_keys.update(tag.key for tag in initial_span_tags)

        for trace in traces:
            for span in trace.spans:
                span_tag_keys = set(tag.key for tag in span.tags)
                common_tag_keys.intersection_update(span_tag_keys)

        return list(common_tag_keys)



# Example usage
if __name__ == "__main__":
    path3 = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\\trace_get_all_cats.json"
    path4 = "A:\py\pythonProjects\\testAssignment\\trace_exploration\\traces\\trace_generate_pairs_with_error.json"
    trace_files = [path3, path4]
    traces = []
    for file in trace_files:
        traces.extend(TraceParser.parse_from_file(file)) # List of Trace objects

    finder = CommonAttributesFinder()
    common_attributes = finder.find_common_attributes(traces)

    print("Common Span Attributes:", common_attributes['common_span_attributes'])
    print("Common Tag Attributes:", common_attributes['common_tag_attributes'])
