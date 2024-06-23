class TraceAnalyzer:
    def __init__(self, detectors):
        self.detectors = detectors

    def analyze(self, trace):
        results = {}
        for detector in self.detectors:
            result = detector.detect(trace)
            if result:
                results[detector.__class__.__name__] = result
        return results

    def analyze_multiple(self, traces):
        all_results = {}
        for trace in traces:
            trace_results = self.analyze(trace)
            if trace_results:
                all_results[trace.trace_id] = trace_results
        return all_results
