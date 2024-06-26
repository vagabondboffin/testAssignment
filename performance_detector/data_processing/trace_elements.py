class Tag:
    def __init__(self, tag_key, tag_value):
        self.key = tag_key
        self.value = tag_value

class Span:
    def __init__(self, span_id, operation_name, start_time, duration, tags=None,
                 logs=None, references=None, process_id=None, warnings=None):
        self.span_id = span_id
        self.operation_name = operation_name
        self.start_time = start_time
        self.duration = duration
        self.tags = [Tag(tag_key = tag['key'], tag_value = tag['value']) for tag in tags] if tags else []
        self.references = references if references else []
        self.logs = logs
        self.process_id = process_id
        self.warnings = warnings

class Trace:
    def __init__(self, trace_id, spans=None, processes=None, warnings=None):
        self.trace_id = trace_id
        self.spans = [Span(span_id=span['spanID'], operation_name=span['operationName'], start_time=span['startTime'],
                           duration=span['duration'], tags=span.get('tags'), references=span.get('references'),
                           logs=span.get('logs'), process_id=span.get('processID'), warnings=span.get('warnings')) for span in spans] if spans else []
        self.processes = processes if processes else {}
        self.warnings = warnings
