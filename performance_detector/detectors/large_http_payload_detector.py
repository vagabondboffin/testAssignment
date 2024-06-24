from .base_detector import BaseDetector


class LargeHttpPayloadDetector(BaseDetector):
    """
    LargeHttpPayloadDetector detects large HTTP payload issues in traces.

    Definition:
    Large HTTP Payload issues are created when an HTTP span has an encoded body size that exceeds a threshold.

    Detection Criteria:
    - The HTTP URL must not begin with _next/static/ or _next/data/.
    - The HTTP URL must not end with an extension (e.g., .js, .css, .png, .jpg, .jpeg, .mp3), unless the extension is .json.
    - The HTTP span must have an http.response_content_length that exceeds 300KB.
    - The HTTP span duration must exceed 100ms.

    Source:
    https://docs.sentry.io/product/issues/issue-details/performance-issues/large-http-payload/
    """

    def __init__(self, payload_size_threshold_kb=300, duration_threshold_ms=100):
        self.payload_size_threshold_kb = payload_size_threshold_kb
        self.duration_threshold_ms = duration_threshold_ms

    def detect(self, trace):
        issues = []
        for span in trace.spans:
            if self._is_large_http_payload(span):
                namespace, function = self.find_namespace_function([span], trace)
                payload_size_kb = self._get_payload_size(span) / 1024  # Convert bytes to KB
                issues.append(
                    f"Large HTTP Payload Span: {namespace}.{function} - {span.operation_name} - Payload size: {payload_size_kb:.2f} KB")
        return issues

    def _is_large_http_payload(self, span):
        url, response_content_length, duration_ms = None, None, span.duration / 1000  # Convert microseconds to milliseconds

        # First check if span has 'http.url' indicating it is an HTTP span
        for tag in span.tags:
            if tag.key == 'http.url':
                url = tag.value
                break

        if not url:
            return False

        # Now check for 'http.response_content_length' tag
        for tag in span.tags:
            if tag.key == 'http.response_content_length':
                response_content_length = tag.value

        if not response_content_length:
            return False

        # Check URL criteria
        if url.startswith('_next/static/') or url.startswith('_next/data/'):
            return False
        if not url.endswith('.json') and any(
                url.endswith(ext) for ext in ['.js', '.css', '.png', '.jpg', '.jpeg', '.mp3']):
            return False

        # Check payload size and duration criteria
        if response_content_length > self.payload_size_threshold_kb * 1024 and duration_ms > self.duration_threshold_ms:
            return True

        return False

    def _get_payload_size(self, span):
        for tag in span.tags:
            if tag.key == 'http.response_content_length':
                return tag.value  # Payload size is in bytes
        return 0
